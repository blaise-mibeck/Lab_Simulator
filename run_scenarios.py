import yaml
import csv
import datetime
from lab_simulation.core.lab_calendar import LabCalendar
from lab_simulation.core.simulation_calendar import LabSimulationWithCalendar
from run_burn_plots import summarize_completion

# Load workflow steps from CSV
with open('Rock_Workflow_CLEAN.csv', newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))
    workflow_steps = [row for row in reader]

# Load scenarios
def load_scenarios(path='scenarios.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)['scenarios']

scenarios = load_scenarios()
lab_calendar = LabCalendar(country='US', work_hours_per_day=7)

results = []
for scenario in scenarios:
    staff = scenario['staff']
    sim = LabSimulationWithCalendar(calendar=lab_calendar, n_tech=staff['tech'], n_sci=staff['sci'])
    sample_events = sim.simulate_sample_set(workflow_steps, sample_count=100, start_date=datetime.datetime(2025, 6, 18, 9, 0))
    summary = summarize_completion(sample_events, lab_calendar)
    results.append({
        'scenario': scenario['name'],
        'tech': staff['tech'],
        'sci': staff['sci'],
        'days_to_50': summary['business_days_to_50'],
        'days_to_100': summary['business_days_to_100'],
        'date_50': summary['date_50'],
        'date_100': summary['date_100'],
    })

# Print summary table
print("\nScenario Summary Table:")
print("Scenario,Tech,Sci,BusinessDaysTo50,BusinessDaysTo100,Date50,Date100")
for r in results:
    print(f"{r['scenario']},{r['tech']},{r['sci']},{r['days_to_50']},{r['days_to_100']},{r['date_50']},{r['date_100']}")
