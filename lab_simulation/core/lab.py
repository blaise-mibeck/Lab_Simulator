# Lab classes (Internal, External)
import simpy

class Lab:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.sample_queue = simpy.Store(env)
        self.resources = {}

class InternalLab(Lab):
    pass

class ExternalLab(Lab):
    pass
