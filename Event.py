
class EventDetector:
    def __init__(self, log):
        self.log = log
        self.last_completed = 0
        self.previous_status = "NORMAL"

    def check_orbits(self, sim_time, orbit_period):
        completed = int(sim_time // orbit_period)

        if completed > self.last_completed:
            for orbit in range(self.last_completed + 1, completed + 1):
                self.log.record(
                    "INFO",
                    f"Orbit {orbit} completed",
                    orbit * orbit_period
                )

        self.last_completed = completed

    def check_safety(self, status, sim_time):
        if status != self.previous_status:
            if status != "NORMAL":
                self.log.record("WARNING", status, sim_time)
            elif self.previous_status != "NORMAL":
                self.log.record(
                    "INFO",
                    "Safety status returned to NORMAL",
                    sim_time
                )

            self.previous_status = status

    def reset(self):
        self.last_completed = 0
        self.previous_status = "NORMAL"
