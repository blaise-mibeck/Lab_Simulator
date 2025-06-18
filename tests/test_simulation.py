import pytest
from lab_simulation.core.simulation import LabSimulation
from lab_simulation.core.lab import Lab
from lab_simulation.resources.equipment import Equipment
from lab_simulation.resources.staff import Staff


def test_lab_simulation_runs():
    sim = LabSimulation()
    lab = Lab(sim.env, 'TestLab')
    sim.add_lab(lab)
    eq = Equipment(sim.env, 'Centrifuge')
    staff = Staff(sim.env, 'Alice', skills=['centrifuge'])
    assert sim.env.now == 0
    sim.run(until=10)
    assert sim.env.now == 10
