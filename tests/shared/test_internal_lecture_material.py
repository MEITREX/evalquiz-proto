from pathlib import Path
import pytest
from shared.internal_lecture_material import InternalLectureMaterial
from shared.generated import LectureMaterial


@pytest.fixture(scope="session")
def material():
    material_metadata = LectureMaterial(
        reference="Example textfile", file_type="text/plain"
    )
    material = InternalLectureMaterial(
        Path("tests/shared/example_materials/example.txt"), material_metadata
    )
    return material


def test_modification_and_verification(material):
    hash = material.hash
    material.local_path = Path("tests/shared/example_materials/modified_example.txt")
    assert material.verify_hash() == False
    material.update_hash()
    assert material.hash != hash


def test_evaluate_mimetype(material):
    with pytest.raises(Exception):
        material._evaluate_mimetype("Not a valid mimetype")
