from lab_simulation.core.config_loader import load_config
from lab_simulation.resources.equipment import Equipment
from lab_simulation.resources.staff import Staff
from lab_simulation.processes.steps import Step
import simpy


def test_instantiate_resources_and_steps():
    config = load_config('rock_analysis_configs.txt')
    env = simpy.Environment()

    # Instantiate equipment
    equipment_objs = {}
    for key, eq_conf in config['equipment'].items():
        equipment_objs[key] = Equipment(env, eq_conf['name'], eq_conf)
    assert len(equipment_objs) == len(config['equipment'])

    # Instantiate staff
    staff_objs = {}
    for key, st_conf in config['staff'].items():
        staff_objs[key] = Staff(env, st_conf['name'], st_conf)
    assert len(staff_objs) == len(config['staff'])

    # Instantiate steps
    step_objs = {}
    for key, step_conf in config['workflow_steps'].items():
        step_objs[key] = Step(step_conf['name'], step_conf)
    assert len(step_objs) == len(config['workflow_steps'])

    print('Equipment objects:', list(equipment_objs.keys()))
    print('Staff objects:', list(staff_objs.keys()))
    print('Step objects:', list(step_objs.keys()))
