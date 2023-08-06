class MimetypeMismatchException(Exception):
    """Expected mimetype does not match the given mimetype."""


class MimetypeNotDetectedException(Exception):
    """Mimetype could not have been detected."""


class MaterialAlreadyLoadedException(Exception):
    """InternalLectureMaterial is already available under the given hash. Unload the existing lecture material first to change its metadata. Delete the existing lecture material first to change its content and metadata."""


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


class NoMimetypeMappingException(Exception):
    """The system could not map any file extension to the given mimetype, the mimetype could be invalid."""


class LectureMaterialCastRequiredException(Exception):
    """InternalLectureMaterial object should be casted to LectureMaterial to ensure correctness. This can be done with the InternalLectureMaterial method cast_to_lecture_material()."""
