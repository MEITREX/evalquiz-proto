class MimetypeMismatchException(Exception):
    """Expected mimetype does not match the given mimetype."""


class MimetypeNotDetectedException(Exception):
    """Mimetype could not have been detected."""


class FirstDataChunkNotMetadataException(Exception):
    """The first chunk of a lecture material upload stream should be of type Metadata."""


class DataChunkNotBytesException(Exception):
    """All chunks of a lecture material upload stream except the first one should be bytes."""


class FileOverwriteNotPermittedException(Exception):
    """A file is already present at the given location and is not permitted to be overwritten."""


class NoMimetypeMappingException(Exception):
    """The system could not map any file extension to the given mimetype, the mimetype could be invalid."""


class PipelineModuleCompositionNotValidException(Exception):
    """Input and output datatypes at least one successive PipelineModule are not compatible."""


class PipelineExecutionException(Exception):
    """Unexpected behavior occurred in the execution of a PipelineModule"""


class LectureMaterialNotFoundOnRemotesException(PipelineExecutionException):
    """All remotes have been requested to provide the lecture material, but none of the remotes is able to."""


class LectureMaterialLocallyNotFoundException(Exception):
    """The requested lecture material cannot be provided by the InternalMaterialController."""


class ResultException(PipelineExecutionException):
    """The generated result by the language model is not able to be further processed, due to incompatibilities."""


class ResultSectionNotFoundException(ResultException):
    """The result section, marked with `<result></result>` tags was not found in the given text."""


class ResultSectionNotParsableException(ResultException):
    """The structure of the result section, marked with `<result></result>` tags does not match the QuestionType."""


class PipelineModuleRuntimeInputException(Exception):
    """The input given at runtime, does not match the defined input type of the InternalPipelineModule"""


class MissingDefaultInternalConfigAttributeException(Exception):
    """A DefaultInternalConfig attribute was not be found."""


class EvaluationNotCompatibleWithInternalEvaluation(Exception):
    """Evaluation is not compatible with InternalEvaluation. Please check the `QuestionEvaluation.internal_evaluations` mappings."""
