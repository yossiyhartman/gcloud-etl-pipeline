import random
from datetime import datetime, timedelta

OutputFmt = list[dict[str, list[dict[str, str]]]]


class MoodDataGenerator:
    moods: list[str] = ["Hungry", "Horny", "Optimistic", "Motivated", "Dreamy"]
    names: list[str] = ["Wilgo", "Draco", "Silvy", "Jonathan", "Aisha"]

    def generate(self, n_days: int) -> OutputFmt:

        event_records: OutputFmt = []

        for idx in range(n_days):
            event_time = (datetime.now() - timedelta(idx)).strftime("%Y-%m-%d")
            day = {event_time: []}

            for name in self.names:
                todays_mood = random.choice(self.moods)

                record = {
                    "event_time": event_time,
                    "name": name,
                    "mood": todays_mood,
                }

                day[event_time].append(record)

            # Append the day
            event_records.append(day)

        return event_records


if __name__ == "__main__":
    from pprint import pprint

    pprint(MoodDataGenerator().generate(5))
