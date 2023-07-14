class MimetypeMismatchException(Exception):
    """Expected mimetype does not match the given mimetype."""


class MimetypeNotDetectedException(Exception):
    """Mimetype could not have been detected."""


class MaterialAlreadyLoadedException(Exception):
    """InternalLectureMaterial is already available."""
