import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
c = 299792458  # Speed of light (m/s)
AU = 1.496e11  # Astronomical Unit in meters
Msun = 1.989e30  # Mass of the Sun in kg

# Properties of Alpha Centauri A and B
mass_A = 1.1 * Msun
mass_B = 0.9 * Msun
distance_AB = 23.6 * AU  # Average distance between the two stars
orbital_period_years = 79.91
orbital_period_seconds = orbital_period_years * 365.25 * 24 * 3600

# Orbital velocities (simplified for circular orbit)
velocity_A = np.sqrt(G * (mass_A + mass_B) / distance_AB)
velocity_B = np.sqrt(G * (mass_A + mass_B) / distance_AB)

# Time dilation factor: Δt' = Δt * sqrt(1 - (2GM)/(rc²))
def time_dilation(mass, radius):
    return np.sqrt(1 - (2 * G * mass) / (radius * c**2))

# Kinetic energy: KE = 0.5 * m * v²
def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity**2

# Calculate time dilation and kinetic energy
time_dilated_A = time_dilation(mass_A, distance_AB)
time_dilated_B = time_dilation(mass_B, distance_AB)
energy_A = kinetic_energy(mass_A, velocity_A)
energy_B = kinetic_energy(mass_B, velocity_B)

# Output the calculations
print(f"Time Dilation for Alpha Centauri A: {time_dilated_A}")
print(f"Time Dilation for Alpha Centauri B: {time_dilated_B}")
print(f"Kinetic Energy for Alpha Centauri A: {energy_A:.2e} J")
print(f"Kinetic Energy for Alpha Centauri B: {energy_B:.2e} J")

# Prepare data for visualization
time_steps = np.linspace(0, orbital_period_seconds, 1000)
td_A = time_dilated_A * np.ones_like(time_steps)
td_B = time_dilated_B * np.ones_like(time_steps)
ke_A = energy_A * np.ones_like(time_steps)
ke_B = energy_B * np.ones_like(time_steps)

# Plot results
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(time_steps, td_A, label='Alpha Centauri A', color='red')
plt.plot(time_steps, td_B, label='Alpha Centauri B', color='blue')
plt.title("Time Dilation Over Orbital Period")
plt.xlabel("Time (s)")
plt.ylabel("Time Dilation Factor")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(time_steps, ke_A, label='Alpha Centauri A', color='red')
plt.plot(time_steps, ke_B, label='Alpha Centauri B', color='blue')
plt.title("Kinetic Energy Over Orbital Period")
plt.xlabel("Time (s)")
plt.ylabel("Kinetic Energy (Joules)")
plt.legend()

plt.tight_layout()
plt.show()