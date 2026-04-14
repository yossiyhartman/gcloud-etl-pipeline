import polars as pl
import pydantic
from poldantic.infer_polars import to_polars_schema

from gcp_pipeline.models.poke_spawn import PokeSpawn
from gcp_pipeline.simulation import PokeSpawnDataSimulator

data = PokeSpawnDataSimulator().generate(1)[0]

df = pl.DataFrame(data)

df.show()


schema = pl.Schema(to_polars_schema(PokeSpawn))

df.cast(schema)
print(schema)
