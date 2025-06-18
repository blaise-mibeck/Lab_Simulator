from lab_simulation.core.config_loader import load_config
from lab_simulation.resources.equipment import Equipment
from lab_simulation.resources.staff import Staff
from lab_simulation.processes.steps import Step
from lab_simulation.core.process_runner import run_step
import simpy
import json


def test_basic_workflow_execution():
    config = load_config('rock_analysis_configs.txt')
    env = simpy.Environment()
    # Instantiate resources
    equipment_objs = {k: Equipment(env, v['name'], v) for k, v in config['equipment'].items()}
    staff_objs = {k: Staff(env, v['name'], v) for k, v in config['staff'].items()}
    step_objs = {k: Step(v['name'], v) for k, v in config['workflow_steps'].items()}
    # Simulate first three steps for 10 samples
    sample_count = 10
    metrics = []
    def process():
        yield from run_step(env, step_objs['sample_receipt'], equipment_objs, staff_objs, sample_count, metrics)
        yield from run_step(env, step_objs['rock_cutting'], equipment_objs, staff_objs, sample_count, metrics)
        yield from run_step(env, step_objs['micronization'], equipment_objs, staff_objs, sample_count, metrics)
    env.process(process())
    env.run()
    print('Workflow execution completed. Simulated time:', env.now)
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
