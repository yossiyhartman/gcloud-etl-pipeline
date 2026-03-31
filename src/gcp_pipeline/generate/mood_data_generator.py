import random
from datetime import datetime, timedelta

OutputFmt = list[dict[str, str]]


class MoodDataGenerator:
    moods: list[str] = ["Hungry", "Horny", "Optimistic", "Motivated", "Dreamy"]
    names: list[str] = ["Wilgo", "Draco", "Silvy", "Jonathan", "Aisha"]

    def generate(self, n_records: int) -> OutputFmt:

        event_records: OutputFmt = []

        for name in self.names:
            for idx in range(n_records):
                event_time = (datetime.now() - timedelta(idx)).strftime("%d-%m-%Y")
                todays_mood = random.choice(self.moods)

                record = {
                    "event_time": event_time,
                    "name": name,
                    "mood": todays_mood,
                }

                event_records.append(record)

        return event_records


if __name__ == "__main__":
    from pprint import pprint

    pprint(MoodDataGenerator().generate(5))
