from lab_simulation.core.config_loader import load_config

def test_load_rock_analysis_config():
    config = load_config('rock_analysis_configs.txt')
    assert 'lab_config' in config
    assert 'equipment' in config
    assert 'staff' in config
    assert 'workflow_steps' in config
    print('Lab name:', config['lab_config']['name'])
    print('Equipment:', list(config['equipment'].keys()))
    print('Staff:', list(config['staff'].keys()))
    print('Workflow steps:', list(config['workflow_steps'].keys()))
