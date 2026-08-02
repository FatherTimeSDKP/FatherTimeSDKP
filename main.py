from fastapi import FastAPI
from solver.knapsack import solve_knapsack
from networking.sdn_controller import SDNController
from virtualization.vfe_engine import VFEEngine
from temporal.fathertimes369v import FatherTimes369v
from quantum.qcc_simulator import QCCSimulator

app = FastAPI(title="FatherTimeSDKP Unified Cloud Service")

# Initialize module controllers
sdn = SDNController()
vfe = VFEEngine()
fathertime = FatherTimes369v()
qcc = QCCSimulator()

@app.get("/")
def home():
    return {"status": "Active", "framework": "FatherTimeSDKP Unified Platform"}

@app.post("/solve/knapsack")
def solve_kp(values: list[float], weights: list[int], capacity: int):
    return solve_knapsack(values, weights, capacity)

@app.post("/networking/sdn")
def config_sdn(rule_id: str, match_ip: str, action: str):
    return sdn.add_flow_rule(rule_id, match_ip, action)

@app.post("/virtualization/provision")
def config_vfe(vm_id: str, cpu: int, ram: int):
    return vfe.provision_virtual_resource(vm_id, cpu, ram)

@app.post("/temporal/sync")
def log_time(epoch: float):
    return fathertime.log_sync_checkpoint(epoch)

@app.get("/quantum/superposition")
def run_quantum():
    return {"state_vector": qcc.apply_superposition()}
