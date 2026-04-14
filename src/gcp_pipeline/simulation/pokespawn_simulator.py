import random
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from typing import Any

from localdex import LocalDex

Record = dict[str, Any]
Records = list[list[Record]]

pokedex = LocalDex()
LOCATIONS = ["Amsterdam", "Rotterdam", "Utrecht", "Groningen", "Den Haag", "Zutphen", "Urk"]


class PokeSpawnDataSimulator:
    """"""

    def generate(self, n_days: int) -> Records:
        """"""
        today = datetime.now(timezone.utc)

        records: Records = []

        for idx in range(n_days):
            today_records = []
            day = today - timedelta(idx)
            n_events = random.randint(20, 100)

            for _ in range(n_events):
                pokemon = pokedex.get_pokemon_by_id(random.randint(1, 1000))
                spawn_time = day + timedelta(seconds=random.randint(100, 40000))

                record: Record = {
                    "date": str(spawn_time.date()),
                    "time": str(spawn_time.time()),
                    "location": random.choice(LOCATIONS),
                    "pokemon": {
                        "id": pokemon.id,
                        "name": pokemon.name,
                        "weight": pokemon.weight,
                        "height": pokemon.height,
                        "evo_condition": pokemon.evo_condition,
                        "evo_level": pokemon.evo_level,
                        "types": pokemon.types,
                        "generation": pokemon.generation,
                        "evolutions": pokemon.evolutions,
                        "stats": {k: v for k, v in asdict(pokemon.base_stats).items()},
                        "moves": pokemon.moves,
                    },
                }

                today_records.append(record)
            records.append(today_records)
        return records


if __name__ == "__main__":
    from pprint import pprint

    pprint(PokeSpawnDataSimulator().generate(1))
