
import os
import tempfile
from Mission_log import MissionLog

with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "test_log.json")

    log = MissionLog()
    log.record("INFO", "Mission started", 0)
    log.save(path)

    restored = MissionLog()
    restored.load(path)

    assert len(restored.events) == 1
    assert restored.events[0]["message"] == "Mission started"

    restored.record("INFO", "Orbit completed", 5500)
    restored.save(path)

    recovered = MissionLog()
    recovered.load(path)

    assert len(recovered.events) == 2
    assert recovered.events[1]["message"] == "Orbit completed"

print("All MissionLog tests passed!")
