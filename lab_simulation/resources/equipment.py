# Equipment base class
import simpy

class Equipment:
    def __init__(self, env, name, config=None):
        self.env = env
        self.name = name
        self.resource = simpy.Resource(env, capacity=config.get('capacity', 1) if config else 1)
        self.state = 'idle'
        self.config = config or {}
        # Timing parameters
        self.setup_time = self.config.get('setup_time', {})
        self.run_time = self.config.get('sample_run_time', {})
        self.cleanup_time = self.config.get('cleanup_time', {})
        self.shutdown_time = self.config.get('shutdown_time', {})
        # Maintenance
        self.max_samples_before_maintenance = self.config.get('max_samples_before_maintenance')
        self.maintenance_duration_hours = self.config.get('maintenance_duration_hours')
        # Failure
        self.mtbf_hours = self.config.get('mtbf_hours')
        self.mttr_hours = self.config.get('mttr_hours')
        # Resource requirements
        self.required_operator_skill = self.config.get('required_operator_skill')
        self.operator_skill_level = self.config.get('operator_skill_level')
        self.consumables_per_sample = self.config.get('consumables_per_sample', {})
        # Operational
        self.automation_level = self.config.get('automation_level')
        self.requires_supervision = self.config.get('requires_supervision', True)
        self.samples_processed = 0

    def use(self, duration):
        with self.resource.request() as req:
            yield req
            self.state = 'running'
            yield self.env.timeout(duration)
            self.state = 'idle'
            self.samples_processed += 1
            # Maintenance check
            if self.max_samples_before_maintenance and self.samples_processed >= self.max_samples_before_maintenance:
                self.state = 'maintenance'
                yield self.env.timeout(self.maintenance_duration_hours * 60)  # hours to minutes
                self.samples_processed = 0
                self.state = 'idle'
