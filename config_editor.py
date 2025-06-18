import yaml
import os

def load_config(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def save_config(config, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, sort_keys=False, allow_unicode=True)

def prompt(msg, default=None):
    val = input(f"{msg} [{default}]: ")
    return val if val else default

def add_equipment(config):
    eq_key = prompt('Equipment key (unique, e.g. micronizer_3)')
    eq = {}
    eq['name'] = prompt('Name', 'New Equipment')
    eq['make'] = prompt('Make', 'Generic')
    eq['model'] = prompt('Model', 'Model X')
    eq['year'] = int(prompt('Year', '2025'))
    eq['serial_number'] = prompt('Serial Number', 'SN-000')
    eq['mounting_type'] = prompt('Mounting Type', 'benchtop')
    eq['location'] = prompt('Location', 'Lab')
    # Timing
    eq['setup_time'] = {k: int(prompt(f'Setup time {k} (min)', '5')) for k in ['min','most_likely','max']}
    eq['sample_run_time'] = {k: int(prompt(f'Run time {k} (min)', '10')) for k in ['min','most_likely','max']}
    eq['cleanup_time'] = {k: int(prompt(f'Cleanup time {k} (min)', '5')) for k in ['min','most_likely','max']}
    eq['shutdown_time'] = {k: int(prompt(f'Shutdown time {k} (min)', '2')) for k in ['min','most_likely','max']}
    eq['automation_level'] = prompt('Automation level', 'manual')
    eq['sample_handling_type'] = prompt('Sample handling type', 'individual')
    eq['data_output_type'] = prompt('Data output type', 'none')
    eq['requires_supervision'] = prompt('Requires supervision (true/false)', 'true').lower() == 'true'
    eq['capacity'] = int(prompt('Capacity', '1'))
    eq['max_samples_before_maintenance'] = int(prompt('Max samples before maintenance', '100'))
    eq['maintenance_duration_hours'] = int(prompt('Maintenance duration (hours)', '2'))
    eq['calibration_frequency_days'] = prompt('Calibration frequency (days)', 'null')
    eq['required_operator_skill'] = prompt('Required operator skill', 'operation')
    eq['operator_skill_level'] = prompt('Operator skill level', 'basic')
    eq['consumables_per_sample'] = {}
    while True:
        c = prompt('Add consumable (name or blank to finish)', '')
        if not c: break
        eq['consumables_per_sample'][c] = float(prompt(f'Amount per sample for {c}', '0.1'))
    eq['mtbf_hours'] = int(prompt('MTBF (hours)', '100'))
    eq['mttr_hours'] = int(prompt('MTTR (hours)', '1'))
    config.setdefault('equipment', {})[eq_key] = eq
    print(f"Added/updated equipment: {eq_key}")

def add_staff(config):
    staff_key = prompt('Staff key (unique, e.g. technician_3)')
    st = {}
    st['name'] = prompt('Name', 'New Staff')
    st['role'] = prompt('Role', 'technician')
    st['experience_years'] = int(prompt('Experience (years)', '1'))
    st['full_time_equivalent'] = float(prompt('FTE', '1.0'))
    st['skills'] = {}
    while True:
        skill = prompt('Add skill (name or blank to finish)', '')
        if not skill: break
        st['skills'][skill] = {
            'level': prompt(f'Level for {skill}', 'basic'),
            'certified': prompt(f'Certified for {skill} (true/false)', 'false').lower() == 'true'
        }
    st['vacation_days_per_year'] = int(prompt('Vacation days/year', '15'))
    st['sick_days_per_year'] = int(prompt('Sick days/year', '5'))
    st['training_days_per_year'] = int(prompt('Training days/year', '10'))
    st['efficiency_factor'] = float(prompt('Efficiency factor', '1.0'))
    st['error_rate'] = float(prompt('Error rate', '0.02'))
    config.setdefault('staff', {})[staff_key] = st
    print(f"Added/updated staff: {staff_key}")

def main():
    path = prompt('Config file path', 'rock_analysis_configs.txt')
    config = load_config(path)
    while True:
        print("\nConfig Editor Menu:")
        print("1. Add/Edit Equipment")
        print("2. Add/Edit Staff")
        print("3. Save and Exit")
        print("4. Exit without Saving")
        choice = prompt('Choose option', '1')
        if choice == '1':
            add_equipment(config)
        elif choice == '2':
            add_staff(config)
        elif choice == '3':
            save_config(config, path)
            print('Config saved.')
            break
        elif choice == '4':
            print('Exiting without saving.')
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    main()
