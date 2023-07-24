from collections import defaultdict
import jsonpickle
import os
from pathlib import Path
from evalquiz_proto.shared.exceptions import (
    DataChunkNotBytesException,
    FileHasDifferentHashException,
    FileOverwriteNotPermittedException,
    LectureMaterialCastRequiredException,
)
from evalquiz_proto.shared.generated import LectureMaterial, MaterialUploadData
from typing import AsyncIterator, ByteString, Optional
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
import betterproto


class InternalMaterialController:
    """The InternalMaterialController manages accesses to the local file system,
    containing relevant lecture materials.
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Constructor of InternalMaterialController.

        Args:
            config_path (Optional[Path], optional): Specifies where backups of the InternalMaterialController state are saved. Defaults to None.
        """
        self.config_path: Optional[Path] = None
        self.internal_lecture_materials: defaultdict[
            str, InternalLectureMaterial
        ] = defaultdict()
        if config_path is not None:
            self.config_path = config_path
            self.deserialize_from_config()

    def deserialize_from_config(self) -> None:
        """Serializes InternalMaterialController from config.
        Loads all InternalLectureMaterials referenced in the config.
        This method overwrites all existing state of InternalMaterialController.
        """
        if self.config_path is None:
            raise ValueError(
                "config_path is not set. Must be set for serialization or deserialization."
            )
        with open(self.config_path, "r") as local_file:
            config = local_file.read()
        internal_lecture_materials: defaultdict[
            str, InternalLectureMaterial
        ] = jsonpickle.decode(config)
        for internal_lecture_material in internal_lecture_materials.values():
            lecture_material = internal_lecture_material.cast_to_lecture_material()
            print(type(lecture_material))
            self.load_material(internal_lecture_material.local_path, lecture_material)

    def serialize_to_config(self) -> None:
        """Deserializes InternalMaterialController to config.
        Saves all InternalLectureMaterials referenced in the config.
        Contents of an existing config referenced by config_path are overwritten.
        """
        if self.config_path is None:
            raise ValueError(
                "config_path is not set. Must be set for serialization or deserialization."
            )
        serialized_internal_lecture_materials = jsonpickle.encode(
            self.internal_lecture_materials
        )
        with open(self.config_path, "w") as local_file:
            local_file.write(serialized_internal_lecture_materials)

    async def get_material_from_hash_async(
        self, hash: str, content_partition_size: int = 5 * 10**8
    ) -> AsyncIterator[MaterialUploadData]:
        """A material that exists as an internal representation can be retrieved using a hash.
        Arbitrary large files can be read, as only a partition of the file is read at a time.

        Args:
            hash (str): Hash generated using the material
            content_partition_size (int, optional): Amount of bytes that are read from the file at one time. Defaults to 5*10**8.

        Returns:
            AsyncIterator[MaterialUploadData]: Yields MaterialUploadData, this can be metadata or binary data of the file itself.
        """
        content_partition_size
        internal_lecture_material = self.internal_lecture_materials[hash]
        material_upload_data = MaterialUploadData(
            lecture_material=internal_lecture_material.cast_to_lecture_material()
        )
        yield material_upload_data
        with open(internal_lecture_material.local_path, "rb") as local_file:
            while content_partition := local_file.read(content_partition_size):
                print(content_partition)
                material_upload_data = MaterialUploadData(data=content_partition)
                yield material_upload_data

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
            if internal_lecture_material.hash not in self.internal_lecture_materials:
                self.internal_lecture_materials[
                    internal_lecture_material.hash
                ] = internal_lecture_material
        else:
            raise FileHasDifferentHashException()

    def unload_material(self, hash: str) -> None:
        """Removes the internal representation of a lecture material. Does not delete the file.

        Args:
            hash: Hash generated using the material.
        """
        del self.internal_lecture_materials[hash]

    def add_material(
        self,
        local_path: Path,
        lecture_material: LectureMaterial,
        binary: ByteString,
        overwrite: bool = True,
    ) -> None:
        """A new material is created at the specified location.

        Args:
            local_path: The system path to the location where the file is created.
            lecture_material: Information about the lecture material.
            binary: Binary data of the lecture material file itself.
            overwrite: Boolean to describe if an existing file can be overwritten.
        """
        if os.path.exists(local_path) and not overwrite:
            raise FileOverwriteNotPermittedException()
        with open(local_path, "wb") as local_file:
            local_file.write(binary)
        self.load_material(local_path, lecture_material)

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
        internal_lecture_material = self.internal_lecture_materials[hash]
        self.unload_material(hash)
        os.remove(internal_lecture_material.local_path)

    def get_material_hashes(self) -> list[str]:
        """Retrieves all hashes of the internally referenced materials.

        Returns:
            A set of strings
        """
        return list(self.internal_lecture_materials.keys())
