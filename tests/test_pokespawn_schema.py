import pytest

from gcp_pipeline.models.poke_spawn import PokeSpawn
from gcp_pipeline.simulation import PokeSpawnDataSimulator


def generate_cases():
    return PokeSpawnDataSimulator().generate(1)[0][:10]


@pytest.mark.parametrize("sample", generate_cases())
def test_pokespawn_cases(sample):
    PokeSpawn.model_validate(sample)
