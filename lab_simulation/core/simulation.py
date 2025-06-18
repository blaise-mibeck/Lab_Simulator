# LabSimulation and environment management

import simpy

class LabSimulation:
    def __init__(self):
        self.env = simpy.Environment()
        self.labs = []
        self.metrics = {}

    def add_lab(self, lab):
        self.labs.append(lab)

    def run(self, until=100):
        self.env.run(until=until)
