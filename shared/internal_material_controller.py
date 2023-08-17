import os
from pathlib import Path

from pymongo import MongoClient
from evalquiz_proto.shared.exceptions import (
    DataChunkNotBytesException,
    FileHasDifferentHashException,
    FileOverwriteNotPermittedException,
    LectureMaterialCastRequiredException,
    LectureMaterialLocallyNotFoundException,
)
from evalquiz_proto.shared.generated import LectureMaterial, MaterialUploadData
from typing import Any, AsyncIterator
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
import betterproto


class InternalMaterialController:
    """The InternalMaterialController manages accesses to the local file system,
    containing relevant lecture materials.
    The state of lecture materials that are available on the host is managed by MongoDB.
    Multiple InternalMaterialControllers are able to share this state through MongoDB.
    """

    def __init__(
        self,
        mongodb_client: MongoClient[dict[str, Any]] = MongoClient("db", 27017),
        mongodb_database: str = "lecture_material_db",
    ) -> None:
        """Constructor of InternalMaterialController.

        Args:
            mongodb_client (MongoClient[dict[str, Any]]): A pymongo client to enable communication with a MongoDB server.
            mongodb_database: (str): The database that all operations are performed on.
        """
        self.mongodb_client = mongodb_client
        self.internal_lecture_materials = mongodb_client[
            mongodb_database
        ].lecture_materials

    async def get_material_from_hash_async(
        self, hash: str, content_partition_size: int = 5 * 10**8
    ) -> AsyncIterator[MaterialUploadData]:
        """A material that exists as an internal representation can be retrieved using a hash.
        Arbitrary large files can be read, as only a partition of the file is read at a time.

        Args:
            hash (str): Hash generated using the material.
            content_partition_size (int, optional): Amount of bytes that are read from the file at one time. Defaults to 5*10**8.

        Raises:
            KeyError: Lecture material of given hash is locally not found.

        Returns:
            AsyncIterator[MaterialUploadData]: Yields MaterialUploadData, this can be metadata or binary data of the file itself.
        """
        mongodb_document = self.internal_lecture_materials.find_one({"_id": hash})
        if mongodb_document is None:
            raise KeyError()
        internal_lecture_material = InternalLectureMaterial.from_mongodb_document(
            mongodb_document
        )
        material_upload_data = MaterialUploadData(
            lecture_material=internal_lecture_material.cast_to_lecture_material()
        )
        yield material_upload_data
        with open(internal_lecture_material.local_path, "rb") as local_file:
            while content_partition := local_file.read(content_partition_size):
                print(content_partition)
                material_upload_data = MaterialUploadData(data=content_partition)
                yield material_upload_data

    def get_material_path_from_hash(self, hash: str) -> Path:
        """Returns the local path of the lecture material, if it is present in the internal pool of lecture materials.

        Args:
            hash (str): Hash generated using the material.

        Raises:
            LectureMaterialLocallyNotFoundException

        Returns:
            Path: A local path to the lecture material.
        """
        mongodb_document = self.internal_lecture_materials.find_one({"_id": hash})
        if mongodb_document is None:
            raise LectureMaterialLocallyNotFoundException()
        internal_lecture_material = InternalLectureMaterial.from_mongodb_document(
            mongodb_document
        )
        return internal_lecture_material.local_path

    def load_material(
        self, local_path: Path, lecture_material: LectureMaterial
    ) -> None:
        """Adds a material to the internal pool of lecture materials.

        Args:
            local_path: The system path to the file.
            lecture_material: Information about the lecture material.

        Raises:
            FileHasDifferentHashException
        """
        if type(lecture_material) is not LectureMaterial:
            raise LectureMaterialCastRequiredException()
        received_hash = lecture_material.hash
        internal_lecture_material = InternalLectureMaterial(
            local_path, lecture_material
        )
        if internal_lecture_material.verify_hash(received_hash):
            mongodb_document = internal_lecture_material.to_mongodb_document()
            self.internal_lecture_materials.update_one(
                {"_id": mongodb_document["_id"]},
                {"$set": mongodb_document},
                upsert=True,
            )
        else:
            raise FileHasDifferentHashException()

    def unload_material(self, hash: str) -> None:
        """Removes the internal representation of a lecture material. Does not delete the file.

        Args:
            hash: Hash generated using the material.
        """
        self.internal_lecture_materials.delete_one({"_id": hash})

    async def add_material_async(
        self,
        local_path: Path,
        lecture_material: LectureMaterial,
        binary_iterator: AsyncIterator[MaterialUploadData],
        overwrite: bool = True,
    ) -> None:
        """A new material is created asynchronously at the specified location.
        System operations are carried out async to allow large file sizes and reduce the memory footprint.

        Args:
            local_path: The system path to the location where the file is created.
            lecture_material: Information about the lecture material.
            binary_iterator: Yields MaterialUploadData, this can be metadata or binary data of the file itself.
            overwrite: Boolean to describe if an existing file can be overwritten.

        Raises:
            FileOverwriteNotPermittedException
            FileHasDifferentHashException
        """
        if os.path.exists(local_path) and not overwrite:
            raise FileOverwriteNotPermittedException()
        with open(local_path, "ab") as local_file:
            local_file.truncate(0)
            while True:
                try:
                    material_upload_data = await binary_iterator.__anext__()
                    (datatype, data) = betterproto.which_one_of(
                        material_upload_data, "material_upload_data"
                    )
                    if data is not None and datatype == "data":
                        local_file.write(data)
                    else:
                        raise DataChunkNotBytesException()
                except StopAsyncIteration:
                    break
        try:
            self.load_material(local_path, lecture_material)
        except FileHasDifferentHashException:
            os.remove(local_path)
            raise FileHasDifferentHashException()

    def delete_material(self, hash: str) -> None:
        """Deletes the internal representation of the file in memory and the file itself from the filesystem.

        Args:
            local_path: The system path to the file.
        """
        mongodb_document = self.internal_lecture_materials.find_one({"_id": hash})
        if mongodb_document is not None:
            internal_lecture_material = InternalLectureMaterial.from_mongodb_document(
                mongodb_document
            )
            self.unload_material(hash)
            if self.internal_lecture_materials.find_one({"_id": hash}) is None:
                os.remove(internal_lecture_material.local_path)

    def get_material_hashes(self) -> list[str]:
        """Retrieves all hashes of the internally referenced materials.

        Returns:
            A set of strings
        """
        return [str(id) for id in self.internal_lecture_materials.distinct("_id")]
