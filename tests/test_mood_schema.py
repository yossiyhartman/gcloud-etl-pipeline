import pytest

from gcp_pipeline.models.mood import Mood
from gcp_pipeline.simulation import MoodDataSimulator


def generate_cases():
    return MoodDataSimulator().generate(1)[0]


@pytest.mark.parametrize("sample", generate_cases())
def test_pokespawn_cases(sample):
    Mood.model_validate(sample)
