import csv
import datetime
from lab_simulation.core.lab_calendar import LabCalendar
from lab_simulation.core.simulation_calendar import LabSimulationWithCalendar

with open('Rock_Workflow_CLEAN.csv', newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))
    workflow_steps = [row for row in reader]

lab_calendar = LabCalendar(country='US', work_hours_per_day=7)
sim = LabSimulationWithCalendar(calendar=lab_calendar, n_tech=3, n_sci=3, batching={'enabled': True, 'steps': {'XRF Scan': 40, 'XRD Scan': 6}, 'default_batch_size': 1, 'batch_policy': 'all'})
sample_events = sim.simulate_sample_set(workflow_steps, sample_count=100, start_date=datetime.datetime(2025, 6, 30, 9, 0))
last_ends = [max(e['planned_end'].date() for e in events) for events in sample_events.values()]
print(sorted(set(last_ends)))
