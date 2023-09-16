import mimetypes
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
            (type, _) = mimetypes.guess_type(suffix)
            return type
