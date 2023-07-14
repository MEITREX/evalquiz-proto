import pytest
from shared.internal_lecture_material import InternalLectureMaterial
from shared.generated import LectureMaterial

"""
@pytest.fixture(scope="session")
def il_material():
    il_material = InternalLectureMaterial()
    return il_material
"""


def test_init_internal_lecture_material():
    material_metadata = LectureMaterial(reference="Example textfile", url=None, hash="asdfjkl", file_type="text/plain", page_filter=None)
    material = InternalLectureMaterial("tests/shared/example_materials/example.txt", material_metadata)