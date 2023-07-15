import pytest
from blake3 import blake3
from pathlib import Path
from evalquiz_proto.shared.generated import LectureMaterial
from evalquiz_proto.shared.internal_material_controller import InternalMaterialController


@pytest.fixture(scope="session")
def im_controller() -> InternalMaterialController:
    im_controller = InternalMaterialController()
    return im_controller


def test_load_material(im_controller: InternalMaterialController) -> None:
    material_path = Path("tests/shared/example_materials/example.txt")
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/plain"
    )
    im_controller.load_material(material_path, material_metadata)
    assert len(im_controller.internal_lecture_materials) != 0
    lecture_material = list(im_controller.internal_lecture_materials.values())[0]
    hash = lecture_material.hash
    assert hash in im_controller.internal_lecture_materials.keys()
    assert lecture_material.reference == "Example textfile"


def test_unload_material(im_controller: InternalMaterialController) -> None:
    material_path = Path("tests/shared/example_materials/example.txt")
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/plain"
    )
    im_controller.load_material(material_path, material_metadata)
    lecture_material = list(im_controller.internal_lecture_materials.values())[0]
    hash = lecture_material.hash
    im_controller.unload_material(hash)
    assert hash not in im_controller.internal_lecture_materials.keys()


def test_get_material_hashes(im_controller: InternalMaterialController) -> None:
    material_path = Path("tests/shared/example_materials/example.txt")
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/plain"
    )
    im_controller.load_material(material_path, material_metadata)
    material_path = Path("tests/shared/example_materials/modified_example.txt")
    material_metadata = LectureMaterial(
        reference="Modified example textfile", file_type="text/plain"
    )
    im_controller.load_material(material_path, material_metadata)
    material_hashes = im_controller.get_material_hashes()
    assert len(material_hashes) == 2
    with open(material_path, "r") as local_file:
        file_content = local_file.read()
    hash = blake3(file_content.encode("utf-8")).hexdigest()
    assert hash in material_hashes
