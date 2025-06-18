# Lab Simulator Project (June 2025)

## Project Overview
This project is a modular, data-driven laboratory discrete event simulation system in Python. It focuses on workflow/process modeling, resource management, and project management for laboratory environments. The system supports configuration via editable YAML/CSV files, provides both CLI and GUI utilities for editing lab resources and workflows, and includes both static and interactive visualization tools for simulation results and project network diagrams.

### Key Features
- Discrete event simulation of lab workflows (SimPy-based)
- Resource modeling: staff, equipment, instruments
- Data-driven configuration (YAML, CSV)
- CLI and Tkinter GUI for editing resources and workflows
- Metrics collection and visualization (Gantt, utilization, burn charts)
- Static and interactive project network diagrams (NetworkX/Matplotlib, Dash Cytoscape)
- Critical path analysis and CPM/PERT-style diagrams

### Current State (June 2025)
- Core simulation, resource, and process classes implemented
- YAML config loader and workflow table CSV parser complete
- CLI and GUI config editors for equipment, staff, instruments, workflow steps
- Metrics collection and Matplotlib-based visualization scripts
- Static and interactive project network diagram generators (with critical path highlighting)
- Dash Cytoscape app for interactive workflow visualization
- Example workflow CSVs and cleaned workflow for correct network structure
- Unit tests for core modules

### Directory Structure
- `lab_simulation/` — Core simulation engine and modules
- `tests/` — Unit tests
- `workflow_dash_app.py` — Dash Cytoscape interactive network diagram
- `visualize_metrics.py` — Metrics and Gantt chart visualization
- `config_editor.py`, `config_editor_gui.py` — CLI/GUI config editors
- `Rock_Workflow_CLEAN.csv` — Cleaned workflow table for network diagrams
- `requirements.txt` — Python dependencies
- `OLD/` — Deprecated or unneeded files (see below)

### Deprecated/Unneeded Files (moved to `OLD/`)
- `rock_analysis_configs.txt` — Old config example
- `example_workflow.csv` — Example, not used in current workflow

### How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Edit your lab resources and workflow using the CLI/GUI or by editing the YAML/CSV files
3. Run simulations and visualize results using the provided scripts
4. Launch the Dash app: `python workflow_dash_app.py`

### Next Steps
- (Optional) Add real CPM/PERT values to interactive diagrams
- (Optional) Add tooltips, export, or further customization to Dash app
- (Optional) Integrate simulation results into diagrams
- (Optional) Support for publication-quality exports (SVG, PDF)

---
For more details, see `lab_simulation_readme.md`.
