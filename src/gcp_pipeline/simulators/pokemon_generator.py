import random
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from typing import Any

from localdex import LocalDex

Record = dict[str, Any]
Records = list[Record]

pokedex = LocalDex()
LOCATIONS = ["Amsterdam", "Rotterdam", "Utrecht", "Groningen", "Den Haag", "Zutphen", "Urk"]


class PokeSpawnDataGenerator:
    def generate(self, n_days: int) -> Records:

        today = datetime.now(timezone.utc)

        records: Records = []

        for idx in range(n_days):
            day = today - timedelta(idx)
            n_events = random.randint(20, 100)

            for _ in range(n_events):
                pokemon = pokedex.get_pokemon_by_id(random.randint(1, 1000))
                spawn_time = day + timedelta(seconds=random.randint(100, 40000))

                record: Record = {
                    "date": spawn_time.date(),
                    "time": spawn_time.time(),
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
                        "abilities": pokemon.abilities,
                        "moves": pokemon.moves,
                    },
                }

                records.append(record)

        return records


if __name__ == "__main__":
    from pprint import pprint

    pprint(PokeSpawnDataGenerator().generate(1))
