from pathlib import Path
import pytest
from evalquiz_proto.shared.exceptions import MimetypeMismatchException
from evalquiz_proto.shared.internal_lecture_material import InternalLectureMaterial
from evalquiz_proto.shared.generated import LectureMaterial


@pytest.fixture(scope="session")
def internal_lecture_material() -> InternalLectureMaterial:
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


def test_modification_and_verification(
    internal_lecture_material: InternalLectureMaterial,
) -> None:
    """Tests recognition of file modification using InternalLectureMaterial.verify_hash().

    Args:
        internal_lecture_material (InternalLectureMaterial): Pytest fixture of InternalLectureMaterial.
    """
    hash = internal_lecture_material.hash
    path = Path(__file__).parent / "example_materials/modified_example.txt"
    internal_lecture_material.local_path = path
    assert internal_lecture_material.verify_hash() == False
    internal_lecture_material.update_hash()
    assert internal_lecture_material.hash != hash


def test_evaluate_mimetype(internal_lecture_material: InternalLectureMaterial) -> None:
    """Tests failure of mimetype evaluation using an invalid mimetype.

    Args:
        internal_lecture_material (InternalLectureMaterial): Pytest fixture of InternalLectureMaterial.
    """
    with pytest.raises(MimetypeMismatchException):
        internal_lecture_material.file_type = "Not a valid mimetype"
        internal_lecture_material._evaluate_mimetype()
