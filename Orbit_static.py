import matplotlib.pyplot as plt
from Orbit_math import Es_param_find

sat = Es_param_find(400)
path = sat.trajectory(10)
x, y = zip(*path)

earth = plt.Circle((0, 0), sat.R, color="deepskyblue", label="Earth")
fig, ax = plt.subplots()

ax.add_patch(earth)
ax.plot(x, y, color="orange", label="Satellite Orbit")
ax.scatter([x[0]], [y[0]], color="red", label="Satellite")

ax.set_xlabel("X Position (km)")
ax.set_ylabel("Y Position (km)")
ax.set_title("ORBIT-1: Earth and Satellite Orbit")
ax.set_aspect("equal")
ax.grid(True)
ax.legend()
plt.show()
