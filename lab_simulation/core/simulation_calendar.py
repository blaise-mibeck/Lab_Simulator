import datetime
from .lab_calendar import LabCalendar
from collections import defaultdict, deque

ROLE_MAP = {
    'sample prep': 'tech',
    'instrument': 'tech',
    'sample entry': 'tech',
    'data analysis': 'sci',
    'data review': 'sci',
    'reporting': 'sci',
}

def get_batch_size(step, batching):
    if not batching or not batching.get('enabled', False):
        return 1
    return batching.get('steps', {}).get(step, batching.get('default_batch_size', 1))

def get_batch_policy(batching):
    if not batching or not batching.get('enabled', False):
        return 'none'
    return batching.get('batch_policy', 'all')

class LabSimulationWithCalendar:
    def __init__(self, calendar=None, n_tech=2, n_sci=2, batching=None):
        self.calendar = calendar or LabCalendar()
        self.n_tech = n_tech
        self.n_sci = n_sci
        self.batching = batching or {}
        self.events = []  # (sample_id, step, planned_start, planned_end)

    def simulate_sample_set(self, workflow_steps, sample_count, start_date=None):
        """
        Simulate the planned schedule for a set of samples, respecting lab calendar constraints.
        workflow_steps: list of dicts with keys: 'Step Name', 'Time (min)', 'Previous Task', 'Next Task'
        sample_count: number of samples to simulate
        start_date: datetime.datetime for simulation start
        """
        if start_date is None:
            start_date = datetime.datetime.combine(datetime.date.today(), datetime.time(9,0))
        # Build step dependency graph
        step_map = {row['Step Name']: row for row in workflow_steps}
        dependencies = {row['Step Name']: [d.strip() for d in row['Dependencies'].replace(';', ',').split(',') if d.strip() and d.strip().lower() != 'none'] for row in workflow_steps}
        step_order = [row['Step Name'] for row in workflow_steps]
        # Resource pools
        tech_available = [start_date]*self.n_tech
        sci_available = [start_date]*self.n_sci
        # For each sample, track when each step can start
        sample_events = {i: [] for i in range(sample_count)}
        # Track when each sample is ready for each step
        step_ready_times = {step: [start_date]*sample_count for step in step_order}
        # For batching
        batch_policy = get_batch_policy(self.batching)
        for step in step_order:
            batch_size = get_batch_size(step, self.batching)
            ttype = step_map[step]['Task Type'].lower()
            role = ROLE_MAP.get(ttype, 'tech')
            duration = int(step_map[step]['Time (min)'])
            # For each batch
            sample_idxs = list(range(sample_count))
            batch_queue = deque(sample_idxs)
            while batch_queue:
                batch = [batch_queue.popleft() for _ in range(min(batch_size, len(batch_queue)))]
                if not batch:
                    break
                # Wait for all dependencies for all samples in batch
                dep_ends = []
                for idx in batch:
                    if dependencies[step]:
                        dep_ends.append(max(next(e['planned_end'] for e in sample_events[idx] if e['step']==dep) for dep in dependencies[step]))
                    else:
                        dep_ends.append(start_date)
                if batch_policy == 'all':
                    ready_time = max(dep_ends)
                elif batch_policy == 'min':
                    ready_time = min(dep_ends)
                else:
                    ready_time = dep_ends[0]
                # Assign staff
                if role == 'tech':
                    idx_staff = min(range(self.n_tech), key=lambda i: tech_available[i])
                    staff_ready = tech_available[idx_staff]
                    planned_start = max(ready_time, staff_ready)
                    planned_start = self.calendar.add_work_minutes(planned_start, 0)
                    planned_end = self.calendar.add_work_minutes(planned_start, duration)
                    tech_available[idx_staff] = planned_end
                else:
                    idx_staff = min(range(self.n_sci), key=lambda i: sci_available[i])
                    staff_ready = sci_available[idx_staff]
                    planned_start = max(ready_time, staff_ready)
                    planned_start = self.calendar.add_work_minutes(planned_start, 0)
                    planned_end = self.calendar.add_work_minutes(planned_start, duration)
                    sci_available[idx_staff] = planned_end
                for idx in batch:
                    sample_events[idx].append({
                        'step': step,
                        'planned_start': planned_start,
                        'planned_end': planned_end,
                        'duration': duration,
                        'staff_role': role
                    })
        self.events = sample_events
        return sample_events
