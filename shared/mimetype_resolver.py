import mimetypes
from pathlib import Path
from typing import Optional


class MimetypeResolver:
    @staticmethod
    def fixed_guess_type(suffix: str) -> Optional[str]:
        """Fixes the missing markdown type in Python's mimetypes library.

        Args:
            local_path (Path): Path to guess type for.

        Returns:
            str: The guessed mime type.

        Raises:
            MimetypeNotDetectedException
        """
        if suffix == ".md" or suffix == ".markdown":
            return "text/markdown"
        if suffix == ".pptx":
            return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            local_path = Path("test/misc" + suffix)
            (type, _) = mimetypes.guess_type(local_path, strict=False)
            return type

    @staticmethod
    def fixed_guess_extension(mimetype: str) -> Optional[str]:
        """Fixes the missing markdown type in Python's mimetypes library.

        Args:
            mimetype (str): Mimetype to guess extension for.

        Returns:
            Optional[str]: Extension with leading dot.
        """
        if mimetype == "text/markdown":
            return ".md"
        if mimetype == ".pptx":
            return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        else:
            return mimetypes.guess_extension(mimetype, strict=False)
