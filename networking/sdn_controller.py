class SDNController:
    """
    Manages Software Defined Networking & Routing (SD&N) configurations.
    """
    def __init__(self):
        self.flow_table = {}

    def add_flow_rule(self, rule_id: str, match_ip: str, action: str) -> dict:
        self.flow_table[rule_id] = {"match": match_ip, "action": action}
        return {"status": "Success", "rule_added": rule_id}

    def route_packet(self, destination_ip: str) -> str:
        for rule, details in self.flow_table.items():
            if details["match"] == destination_ip:
                return f"Routing packet via rule {rule} -> {details['action']}"
        return "Default Route: Dropping packet"
