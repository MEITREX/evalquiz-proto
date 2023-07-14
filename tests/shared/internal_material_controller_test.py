import pytest
from shared.internal_lecture_material import InternalLectureMaterial


@pytest.fixture(scope="session")
def il_material():
    il_material = InternalLectureMaterial()
    return il_material
