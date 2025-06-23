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
    def __init__(self, calendar=None, n_tech=2, n_sci=2, batching=None, equipment=None):
        self.calendar = calendar or LabCalendar()
        self.n_tech = n_tech
        self.n_sci = n_sci
        self.batching = batching or {}
        self.equipment = equipment or []
        self.events = []  # (sample_id, step, planned_start, planned_end)

    def get_equipment_quantity(self, step_name):
        # Match equipment by step name (case-insensitive substring match)
        for eq in self.equipment:
            if eq['name'].lower() in step_name.lower() or step_name.lower() in eq['name'].lower():
                return eq.get('quantity', 1)
        return 1

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
            # Equipment constraint
            eq_quantity = self.get_equipment_quantity(step)
            eq_available = [start_date]*eq_quantity
            # For each batch
            sample_idxs = list(range(sample_count))
            completed = set()
            while len(completed) < sample_count:
                # Find samples ready for this step (dependencies met and not already processed)
                ready_now = []
                for idx in sample_idxs:
                    if idx in completed:
                        continue
                    # Only consider sample ready if all dependencies are completed
                    if dependencies[step]:
                        dep_ends = []
                        all_deps_done = True
                        for dep in dependencies[step]:
                            dep_event = next((e for e in sample_events[idx] if e['step']==dep), None)
                            if dep_event is not None:
                                dep_ends.append(dep_event['planned_end'])
                            else:
                                all_deps_done = False
                                break
                        if not all_deps_done:
                            continue
                        ready_time = max(dep_ends) if batch_policy == 'all' else min(dep_ends)
                        ready_now.append((idx, ready_time))
                    else:
                        ready_now.append((idx, start_date))
                # Sort by ready_time, take up to batch_size
                ready_now.sort(key=lambda x: x[1])
                batch = [idx for idx, _ in ready_now[:batch_size]]
                if not batch:
                    # If no samples are ready, advance time to the next soonest ready_time
                    if ready_now:
                        soonest = min(rt for _, rt in ready_now)
                        for i in range(len(tech_available if role=='tech' else sci_available)):
                            if role == 'tech':
                                if tech_available[i] < soonest:
                                    tech_available[i] = soonest
                            else:
                                if sci_available[i] < soonest:
                                    sci_available[i] = soonest
                    break
                # Use the latest ready_time in the batch for 'all', earliest for 'min'
                if batch_policy == 'all':
                    batch_ready_time = max(ready_now[i][1] for i in range(len(batch)))
                else:
                    batch_ready_time = min(ready_now[i][1] for i in range(len(batch)))
                # Assign staff
                if role == 'tech':
                    idx_staff = min(range(self.n_tech), key=lambda i: tech_available[i])
                    staff_ready = tech_available[idx_staff]
                else:
                    idx_staff = min(range(self.n_sci), key=lambda i: sci_available[i])
                    staff_ready = sci_available[idx_staff]
                # Assign equipment
                idx_eq = min(range(eq_quantity), key=lambda i: eq_available[i])
                eq_ready = eq_available[idx_eq]
                planned_start = max(batch_ready_time, staff_ready, eq_ready)
                planned_start = self.calendar.add_work_minutes(planned_start, 0)
                planned_end = self.calendar.add_work_minutes(planned_start, duration)
                # Update resource availability
                if role == 'tech':
                    tech_available[idx_staff] = planned_end
                else:
                    sci_available[idx_staff] = planned_end
                eq_available[idx_eq] = planned_end
                for idx in batch:
                    sample_events[idx].append({
                        'step': step,
                        'planned_start': planned_start,
                        'planned_end': planned_end,
                        'duration': duration,
                        'staff_role': role
                    })
                    completed.add(idx)
        self.events = sample_events
        return sample_events
