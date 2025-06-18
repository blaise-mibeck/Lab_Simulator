# Staff base class
import simpy

class Staff:
    def __init__(self, env, name, config=None):
        self.env = env
        self.name = name
        self.config = config or {}
        self.skills = self.config.get('skills', {})
        self.role = self.config.get('role')
        self.experience_years = self.config.get('experience_years', 0)
        self.efficiency_factor = self.config.get('efficiency_factor', 1.0)
        self.error_rate = self.config.get('error_rate', 0.0)
        self.availability = True
        self.vacation_days_per_year = self.config.get('vacation_days_per_year', 0)
        self.sick_days_per_year = self.config.get('sick_days_per_year', 0)
        self.training_days_per_year = self.config.get('training_days_per_year', 0)
        self.full_time_equivalent = self.config.get('full_time_equivalent', 1.0)
