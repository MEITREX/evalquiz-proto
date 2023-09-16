# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: proto/evalquiz.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    AsyncIterable,
    AsyncIterator,
    Dict,
    Iterable,
    List,
    Optional,
    Union,
)

import betterproto
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class EducationalObjective(betterproto.Enum):
    KNOW_AND_UNDERSTAND = 0
    APPLY = 1
    ANALYZE = 2
    SYNTHESIZE = 3
    EVALUATE = 4
    INNOVATE = 5


class Relationship(betterproto.Enum):
    SIMILARITY = 0
    DIFFERENCES = 1
    ORDER = 2
    COMPLEX = 3


class QuestionType(betterproto.Enum):
    MULTIPLE_CHOICE = 0
    MULTIPLE_RESPONSE = 1


class ModuleStatus(betterproto.Enum):
    IDLE = 0
    RUNNING = 1
    FAILED = 2
    SUCCESS = 3


@dataclass(eq=False, repr=False)
class Empty(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class String(betterproto.Message):
    value: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class ListOfStrings(betterproto.Message):
    values: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class MaterialUploadData(betterproto.Message):
    metadata: "Metadata" = betterproto.message_field(1, group="material_upload_data")
    data: bytes = betterproto.bytes_field(2, group="material_upload_data")


@dataclass(eq=False, repr=False)
class Metadata(betterproto.Message):
    mimetype: str = betterproto.string_field(1)
    name: str = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class InternalConfig(betterproto.Message):
    """*Matches question type specification."""

    material_server_urls: List[str] = betterproto.string_field(1)
    batches: List["Batch"] = betterproto.message_field(2)
    course_settings: Optional["CourseSettings"] = betterproto.message_field(
        3, optional=True, group="_course_settings"
    )
    generation_settings: Optional["GenerationSettings"] = betterproto.message_field(
        4, optional=True, group="_generation_settings"
    )
    evaluation_settings: Optional["EvaluationSettings"] = betterproto.message_field(
        5, optional=True, group="_evaluation_settings"
    )


@dataclass(eq=False, repr=False)
class CourseSettings(betterproto.Message):
    course_goals: List["Capability"] = betterproto.message_field(1)
    required_capabilites: List["Capability"] = betterproto.message_field(2)
    advantageous_capabilities: List["Capability"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class Capability(betterproto.Message):
    keywords: List[str] = betterproto.string_field(1)
    educational_objective: "EducationalObjective" = betterproto.enum_field(2)
    relationship: "Relationship" = betterproto.enum_field(3)


@dataclass(eq=False, repr=False)
class GenerationSettings(betterproto.Message):
    mode: Optional["Mode"] = betterproto.message_field(1, optional=True, group="_mode")
    model: Optional[str] = betterproto.string_field(2, optional=True, group="_model")


@dataclass(eq=False, repr=False)
class Mode(betterproto.Message):
    complete: "Complete" = betterproto.message_field(1, group="mode")
    overwrite: "Overwrite" = betterproto.message_field(2, group="mode")
    by_metrics: "ByMetrics" = betterproto.message_field(3, group="mode")


@dataclass(eq=False, repr=False)
class Complete(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class Overwrite(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class ByMetrics(betterproto.Message):
    evaluation_reference: str = betterproto.string_field(1)
    evaluator_type: str = betterproto.string_field(2)
    evaluation_result: "EvaluationResult" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class EvaluationSettings(betterproto.Message):
    metrics: List["Metric"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Question(betterproto.Message):
    question_type: "QuestionType" = betterproto.enum_field(1)
    generation_result: Optional["GenerationResult"] = betterproto.message_field(
        2, optional=True, group="_generation_result"
    )
    evaluation_results: Dict[str, "EvaluationResult"] = betterproto.map_field(
        3, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class GenerationResult(betterproto.Message):
    multiple_choice: "MultipleChoice" = betterproto.message_field(
        1, group="generation_result"
    )
    multiple_response: "MultipleResponse" = betterproto.message_field(
        2, group="generation_result"
    )


@dataclass(eq=False, repr=False)
class MultipleChoice(betterproto.Message):
    question_text: str = betterproto.string_field(1)
    answer_text: str = betterproto.string_field(2)
    distractor_text: List[str] = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class MultipleResponse(betterproto.Message):
    question_text: str = betterproto.string_field(1)
    answer_texts: List[str] = betterproto.string_field(2)
    distractor_texts: List[str] = betterproto.string_field(3)


@dataclass(eq=False, repr=False)
class Metric(betterproto.Message):
    reference: str = betterproto.string_field(1)
    mode: Optional["Mode"] = betterproto.message_field(2, optional=True, group="_mode")
    evaluation: "Evaluation" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class Evaluation(betterproto.Message):
    language_model_evaluation: "LanguageModelEvaluation" = betterproto.message_field(
        1, group="evaluation"
    )


@dataclass(eq=False, repr=False)
class LanguageModelEvaluation(betterproto.Message):
    model: str = betterproto.string_field(1)
    evaluation_description: str = betterproto.string_field(2)
    few_shot_examples: List["GenerationEvaluationResult"] = betterproto.message_field(3)
    evaluation_result_type: "EvaluationResultType" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class EvaluationResultType(betterproto.Message):
    value_range: "ValueRange" = betterproto.message_field(
        1, group="evaluation_result_type"
    )
    categorical: "Categorical" = betterproto.message_field(
        2, group="evaluation_result_type"
    )


@dataclass(eq=False, repr=False)
class EvaluationResult(betterproto.Message):
    str_value: str = betterproto.string_field(1, group="evaluation_result")
    float_value: float = betterproto.float_field(2, group="evaluation_result")


@dataclass(eq=False, repr=False)
class GenerationEvaluationResult(betterproto.Message):
    generation_result: "GenerationResult" = betterproto.message_field(1)
    evaluation_result: "EvaluationResult" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class ValueRange(betterproto.Message):
    lower_bound: float = betterproto.float_field(1)
    upper_bound: float = betterproto.float_field(2)


@dataclass(eq=False, repr=False)
class Categorical(betterproto.Message):
    categories: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class Batch(betterproto.Message):
    lecture_materials: List["LectureMaterial"] = betterproto.message_field(1)
    question_to_generate: List["Question"] = betterproto.message_field(2)
    capabilites: List["Capability"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class LectureMaterial(betterproto.Message):
    reference: str = betterproto.string_field(1)
    url: Optional[str] = betterproto.string_field(2, optional=True, group="_url")
    hash: str = betterproto.string_field(3)
    file_type: str = betterproto.string_field(4)
    page_filter: Optional["PageFilter"] = betterproto.message_field(
        5, optional=True, group="_page_filter"
    )


@dataclass(eq=False, repr=False)
class PageFilter(betterproto.Message):
    lower_bound: int = betterproto.int32_field(1)
    upper_bound: int = betterproto.int32_field(2)


@dataclass(eq=False, repr=False)
class PipelineStatus(betterproto.Message):
    result: Optional["betterproto_lib_google_protobuf.Any"] = betterproto.message_field(
        1, optional=True, group="_result"
    )
    batch_status: List["BatchStatus"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class BatchStatus(betterproto.Message):
    error_message: Optional[str] = betterproto.string_field(
        1, optional=True, group="_error_message"
    )
    pipeline_module: "PipelineModule" = betterproto.message_field(2)
    module_status: "ModuleStatus" = betterproto.enum_field(3)


@dataclass(eq=False, repr=False)
class PipelineModule(betterproto.Message):
    name: str = betterproto.string_field(1)
    input_datatype: str = betterproto.string_field(2)
    output_datatype: str = betterproto.string_field(3)


class PipelineServerStub(betterproto.ServiceStub):
    async def iterate_config(
        self,
        internal_config: "InternalConfig",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> AsyncIterator["PipelineStatus"]:
        async for response in self._unary_stream(
            "/PipelineServer/IterateConfig",
            internal_config,
            PipelineStatus,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        ):
            yield response


class MaterialServerStub(betterproto.ServiceStub):
    async def upload_material(
        self,
        material_upload_data_iterator: Union[
            AsyncIterable["MaterialUploadData"], Iterable["MaterialUploadData"]
        ],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "Empty":
        return await self._stream_unary(
            "/MaterialServer/UploadMaterial",
            material_upload_data_iterator,
            MaterialUploadData,
            Empty,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def delete_material(
        self,
        string: "String",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "Empty":
        return await self._unary_unary(
            "/MaterialServer/DeleteMaterial",
            string,
            Empty,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_material_hashes(
        self,
        empty: "Empty",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ListOfStrings":
        return await self._unary_unary(
            "/MaterialServer/GetMaterialHashes",
            empty,
            ListOfStrings,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_material_name(
        self,
        string: "String",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "String":
        return await self._unary_unary(
            "/MaterialServer/GetMaterialName",
            string,
            String,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_material(
        self,
        string: "String",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> AsyncIterator["MaterialUploadData"]:
        async for response in self._unary_stream(
            "/MaterialServer/GetMaterial",
            string,
            MaterialUploadData,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        ):
            yield response


class PipelineServerBase(ServiceBase):
    async def iterate_config(
        self, internal_config: "InternalConfig"
    ) -> AsyncIterator["PipelineStatus"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)
        yield PipelineStatus()

    async def __rpc_iterate_config(
        self, stream: "grpclib.server.Stream[InternalConfig, PipelineStatus]"
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.iterate_config,
            stream,
            request,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/PipelineServer/IterateConfig": grpclib.const.Handler(
                self.__rpc_iterate_config,
                grpclib.const.Cardinality.UNARY_STREAM,
                InternalConfig,
                PipelineStatus,
            ),
        }


class MaterialServerBase(ServiceBase):
    async def upload_material(
        self, material_upload_data_iterator: AsyncIterator["MaterialUploadData"]
    ) -> "Empty":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def delete_material(self, string: "String") -> "Empty":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_material_hashes(self, empty: "Empty") -> "ListOfStrings":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_material_name(self, string: "String") -> "String":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_material(
        self, string: "String"
    ) -> AsyncIterator["MaterialUploadData"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)
        yield MaterialUploadData()

    async def __rpc_upload_material(
        self, stream: "grpclib.server.Stream[MaterialUploadData, Empty]"
    ) -> None:
        request = stream.__aiter__()
        response = await self.upload_material(request)
        await stream.send_message(response)

    async def __rpc_delete_material(
        self, stream: "grpclib.server.Stream[String, Empty]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.delete_material(request)
        await stream.send_message(response)

    async def __rpc_get_material_hashes(
        self, stream: "grpclib.server.Stream[Empty, ListOfStrings]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_material_hashes(request)
        await stream.send_message(response)

    async def __rpc_get_material_name(
        self, stream: "grpclib.server.Stream[String, String]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_material_name(request)
        await stream.send_message(response)

    async def __rpc_get_material(
        self, stream: "grpclib.server.Stream[String, MaterialUploadData]"
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.get_material,
            stream,
            request,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/MaterialServer/UploadMaterial": grpclib.const.Handler(
                self.__rpc_upload_material,
                grpclib.const.Cardinality.STREAM_UNARY,
                MaterialUploadData,
                Empty,
            ),
            "/MaterialServer/DeleteMaterial": grpclib.const.Handler(
                self.__rpc_delete_material,
                grpclib.const.Cardinality.UNARY_UNARY,
                String,
                Empty,
            ),
            "/MaterialServer/GetMaterialHashes": grpclib.const.Handler(
                self.__rpc_get_material_hashes,
                grpclib.const.Cardinality.UNARY_UNARY,
                Empty,
                ListOfStrings,
            ),
            "/MaterialServer/GetMaterialName": grpclib.const.Handler(
                self.__rpc_get_material_name,
                grpclib.const.Cardinality.UNARY_UNARY,
                String,
                String,
            ),
            "/MaterialServer/GetMaterial": grpclib.const.Handler(
                self.__rpc_get_material,
                grpclib.const.Cardinality.UNARY_STREAM,
                String,
                MaterialUploadData,
            ),
        }
