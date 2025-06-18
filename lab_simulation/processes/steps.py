# Step definitions
class Step:
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        self.category = self.config.get('category')
        self.duration = self.config.get('duration', {})
        self.unit = self.config.get('unit', 'minutes')
        self.equipment_required = self.config.get('equipment_required', [])
        self.required_skills = self.config.get('required_skills', [])
        self.skill_level = self.config.get('skill_level', 'basic')
        self.supplies = self.config.get('supplies', {})
        self.inputs = self.config.get('inputs', [])
        self.outputs = self.config.get('outputs', [])
        self.can_batch = self.config.get('can_batch', False)
        self.max_batch_size = self.config.get('max_batch_size', 1)
        self.requires_cleanup = self.config.get('requires_cleanup', False)
        self.external_lab = self.config.get('external_lab')
        self.dependencies = self.config.get('dependencies', [])
