import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import NamedTuple

# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class MotorConfig:
    # Rotor
    rotor_mass:           float = 2.0      # kg
    rotor_radius:         float = 0.15     # m
    rotor_type:           str   = "disk"   # "disk" or "ring"

    # Magnetic / electrical
    magnetic_force:       float = 25.0     # N  (effective flux force at stall)

    # Bearing / friction
    friction_coefficient: float = 0.002
    bearing_type:         str   = "standard"  # reserved for future loss models

    # Speed limits
    initial_rpm:          float = 500.0
    max_rpm:              float = 10_000.0

    # Simulation
    time_step:            float = 0.01     # s
    duration:             float = 10.0    # s
    integrator:           str   = "rk2"   # "euler" or "rk2"

    # Derived (auto-filled after init)
    I:                    float = field(init=False)
    omega_0:              float = field(init=False)
    omega_max:            float = field(init=False)
    stall_torque:         float = field(init=False)
    friction_torque:      float = field(init=False)
    omega_eq:             float = field(init=False)

    def __post_init__(self):
        if self.rotor_type == "disk":
            self.I = 0.5 * self.rotor_mass * self.rotor_radius ** 2
        elif self.rotor_type == "ring":
            self.I = self.rotor_mass * self.rotor_radius ** 2
        else:
            raise ValueError(f"Unknown rotor_type '{self.rotor_type}'. Use 'disk' or 'ring'.")

        self.omega_0        = self.initial_rpm * 2 * np.pi / 60
        self.omega_max      = self.max_rpm     * 2 * np.pi / 60
        self.stall_torque   = self.magnetic_force * self.rotor_radius
        self.friction_torque = (self.friction_coefficient
                                * self.rotor_mass * 9.81
                                * self.rotor_radius)

        if self.stall_torque <= self.friction_torque:
            raise ValueError(
                f"Stall torque ({self.stall_torque:.4f} Nm) ≤ friction torque "
                f"({self.friction_torque:.4f} Nm). Motor cannot spin up."
            )

        # Analytical equilibrium: T_mag*(1 - w/w_max) = T_friction
        self.omega_eq = self.omega_max * (
            1.0 - self.friction_torque / self.stall_torque
        )

# ============================================================
# PHYSICS
# ============================================================

def torque(omega: float, cfg: MotorConfig) -> float:
    """
    Net torque at a given angular velocity.
    Magnetic torque uses a linear torque-speed curve (DC motor approximation).
    Friction is constant (Coulomb model).
    """
    speed_ratio     = np.clip(omega / cfg.omega_max, 0.0, 1.0)
    magnetic_torque = cfg.stall_torque * (1.0 - speed_ratio)
    return magnetic_torque - cfg.friction_torque


def alpha(omega: float, cfg: MotorConfig) -> float:
    """Angular acceleration at a given angular velocity."""
    return torque(omega, cfg) / cfg.I


def step_euler(omega: float, cfg: MotorConfig) -> float:
    return omega + alpha(omega, cfg) * cfg.time_step


def step_rk2(omega: float, cfg: MotorConfig) -> float:
    """Midpoint (RK2) integrator — halves truncation error vs Euler."""
    k1 = alpha(omega, cfg)
    k2 = alpha(omega + 0.5 * k1 * cfg.time_step, cfg)
    return omega + k2 * cfg.time_step

# ============================================================
# SIMULATION
# ============================================================

class SimResults(NamedTuple):
    time:       np.ndarray
    omega:      np.ndarray
    rpm:        np.ndarray
    torque:     np.ndarray
    energy:     np.ndarray
    power:      np.ndarray
    cfg:        MotorConfig


def run_simulation(cfg: MotorConfig) -> SimResults:
    time = np.arange(0, cfg.duration, cfg.time_step)
    n    = len(time)

    integrator = {"euler": step_euler, "rk2": step_rk2}.get(cfg.integrator)
    if integrator is None:
        raise ValueError(f"Unknown integrator '{cfg.integrator}'. Use 'euler' or 'rk2'.")

    omega_arr = np.empty(n)
    omega_arr[0] = cfg.omega_0

    for i in range(1, n):
        omega_new      = integrator(omega_arr[i - 1], cfg)
        omega_arr[i]   = np.clip(omega_new, 0.0, cfg.omega_max)

    torque_arr = np.vectorize(torque)(omega_arr, cfg)
    rpm_arr    = omega_arr * 60 / (2 * np.pi)
    energy_arr = 0.5 * cfg.I * omega_arr ** 2
    power_arr  = np.gradient(energy_arr, cfg.time_step)

    return SimResults(time, omega_arr, rpm_arr, torque_arr, energy_arr, power_arr, cfg)


# ============================================================
# REPORTING
# ============================================================

def print_summary(r: SimResults):
    cfg         = r.cfg
    rpm_eq      = cfg.omega_eq * 60 / (2 * np.pi)
    rpm_error   = abs(r.rpm[-1] - rpm_eq)

    print("\n╔══════════════════════════════════════════════╗")
    print("║       SHARONCARE1 MOTOR SIMULATION           ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Rotor type          : {cfg.rotor_type:<21}║")
    print(f"║  Moment of inertia   : {cfg.I:<18.5f} kg·m² ║")
    print(f"║  Stall torque        : {cfg.stall_torque:<18.4f} Nm   ║")
    print(f"║  Friction torque     : {cfg.friction_torque:<18.4f} Nm   ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Initial RPM         : {cfg.initial_rpm:<21.1f}║")
    print(f"║  Simulated final RPM : {r.rpm[-1]:<21.1f}║")
    print(f"║  Theoretical eq. RPM : {rpm_eq:<21.1f}║")
    print(f"║  Steady-state error  : {rpm_error:<18.3f} RPM  ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Final energy        : {r.energy[-1]:<18.2f} J    ║")
    print(f"║  Peak power          : {r.power.max():<18.2f} W    ║")
    print(f"║  Integrator          : {cfg.integrator:<21}║")
    print(f"║  Steps               : {len(r.time):<21}║")
    print("╚══════════════════════════════════════════════╝\n")


# ============================================================
# PLOTTING
# ============================================================

def plot_results(r: SimResults):
    rpm_eq = r.cfg.omega_eq * 60 / (2 * np.pi)

    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("SHARONCARE1 Motor Simulation", fontsize=15, fontweight="bold")

    panels = [
        (axes[0, 0], r.rpm,    "Rotor Speed",        "RPM",        "steelblue"),
        (axes[0, 1], r.energy, "Rotational Energy",  "Energy (J)", "darkorange"),
        (axes[1, 0], r.torque, "Net Torque",         "Torque (Nm)","seagreen"),
        (axes[1, 1], r.power,  "Power Output",       "Power (W)",  "crimson"),
    ]

    for ax, data, title, ylabel, color in panels:
        ax.plot(r.time, data, color=color, linewidth=1.8)
        ax.set_title(title, fontweight="bold")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    # Overlay theoretical steady-state RPM line
    axes[0, 0].axhline(rpm_eq, color="steelblue", linestyle=":", linewidth=1.4,
                        label=f"Eq. RPM = {rpm_eq:.0f}")
    axes[0, 0].legend(fontsize=9)

    # Overlay zero-torque line
    axes[1, 0].axhline(0, color="seagreen", linestyle=":", linewidth=1.2)

    plt.tight_layout()
    plt.show()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    cfg     = MotorConfig()
    results = run_simulation(cfg)
    print_summary(results)
    plot_results(results)
