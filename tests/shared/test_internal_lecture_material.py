from pathlib import Path
import pytest
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.generated import LectureMaterial


@pytest.fixture(scope="session")
def material() -> InternalLectureMaterial:
    """Pytest fixture of InternalLectureMaterial.

    Returns:
        InternalLectureMaterial
    """
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/plain"
    )
    path = Path(__file__).parent / "example_materials/example.txt"
    material = InternalLectureMaterial(path, material_metadata)
    return material


def test_modification_and_verification(material: InternalLectureMaterial) -> None:
    """Tests recognition of file modification using InternalLectureMaterial.verify_hash().

    Args:
        material (InternalLectureMaterial): Pytest fixture of InternalLectureMaterial.
    """
    hash = material.hash
    path = Path(__file__).parent / "example_materials/modified_example.txt"
    material.local_path = path
    assert material.verify_hash() == False
    material.update_hash()
    assert material.hash != hash


def test_evaluate_mimetype(material: InternalLectureMaterial) -> None:
    """Tests failure of mimetype evaluation using an invalid mimetype.

    Args:
        material (InternalLectureMaterial): Pytest fixture of InternalLectureMaterial.y
    """
    with pytest.raises(Exception):
        material.file_type = "Not a valid mimetype"
        material._evaluate_mimetype()
