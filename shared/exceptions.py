class MimetypeMismatchException(Exception):
    """Expected mimetype does not match the given mimetype."""


class MimetypeNotDetectedException(Exception):
    """Mimetype could not have been detected."""


class FirstDataChunkNotMetadataException(ValueError):
    """The first chunk of a lecture material upload stream should be of type Metadata."""


class DataChunkNotBytesException(ValueError):
    """All chunks of a lecture material upload stream except the first one should be bytes."""


class FileOverwriteNotPermittedException(Exception):
    """A file is already present at the given location and is not permitted to be overwritten."""


class NoMimetypeMappingException(Exception):
    """The system could not map any file extension to the given mimetype, the mimetype could be invalid."""


class LectureMaterialNotFoundOnRemotesException(Exception):
    """All remotes have been requested to provide the lecture material, but none of the remotes is able to."""


class LectureMaterialLocallyNotFoundException(Exception):
    """The requested lecture material cannot be provided by the InternalMaterialController."""
