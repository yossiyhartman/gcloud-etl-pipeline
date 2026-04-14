import random
from datetime import datetime, timedelta, timezone
from typing import Any

Record = dict[str, Any]
Records = list[list[Record]]

NAMES = ["Wilgo", "Draco", "Silvy", "Jonathan", "Aisha"]
MOODS = ["Hungry", "Horny", "Optimistic", "Motivated", "Dreamy"]


class MoodDataSimulator:
    def generate(self, n_days: int) -> Records:

        today = datetime.now(timezone.utc).date()

        records: Records = []

        for idx in range(n_days):
            today_records = []
            day = today - timedelta(idx)

            for name in NAMES:
                todays_mood = random.choice(MOODS)

                record: Record = {
                    "date": str(day),
                    "name": name,
                    "mood": todays_mood,
                }

                today_records.append(record)
            records.append(today_records)
        return records


if __name__ == "__main__":
    from pprint import pprint

    pprint(MoodDataSimulator().generate(1))
