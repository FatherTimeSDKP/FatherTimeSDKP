import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# SHARONCARE1 MOTOR PARAMETERS
# -----------------------------

# Rotor properties
rotor_mass = 2.0          # kg
rotor_radius = 0.15       # meters
initial_rpm = 500
magnetic_force = 25       # Newtons (effective flux force)

# Bearing properties
friction_coefficient = 0.002   # low friction (bismuth/tin idea)
load_force = rotor_mass * 9.81

# Simulation time
time_step = 0.01
duration = 10
time = np.arange(0, duration, time_step)

# -----------------------------
# CALCULATIONS
# -----------------------------

# Convert RPM to rad/s
omega = initial_rpm * 2 * np.pi / 60

# Moment of inertia (solid disk)
I = 0.5 * rotor_mass * rotor_radius**2

angular_velocity = []
torque_values = []
energy_values = []

for t in time:

    # Magnetic torque
    magnetic_torque = magnetic_force * rotor_radius

    # Friction torque
    friction_torque = friction_coefficient * load_force * rotor_radius

    # Net torque
    net_torque = magnetic_torque - friction_torque

    # Angular acceleration
    alpha = net_torque / I

    # Update velocity
    omega = omega + alpha * time_step

    # Rotational energy
    energy = 0.5 * I * omega**2

    angular_velocity.append(omega)
    torque_values.append(net_torque)
    energy_values.append(energy)

# -----------------------------
# RESULTS
# -----------------------------

rpm_values = np.array(angular_velocity) * 60 / (2*np.pi)

print("Final RPM:", rpm_values[-1])
print("Final Energy (J):", energy_values[-1])

# -----------------------------
# PLOTS
# -----------------------------

plt.figure()
plt.plot(time, rpm_values)
plt.title("Rotor Speed vs Time")
plt.xlabel("Time (s)")
plt.ylabel("RPM")
plt.show()

plt.figure()
plt.plot(time, energy_values)
plt.title("Rotational Energy vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Energy (J)")
plt.show()

plt.figure()
plt.plot(time, torque_values)
plt.title("Torque vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Torque (Nm)")
plt.show()
