class PowerDistributor:
    def __init__(self):
        # Storage Reservoirs
        self.super_capacitors_joules = 0.0
        self.deep_cycle_batteries_pct = 85.0  # Medical/Life Support reserve
        
        # System Thresholds
        self.plasma_ignition_threshold = 1000000 # 1 Megajoule for thrust
        self.critical_life_support_level = 20.0  # Priority shift trigger

    def distribute_harvest(self, total_wattage_input):
        """Routes flux energy based on priority."""
        
        # 1. Healthcare/Life Support Priority
        # If batteries are low, the housing redirects all flux to medical
        if self.deep_cycle_batteries_pct < self.critical_life_support_level:
            medical_draw = total_wattage_input * 1.0  # 100% to survival
            plasma_draw = 0.0
            print("CRITICAL: Redirecting all flux to Life Support.")
        else:
            # Standard Operating Procedure (SOP)
            # 70% to Super Capacitors (Movement), 30% to Deep Cycle (Environment)
            plasma_draw = total_wattage_input * 0.70
            medical_draw = total_wattage_input * 0.30

        # 2. Charge the Super Capacitors
        # Designed for high-speed discharge into plasma nozzles
        self.super_capacitors_joules += plasma_draw
        
        # 3. Condition the Deep Cycle Batteries
        # Designed for long-term stability of the atmospheric scrubbers
        self.deep_cycle_batteries_pct += (medical_draw / 5000) # Simplified charge rate
        if self.deep_cycle_batteries_pct > 100: self.deep_cycle_batteries_pct = 100

        return {
            "Capacitor_J": self.super_capacitors_joules,
            "Battery_Pct": self.deep_cycle_batteries_pct
        }

    def fire_plasma_thruster(self):
        """Dumps capacitor energy for propulsion."""
        if self.super_capacitors_joules >= self.plasma_ignition_threshold:
            print("THRUST ACTIVATED: Plasma ignition sequence complete.")
            self.super_capacitors_joules -= self.plasma_ignition_threshold
        else:
            print("CHARGING: Capacitors haven't hit flux threshold yet.")

# Example Run
distro = PowerDistributor()
current_status = distro.distribute_harvest(500000) # Input 500kW from housing
print(f"Status: {current_status}")
distro.fire_plasma_thruster()
