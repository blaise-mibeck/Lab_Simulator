# Workflow and dependency management

class Workflow:
    def __init__(self, steps, dependencies=None):
        self.steps = steps  # dict of step_name: Step
        self.dependencies = dependencies or []  # list of dicts

    def get_step(self, name):
        return self.steps.get(name)

    def get_dependencies(self, step_name):
        return [d for d in self.dependencies if d['to_step'] == step_name]
