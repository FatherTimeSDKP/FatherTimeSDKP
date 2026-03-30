import numpy as np

class SharonCare1Sim:
    def __init__(self):
        # Physical Constants
        self.num_magnets_outer = 12
        self.num_magnets_inner = 6
        self.shield_thickness_cm = 3.0
        self.magnet_volume_in3 = 24 * 9 * 6
        
        # Conductivity Factors
        self.silver_lining_efficiency = 0.98  # Silver-lined copper capture
        self.shielding_effectiveness = 0.991 # 3cm stainless steel dampening of positive pole

    def calculate_flux_density(self, barren_gap_mm):
        """Calculates flux based on the proximity of the cylinders."""
        # Inverse square law for magnetic repulsion in the Barrens
        base_repulsion = (self.magnet_volume_in3 / (barren_gap_mm**2))
        effective_thrust = base_repulsion * self.shielding_effectiveness
        return effective_thrust

    def energy_harvest(self, rpm, barren_gap_mm):
        """Calculates electricity generated for Super Capacitors."""
        flux = self.calculate_flux_density(barren_gap_mm)
        # Silver-lined housing converts flux to voltage
        voltage_out = flux * rpm * self.silver_lining_efficiency
        return voltage_out

# Example Run: High Torque (Narrow Barrens)
sim = SharonCare1Sim()
print(f"Energy Output at 5mm Gap: {sim.energy_harvest(3000, 5):.2f} Volts")

class MotorController:
    def __init__(self):
        self.lever_position = 0.0  # 0 to 100 (100 is max proximity)
        self.shelf_angle = 0.0     # Degrees of adjustment
        self.capacitor_charge = 0.0
        self.battery_level = 100.0

    def adjust_lever(self, target_thrust):
        """Moves the inner cylinder closer or farther in the Barrens."""
        if target_thrust > 80:
            self.lever_position = 95.0 # Max torque for plasma kick
        else:
            self.lever_position = 40.0 # Cruise speed
        return self.lever_position

    def dynamic_shelf_sync(self, current_rpm):
        """Adjusts 3cm shelves after startup to maintain 100% shielding."""
        if current_rpm > 1000:
            self.shelf_angle = 5.5 # Fine-tune for high-speed flux expansion
        else:
            self.shelf_angle = 0.0
        return self.shelf_angle

    def power_distribution(self, generated_power):
        """Directs harvest to Super Capacitors and Deep Cycle Batteries."""
        # 80% to Capacitors for Plasma, 20% to Batteries for system health
        cap_feed = generated_power * 0.8
        bat_feed = generated_power * 0.2
        self.capacitor_charge += cap_feed
        self.battery_level += bat_feed
        print(f"Capacitors Fed: {cap_feed} units | Battery Reserving: {bat_feed} units")
