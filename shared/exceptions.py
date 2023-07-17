class MimetypeMismatchException(Exception):
    """Expected mimetype does not match the given mimetype."""


class MimetypeNotDetectedException(Exception):
    """Mimetype could not have been detected."""


class MaterialAlreadyLoadedException(Exception):
    """InternalLectureMaterial is already available."""


class EmptyUploadException(ValueError):
    """The uploaded data is empty."""


class FirstDataChunkNotLectureMaterialException(ValueError):
    """The first chunk of a lecture material upload stream should be of type LectureMaterial."""


class DataChunkNotBytesException(ValueError):
    """All chunks of a lecture material upload stream except the first one should be bytes."""


class FileOverwriteNotPermittedException(Exception):
    """A file is already present at the given location and is not permitted to be overwritten."""


class FileHasDifferentHashException(Exception):
    """The file referenced in an internal lecture material has a different hash value than the attribute of the internal lecture material."""
