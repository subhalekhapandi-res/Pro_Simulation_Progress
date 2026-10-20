import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from Orbit_math import Es_param_find
from Config import load_config
from Mission_log import MissionLog
from Event import EventDetector

config = load_config()

sat = Es_param_find(config["altitude_km"])
time_step = config["time_step_seconds"]

log = MissionLog()
log.record("INFO", "Mission started", 0)

events = EventDetector(log)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25, right=0.72)

ax.add_patch(plt.Circle((0, 0), sat.R, color="deepskyblue"))

ax.set_xlim(-sat.orbit_rad * 1.2, sat.orbit_rad * 1.2)
ax.set_ylim(-sat.orbit_rad * 1.2, sat.orbit_rad * 1.2)
ax.set_aspect("equal")
ax.grid(True)
ax.set_xlabel("X Position (km)")
ax.set_ylabel("Y Position (km)")
ax.set_title(f"{config['mission_name']} Mission Simulator")

satellite, = ax.plot([], [], "ro", label="Satellite")
trail, = ax.plot([], [], "orange", label="Orbit Trail")

telemetry = fig.text(0.74, 0.75, "", va="top", family="monospace")

xs, ys = [], []
sim_time = 0
last_completed = 0
previous_status = "NORMAL"

def update(frame):
    global sim_time

    sim_time += time_step

    events.check_orbits(sim_time, sat.orbit_period)

    x, y = sat.simulate(sim_time)
    xs.append(x)
    ys.append(y)

    satellite.set_data([x], [y])
    trail.set_data(xs, ys)

    status = sat.safety_check(
        config["min_altitude_km"],
        config["max_altitude_km"],
        config["min_speed_km_s"],
        config["max_speed_km_s"]
    )

    events.check_safety(status, sim_time)
    log.save()

    completed = sat.completed_orbits(sim_time)

    telemetry.set_text(
        f"TELEMETRY\n\n"
        f"Mission: {config['mission_name']}\n"
        f"Mission Time: {sim_time:.0f} s\n"
        f"Completed Orbits: {completed}\n"
        f"Altitude: {sat.h:.1f} km\n"
        f"Speed: {sat.velocity:.3f} km/s\n"
        f"Period: {sat.orbit_period:.1f} s\n"
        f"X: {x:.2f} km\n"
        f"Y: {y:.2f} km\n"
        f"Status: {status}"
    )

    return satellite, trail, telemetry


ani = FuncAnimation(
    fig,
    update,
    interval=config["animation_interval_ms"],
    blit=False,
    cache_frame_data=False
)

def pause(event):
    ani.pause()

def resume(event):
    ani.resume()


def reset(event):
    global sim_time

    sim_time = 0
    events.reset()

    xs.clear()
    ys.clear()

    satellite.set_data([], [])
    trail.set_data([], [])

    log.record("INFO", "Simulation reset", sim_time)
    log.save()

    telemetry.set_text("TELEMETRY\n\nSimulation reset")
    fig.canvas.draw_idle()


def slower(event):
    global time_step
    time_step = max(1, time_step // 2)

def faster(event):
    global time_step
    time_step *= 2

button_definitions = [
    ("Pause", pause),
    ("Resume", resume),
    ("Reset", reset),
    ("Slower", slower),
    ("Faster", faster)
]

button_objects = []

for i, (label, callback) in enumerate(button_definitions):
    button_ax = plt.axes([0.06 + i * 0.18, 0.08, 0.15, 0.07])
    button = Button(button_ax, label)
    button.on_clicked(callback)
    button_objects.append(button)

plt.show()

log.save()
