import random
from datetime import datetime, timedelta


class DataGenerator:
    def __init__(self) -> None:
        self.moods = ["Hungry", "Horny", "Optimistic", "Motivated", "Dreamy"]
        self.names = ["Wilgo", "Draco", "Silvy"]

    def generate(self, n_records: int) -> dict[str, list[str]]:

        data = {
            "event_time": [],
            "name": [],
            "mood": [],
        }

        for name in self.names:
            for idx in range(n_records):
                event_time = (datetime.now() - timedelta(idx)).strftime("%d-%m-%Y")
                todays_mood = random.choice(self.moods)

                data["event_time"].append(event_time)
                data["name"].append(name)
                data["mood"].append(todays_mood)

        return data


if __name__ == "__main__":
    print(DataGenerator().generate(5))
