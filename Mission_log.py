
import json
from datetime import datetime
from pathlib import Path


class MissionLog:
    def __init__(self):
        self.events = []

    def record(self, event_type, message, sim_time):
        event = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "sim_time": sim_time,
            "type": event_type,
            "message": message
        }

        self.events.append(event)
        return event

    def show(self):
        for event in self.events:
            print(
                f"[{event['type']}] "
                f"T+{event['sim_time']:.1f}s | "
                f"{event['message']}"
            )

    def save(self, filename="mission_log.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.events, file, indent=4)

    def load(self, filename="mission_log.json"):
        path = Path(filename)

        if not path.exists():
            self.events = []
            return

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Invalid mission log format")

        self.events = data
