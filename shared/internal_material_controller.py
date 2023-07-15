from collections import defaultdict
import os
from pathlib import Path
from evalquiz_proto.shared.exceptions import (
    DataChunkNotBytesException,
    FileOverwriteNotPermittedException,
)
from evalquiz_proto.shared.generated import LectureMaterial, MaterialUploadData
from typing import AsyncIterator, ByteString
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
import betterproto


class InternalMaterialController:
    """The InternalMaterialController manages accesses to the local file system,
    containing relevant lecture materials.
    """

    def __init__(self) -> None:
        self.internal_lecture_materials: defaultdict[
            str, InternalLectureMaterial
        ] = defaultdict()

    def get_material_from_hash(self, hash: str) -> InternalLectureMaterial:
        """A material that exists as an internal representation can be retrieved using a hash.

        Args:
            hash: A blake3 hash generated using the material.
        """
        return self.internal_lecture_materials[hash]

    def load_material(
        self, local_path: Path, lecture_material: LectureMaterial
    ) -> None:
        """Adds a material to the internal pool of lecture materials.

        Args:
            local_path: The system path to the file.
            lecture_material: Information about the lecture material.
        """
        internal_lecture_material = InternalLectureMaterial(
            local_path, lecture_material
        )
        if internal_lecture_material.hash not in self.internal_lecture_materials:
            self.internal_lecture_materials[
                internal_lecture_material.hash
            ] = internal_lecture_material

    def unload_material(self, hash: str) -> None:
        """Removes the internal representation of a lecture material. Does not delete the file.

        Args:
            hash: A blake3 hash generated using the material.
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
            binary_iterator: An asynchronous iterator with binary data of the file itself.
            overwrite: Boolean to describe if an existing file can be overwritten.
        """
        if os.path.exists(local_path) and not overwrite:
            raise FileOverwriteNotPermittedException()
        while True:
            with open(local_path, "wb") as local_file:
                try:
                    material_upload_data = await binary_iterator.__anext__()
                    (type, data) = betterproto.which_one_of(
                        material_upload_data, "material_upload_data"
                    )
                    if data is not None and type == "lecture_material":
                        local_file.write(data)
                    else:
                        raise DataChunkNotBytesException()
                except StopAsyncIteration:
                    break

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
