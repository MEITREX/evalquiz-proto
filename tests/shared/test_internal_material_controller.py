from typing import List, Tuple
import pytest
from blake3 import blake3
from pathlib import Path
from evalquiz_proto.shared.generated import LectureMaterial
from evalquiz_proto.shared.internal_material_controller import (
    InternalMaterialController,
)


@pytest.fixture(scope="session")
def im_controller() -> InternalMaterialController:
    """Pytest fixture of InternalMaterialController.

    Returns:
        InternalMaterialController
    """
    im_controller = InternalMaterialController()
    return im_controller


@pytest.fixture(scope="session")
def paths_and_lecture_materials() -> List[Tuple[Path, LectureMaterial]]:
    """Pytest fixture of list of parameters for loading InternalLectureMaterials.

    Returns:
        List[Tuple[Path, LectureMaterial]]: Represents two parameter configurations.
    """
    return [
        (
            Path(__file__).parent / "example_materials/example.txt",
            LectureMaterial(
                reference="Example textfile",
                hash="f9f75c3c05c99d69364ae75e028c997fb1a8c209e03a6452efbef6b75784c3ab",
                file_type="text/plain",
            ),
        ),
        (
            Path(__file__).parent / "example_materials/modified_example.txt",
            LectureMaterial(
                reference="Modified example textfile",
                hash="068aee4ee49d6cabb1576286108939205260d07cadeaaa249b352487bfe4bc3d",
                file_type="text/plain",
            ),
        ),
    ]


def test_load_material(
    im_controller: InternalMaterialController,
    paths_and_lecture_materials: List[Tuple[Path, LectureMaterial]],
) -> None:
    """Tests loading a lecture material into a InternalMaterialController.

    Args:
        im_controller (InternalMaterialController): Pytest fixture of InternalMaterialController
        paths_and_lecture_materials (List[Tuple[Path, LectureMaterial]]): Pytest fixture of parameter configurations.
    """
    (material_path, material_metadata) = paths_and_lecture_materials[0]
    im_controller.load_material(material_path, material_metadata)
    assert len(im_controller.internal_lecture_materials) != 0
    lecture_material = list(im_controller.internal_lecture_materials.values())[0]
    hash = lecture_material.hash
    assert hash in im_controller.internal_lecture_materials.keys()
    assert lecture_material.reference == "Example textfile"


def test_unload_material(
    im_controller: InternalMaterialController,
    paths_and_lecture_materials: List[Tuple[Path, LectureMaterial]],
) -> None:
    """Tests unloading a lecture material from a InternalMaterialController.

    Args:
        im_controller (InternalMaterialController): Pytest fixture of InternalMaterialController
        paths_and_lecture_materials (List[Tuple[Path, LectureMaterial]]): Pytest fixture of parameter configurations.
    """
    (material_path, material_metadata) = paths_and_lecture_materials[0]
    im_controller.load_material(material_path, material_metadata)
    lecture_material = list(im_controller.internal_lecture_materials.values())[0]
    hash = lecture_material.hash
    im_controller.unload_material(hash)
    assert hash not in im_controller.internal_lecture_materials.keys()


def test_get_material_hashes(
    im_controller: InternalMaterialController,
    paths_and_lecture_materials: List[Tuple[Path, LectureMaterial]],
) -> None:
    """Tests retrieving all material hashes from an InternalMaterialController.

    Args:
        im_controller (InternalMaterialController): Pytest fixture of InternalMaterialController
        paths_and_lecture_materials (List[Tuple[Path, LectureMaterial]]): Pytest fixture of parameter configurations.
    """
    (material_path, material_metadata) = paths_and_lecture_materials[0]
    im_controller.load_material(material_path, material_metadata)
    (material_path, material_metadata) = paths_and_lecture_materials[1]
    im_controller.load_material(material_path, material_metadata)
    material_hashes = im_controller.get_material_hashes()
    assert len(material_hashes) == 2
    with open(material_path, "r") as local_file:
        file_content = local_file.read()
    hash = blake3(file_content.encode("utf-8")).hexdigest()
    assert hash in material_hashes


def test_serialization_and_deserialization_with_config(
    im_controller: InternalMaterialController,
    paths_and_lecture_materials: List[Tuple[Path, LectureMaterial]],
) -> None:
    """Tests saving InternalMaterialController state to file by serialization and deserialization.

    Args:
        im_controller (InternalMaterialController): Pytest fixture of InternalMaterialController
        paths_and_lecture_materials (List[Tuple[Path, LectureMaterial]]): Pytest fixture of parameter configurations.
    """
    config_path = Path(__file__).parent / "test_config.json"
    im_controller.load_material(*paths_and_lecture_materials[0])
    im_controller.load_material(*paths_and_lecture_materials[1])
    im_controller.config_path = config_path
    im_controller.serialize_to_config()
    new_im_controller = InternalMaterialController(config_path)
    assert new_im_controller.get_material_hashes() == [
        path_and_lecture_material[1].hash
        for path_and_lecture_material in paths_and_lecture_materials
    ]
