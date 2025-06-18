import simpy
from lab_simulation.resources.equipment import Equipment
from lab_simulation.resources.staff import Staff
from lab_simulation.processes.steps import Step


def run_step(env, step: Step, equipment_objs, staff_objs, sample_count=1, metrics=None):
    eq_keys = step.equipment_required
    staff_skill = step.required_skills[0] if step.required_skills else None
    duration = step.duration.get('most_likely', 1)
    batch_size = min(step.max_batch_size, sample_count) if step.can_batch else 1
    # For each batch
    for i in range(0, sample_count, batch_size):
        eq = None
        eq_key_used = None
        # Use the first available equipment in the list
        if eq_keys:
            for key in eq_keys:
                if key in equipment_objs:
                    eq = equipment_objs[key]
                    eq_key_used = key
                    break
        staff = None
        if staff_skill:
            # Find available staff with required skill
            for s in staff_objs.values():
                if staff_skill in s.skills:
                    staff = s
                    break
        start = env.now
        # Simulate process
        if eq:
            yield env.process(eq.use(duration))
        else:
            yield env.timeout(duration)
        end = env.now
        if metrics is not None:
            metrics.append({
                'step': step.name,
                'batch': i // batch_size + 1,
                'start': start,
                'end': end,
                'equipment': eq_key_used,
                'duration': end - start
            })
        # (Staff allocation not modeled in detail yet)
        # (Supplies, outputs, etc. can be added)
        # print(f"Step {step.name} completed batch {i//batch_size+1}")
