
from Event import EventDetector
from Mission_log import MissionLog

log = MissionLog()
events = EventDetector(log)

T = 5500

events.check_orbits(0, T)
assert len(log.events) == 0

events.check_orbits(T, T)
assert len(log.events) == 1
assert log.events[0]["message"] == "Orbit 1 completed"

events.check_orbits(T, T)
assert len(log.events) == 1

events.check_orbits(3 * T, T)
assert len(log.events) == 3

events.check_safety("NORMAL", 0)
events.check_safety("SPEED WARNING", 100)
assert log.events[-1]["type"] == "WARNING"

events.check_safety("SPEED WARNING", 110)
assert len([e for e in log.events if e["type"] == "WARNING"]) == 1

events.check_safety("NORMAL", 120)
assert log.events[-1]["message"] == "Safety status returned to NORMAL"

events.reset()
events.check_orbits(T, T)
assert events.last_completed == 1

print("All EventDetector tests passed!")
