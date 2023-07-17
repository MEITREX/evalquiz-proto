from dataclasses import dataclass
import mimetypes
import os
from pathlib import Path
from evalquiz_proto.shared.generated import LectureMaterial
from blake3 import blake3
from evalquiz_proto.shared.exceptions import (
    MimetypeMismatchException,
    MimetypeNotDetectedException,
)


@dataclass(init=False)
class InternalLectureMaterial(LectureMaterial):
    """A lecture material with an additional local path pointing to the file."""

    local_path: Path = Path("")

    def __init__(self, local_path: Path, lecture_material: LectureMaterial):
        self.local_path = local_path
        self.reference = lecture_material.reference
        self.page_filter = lecture_material.page_filter
        self._evaluate_mimetype(lecture_material.file_type)
        self.update_hash()

    def update_hash(self, rename_file: bool = False) -> None:
        """Updates LectureMaterial hash with file contents.

        Args:
            rename_file (bool, optional): Filename of referenced file is changed to the updated hash, if set to True. Defaults to False.
        """
        with open(self.local_path, "r") as local_file:
            file_content = local_file.read()
        hash = blake3(file_content.encode("utf-8")).hexdigest()
        if hash != self.hash:
            self.hash = hash
            self._update_mimetype()
            if rename_file:
                self._rename_file(hash)

    def _rename_file(self, hash: str) -> None:
        """Renames a file to the newly calculated hash.

        Args:
            hash: The newly calculated hash and filename
        """
        absolute_path = os.path.abspath(self.local_path)
        folder_path = os.path.dirname(absolute_path)
        renamed_path = Path(folder_path) / hash
        os.rename(self.local_path, renamed_path)

    def verify_hash(self) -> bool:
        """Verifies that file did not change using the reference parameter and file contents.

        Returns:
            True, if parameter hash matches calculated hash of file.
        """
        with open(self.local_path, "r") as local_file:
            file_content = local_file.read()
            return self.hash == blake3(file_content.encode("utf-8")).hexdigest()

    def _evaluate_mimetype(self, mimetype: str) -> None:
        """Evaluates if given mimetype matches the mimetype of file at local_path.

        Raises:
            MimetypeNotDetectedException
            MimetypeMismatchException
        """
        (type, _) = mimetypes.guess_type(self.local_path)
        if type is None:
            raise MimetypeNotDetectedException()
        if type != mimetype:
            raise MimetypeMismatchException()

    def _update_mimetype(self) -> None:
        """Updates mimetype to match the mimetype of file at local_path."""
        (type, _) = mimetypes.guess_type(self.local_path)
        if type is not None:
            self.file_type = type
