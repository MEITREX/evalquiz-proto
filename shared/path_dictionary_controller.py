import os
from pathlib import Path
import shutil
import jsonpickle

from pymongo import MongoClient
from evalquiz_proto.shared.exceptions import (
    FileOverwriteNotPermittedException,
    MimetypeNotDetectedException,
)
from typing import Any, AsyncIterator

from evalquiz_proto.shared.mimetype_resolver import MimetypeResolver


class PathDictionaryController:
    """The PathDictionaryController manages str aliases to paths for local files.
    Multiple PathDictionaryController instances are able to share their state using MongoDB.
    """

    def __init__(
        self,
        mongodb_client: MongoClient[dict[str, Any]],
        mongodb_database: str = "local_path_db",
    ) -> None:
        """Constructor of InternalMaterialController.

        Args:
            mongodb_client (MongoClient[dict[str, Any]]): A pymongo client to enable communication with a MongoDB server.
            mongodb_database: (str): The database that all operations are performed on.
        """
        self.mongodb_client = mongodb_client
        self.local_paths = mongodb_client[mongodb_database].local_paths

    def get_file_path_from_hash(self, hash: str) -> Path:
        """Retrieves local path from hash.

        Args:
            hash (str): Hash to reference the file.

        Raises:
            KeyError: If file is not found under the given hash.

        Returns:
            Path: The path to the local file.
        """
        mongodb_document = self.local_paths.find_one({"_id": hash})
        if mongodb_document is None:
            raise KeyError()
        return jsonpickle.decode(mongodb_document["local_path"])

    async def get_file_from_hash_async(
        self, hash: str, content_partition_size: int = 5 * 10**8
    ) -> tuple[str, AsyncIterator[bytes]]:
        """Streams a local file using the given hash and returns its mimetype.

        Args:
            hash (str): Hash to reference the file.
            content_partition_size (int, optional): The maximum filesize in bytes that a packet can have. Defaults to 5*10**8.

        Raises:
            KeyError: If file is not found under the given hash.

        Returns:
            tuple[str, AsyncIterator[MaterialUploadData]]: A tuple with the mimetype at the first index and the asynchronous iterator for streaming at the second index.
        """
        mongodb_document = self.local_paths.find_one({"_id": hash})
        if mongodb_document is None:
            raise KeyError()
        local_path = jsonpickle.decode(mongodb_document["local_path"])
        mimetype = MimetypeResolver.fixed_guess_type(local_path.suffix)
        if mimetype is None:
            raise MimetypeNotDetectedException()
        material_upload_data_iterator = self._get_async_iterator_of_local_file(
            local_path, content_partition_size
        )
        return (mimetype, material_upload_data_iterator)

    async def _get_async_iterator_of_local_file(
        self, local_path: Path, content_partition_size: int = 5 * 10**8
    ) -> AsyncIterator[bytes]:
        """Streams binary data of a file under local_path.

        Args:
            local_path (Path): The path of the file to be stream.
            content_partition_size (int, optional): The maximum filesize in bytes that a packet can have. Defaults to 5*10**8.

        Returns:
            AsyncIterator[bytes]: Iterator with binary packets.
        """
        with open(local_path, "rb") as local_file:
            while content_partition := local_file.read(content_partition_size):
                yield content_partition

    def load_file(self, local_path: Path, hash: str, name: str = "") -> None:
        """Adds a file to the internal pool of files.

        Args:
            local_path (Path): The system path to the file.
            hash (str): Hash to reference the file.
            name: Name or description of the file to load.
        """
        mongodb_document = {
            "_id": hash,
            "name": name,
            "local_path": jsonpickle.encode(local_path),
        }
        self.local_paths.update_one(
            {"_id": mongodb_document["_id"]},
            {"$set": mongodb_document},
            upsert=True,
        )

    def unload_material(self, hash: str) -> None:
        """Removes the internal representation of a lecture material. Does not delete the file.

        Args:
            hash: Hash to reference the file.
        """
        self.local_paths.delete_one({"_id": hash})

    async def add_file_async(
        self,
        local_path: Path,
        hash: str,
        binary_iterator: AsyncIterator[bytes],
        overwrite: bool = True,
        name: str = "",
    ) -> None:
        """A new file is created asynchronously at the specified location from a stream.
        System operations are carried out async to allow large file sizes and reduce the memory footprint.

        Args:
            local_path: The system path to the location where the file is created.
            hash: Hash to reference the file.
            binary_iterator: Yields binary data of the file itself.
            overwrite: Boolean to describe if an existing file can be overwritten.
            name: Name or description of the file to add.

        Raises:
            FileOverwriteNotPermittedException
        """
        if os.path.exists(local_path) and not overwrite:
            raise FileOverwriteNotPermittedException()
        with open(local_path, "ab") as local_file:
            local_file.truncate(0)
            while True:
                try:
                    data = await binary_iterator.__anext__()
                    local_file.write(data)
                except StopAsyncIteration:
                    break
        self.load_file(local_path, hash, name)

    def copy_and_load_file(
        self,
        source_local_path: Path,
        destination_local_path: Path,
        hash: str,
        name: str = "",
    ) -> None:
        """Copies file to destination and loads the destination file with `self.load_file(...)`.

        Args:
            source_local_path (Path): Source file local path.
            destination_local_path (Path): Destination file local path.
            hash (str): Hash to reference the file.
        """
        shutil.copyfile(source_local_path, destination_local_path)
        self.load_file(destination_local_path, hash, name)

    def delete_file(self, hash: str) -> None:
        """Deletes the reference to the file and the file itself from the filesystem.

        Args:
            local_path: The system path to the file.
        """
        mongodb_document = self.local_paths.find_one({"_id": hash})
        if mongodb_document is not None:
            mongodb_document = mongodb_document["local_path"]
            local_path = jsonpickle.decode(mongodb_document)
            self.unload_material(hash)
            if self.local_paths.find_one({"_id": hash}) is None:
                os.remove(local_path)

    def get_material_hashes(self) -> list[str]:
        """Retrieves all hashes of the internally referenced files.

        Returns:
            A set of strings
        """
        return [str(id) for id in self.local_paths.distinct("_id")]

    def get_material_name(self, hash: str) -> str:
        """Returns material name from hash.

        Args:
            hash (str): Hash to reference the file.

        Raises:
            KeyError: If file is not found under the given hash

        Returns:
            str: Material name.
        """
        mongodb_document = self.local_paths.find_one({"_id": hash})
        if mongodb_document is None:
            raise KeyError()
        return mongodb_document["name"]
