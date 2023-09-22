import mimetypes
from pathlib import Path
from typing import Optional

mimetype_extension_mappings = {
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".epub": "application/epub+zip",
    ".ipynb": "application/x-ipynb+json",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".opml": "text/x-opml",
    ".org": "text/x-org",
    ".ris": "application/x-research-info-systems",
    ".rst": "text/x-rst",
    ".tex": "application/x-tex",
}

mimetype_reverse_extension_mappings = {
    mimetype: extension for extension, mimetype in mimetype_extension_mappings.items()
}


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
        if suffix in mimetype_extension_mappings:
            return mimetype_extension_mappings[suffix]
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
        if mimetype in mimetype_reverse_extension_mappings:
            return mimetype_reverse_extension_mappings[mimetype]
        else:
            return mimetypes.guess_extension(mimetype, strict=False)
