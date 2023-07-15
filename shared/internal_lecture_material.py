from dataclasses import dataclass
import mimetypes
from pathlib import Path
from evalquiz_proto.shared.generated import LectureMaterial
from blake3 import blake3
from evalquiz_proto.shared.exceptions import MimetypeMismatchException, MimetypeNotDetectedException


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

    def update_hash(self) -> None:
        """Updates LectureMaterial hash with file contents."""
        with open(self.local_path, "r") as local_file:
            file_content = local_file.read()
        hash = blake3(file_content.encode("utf-8")).hexdigest()
        if hash != self.hash:
            self.hash = hash
            self._update_mimetype()

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
