from dataclasses import dataclass
import mimetypes
from pathlib import Path
from shared.generated import LectureMaterial, PageFilter
from blake3 import blake3
from typing import Optional, TypeVar, Generic
from shared.exceptions import MimetypeMismatchException, MimetypeNotDetectedException


@dataclass(init=False)
class InternalLectureMaterial(LectureMaterial):
    """A lecture material with an additional local path pointing to the file."""

    local_path: str

    def __init__(self, local_path: Path, lecture_material: LectureMaterial):
        self.local_path = local_path
        self.reference = lecture_material.reference
        self.page_filter = lecture_material.page_filter
        self._evaluate_mimetype(lecture_material.file_type)
        self.update_hash()

    def update_hash(self) -> None:
        """Updates LectureMaterial hash with file contents."""
        with open(self.local_path, "r") as local_file:
            file_content: str = local_file.read()
            self.hash = blake3(file_content.encode('utf-8'))

    def verify_hash(self) -> bool:
        """Verifies that file did not change using the reference parameter and file contents.

        Returns:
            True, if parameter hash matches calculated hash of file.
        """
        with open(self.local_path, "r") as local_file:
            file_content = local_file.read()
            return self.hash == blake3(file_content.encode('utf-8'))

    def _evaluate_mimetype(self, mimetype: str) -> None:
        """Evaluates if given mimetype matches the mimetype of file at local_path.

        Raises:
            MimetypeMismatchException
        """
        (
            type,
            _
        ) = mimetypes.guess_type(self.local_path)
        print("dkjslfjdl")
        print(type)
        if type is None:
            raise MimetypeNotDetectedException()
        if type != mimetype:
            raise MimetypeMismatchException()
