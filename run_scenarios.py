import yaml
import csv
import datetime
from lab_simulation.core.lab_calendar import LabCalendar
from lab_simulation.core.simulation_calendar import LabSimulationWithCalendar
from run_burn_plots import summarize_completion

def run_scenarios(scenarios_file='scenarios.yaml', sim_config_file='sim_config.yaml'):
    with open(sim_config_file, 'r') as f:
        sim_config = yaml.safe_load(f)
    workflow_file = sim_config.get('workflow_file', 'Rock_Workflow_CLEAN.csv')
    lab_config_file = sim_config.get('lab_config_file', 'lab_config.yaml')
    with open(workflow_file, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        workflow_steps = [row for row in reader]
    with open(lab_config_file, 'r') as f:
        lab_config = yaml.safe_load(f)
    with open(scenarios_file, 'r') as f:
        scenarios = yaml.safe_load(f)['scenarios']
    results = []
    for scenario in scenarios:
        staff = scenario['staff']
        sample_count = scenario.get('samples', sim_config.get('samples', 100))
        start_date = datetime.datetime.strptime(scenario.get('start_date', sim_config.get('start_date', '2025-06-18 09:00')), '%Y-%m-%d %H:%M')
        batching = scenario.get('batching', sim_config.get('batching', {}))
        sim = LabSimulationWithCalendar(
            calendar=LabCalendar(country='US', work_hours_per_day=7),
            n_tech=staff['tech'],
            n_sci=staff['sci'],
            batching=batching,
            equipment=lab_config['equipment']
        )
        sample_events = sim.simulate_sample_set(workflow_steps, sample_count=sample_count, start_date=start_date)
        summary = summarize_completion(sample_events, LabCalendar(country='US', work_hours_per_day=7), sim_start_date=start_date)
        results.append({
            'scenario': scenario.get('name', f"tech{staff['tech']}_sci{staff['sci']}"),
            'tech': staff['tech'],
            'sci': staff['sci'],
            'days_to_50': summary['business_days_to_50'],
            'days_to_100': summary['business_days_to_100'],
            'date_50': summary['date_50'],
            'date_100': summary['date_100'],
        })
    print("\nScenario Summary Table:")
    print("Scenario,Tech,Sci,BusinessDaysTo50,BusinessDaysTo100,Date50,Date100")
    for r in results:
        print(f"{r['scenario']},{r['tech']},{r['sci']},{r['days_to_50']},{r['days_to_100']},{r['date_50']},{r['date_100']}")

if __name__ == "__main__":
    run_scenarios()
