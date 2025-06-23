import csv
import yaml
from lab_simulation.core.lab_calendar import LabCalendar
from lab_simulation.core.simulation_calendar import LabSimulationWithCalendar
from visualize_burn import plot_sample_burn, plot_project_burn
import datetime

# Load simulation config
def load_sim_config(path='sim_config.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

sim_config = load_sim_config()
sample_count = sim_config.get('samples', 100)
workflow_file = sim_config.get('workflow_file', 'Rock_Workflow_CLEAN.csv')
start_date = datetime.datetime.strptime(sim_config.get('start_date', '2025-06-18 09:00'), '%Y-%m-%d %H:%M')
staff = sim_config.get('staff', {'tech': 2, 'sci': 2})
batching = sim_config.get('batching', {})

# Load workflow steps from config-specified file
with open(workflow_file, newline='', encoding='utf-8') as csvfile:
    reader = list(csv.DictReader(csvfile))
    workflow_steps = [row for row in reader]

# Define lab calendar (US, 7 hours/day, M-F, no custom holidays)
lab_calendar = LabCalendar(country='US', work_hours_per_day=7)

lab_config_file = sim_config.get('lab_config_file', 'lab_config.yaml')
with open(lab_config_file, 'r') as f:
    lab_config = yaml.safe_load(f)

# Simulate a sample set (100 samples)
sim = LabSimulationWithCalendar(calendar=lab_calendar, n_tech=staff['tech'], n_sci=staff['sci'], batching=batching, equipment=lab_config['equipment'])
sample_events = sim.simulate_sample_set(workflow_steps, sample_count=sample_count, start_date=start_date)

# Plot per-sample burn
plot_sample_burn(sample_events, lab_calendar)

# Plot overall project burn
plot_project_burn(sample_events, lab_calendar)

def summarize_completion(sample_events, calendar, sim_start_date=None):
    """
    Returns a dict with business days to 50% and 100% complete.
    """
    all_dates = set()
    for events in sample_events.values():
        for e in events:
            all_dates.add(e['planned_end'].date())
    all_dates = sorted(all_dates)
    total_samples = len(sample_events)
    # Find last step for each sample
    last_ends = [max(e['planned_end'].date() for e in events) for events in sample_events.values()]
    # Count how many samples are done by each date
    done_cum = [sum(1 for d in last_ends if d <= date) for date in all_dates]
    # Find 50% and 100% indices
    half_idx = next((i for i, c in enumerate(done_cum) if c >= total_samples/2), None)
    full_idx = next((i for i, c in enumerate(done_cum) if c >= total_samples), None)
    # Find the actual milestone dates
    date_50 = all_dates[half_idx] if half_idx is not None else None
    date_100 = all_dates[full_idx] if full_idx is not None else None
    # Use the true simulation start date
    if sim_start_date is not None:
        start_date = sim_start_date.date()
    else:
        start_date = min(all_dates) if all_dates else None
    # Count business days between start and milestone date (inclusive)
    def business_days_between(start, end):
        if start is None or end is None:
            return None
        days = 0
        d = start
        while d <= end:
            if calendar.is_workday(d):
                days += 1
            d += datetime.timedelta(days=1)
        return days
    return {
        'business_days_to_50': business_days_between(start_date, date_50),
        'business_days_to_100': business_days_between(start_date, date_100),
        'date_50': date_50,
        'date_100': date_100,
    }

if __name__ == "__main__":
    summary = summarize_completion(sample_events, lab_calendar, sim_start_date=start_date)
    print("\nSummary:")
    print(f"Business days to 50% complete: {summary['business_days_to_50']} (by {summary['date_50']})")
    print(f"Business days to 100% complete: {summary['business_days_to_100']} (by {summary['date_100']})")
