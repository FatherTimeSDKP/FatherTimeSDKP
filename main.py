# main.py
from fastapi import FastAPI
from solver.knapsack import solve_knapsack
from networking.sdn_controller import SDNController
from temporal.fathertimes369v import FatherTimes369v
from quantum.qcc_simulator import QCCSimulator

app = FastAPI(title="Unified SDKP Cloud Platform")

# Instantiate Core Framework Components
sdn = SDNController()
scheduler = FatherTimes369v()
quantum_sim = QCCSimulator()

@app.get("/")
def health_check():
    return {"status": "Online", "platform": "SDKP Unified Web Engine"}

@app.post("/solve/knapsack")
def run_knapsack_solver(values: list[float], weights: list[int], capacity: int):
    return solve_knapsack(values, weights, capacity)

@app.post("/networking/sdn/rules")
def add_sdn_rule(rule_id: str, match_ip: str, action: str):
    return sdn.add_flow_rule(rule_id, match_ip, action)

@app.post("/temporal/sync")
def schedule_sync(task_name: str, epoch_time: float):
    return scheduler.schedule_sync_event(task_name, epoch_time)

@app.post("/quantum/measure")
def run_qcc_measurement():
    quantum_sim.apply_hadamard()
    outcome = quantum_sim.measure()
    return {"collapsed_state": outcome}
