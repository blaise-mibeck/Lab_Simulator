# Laboratory Discrete Event Simulation System

## Overview

A comprehensive discrete event simulation framework for modeling laboratory operations, resource utilization, and project management. Built on SimPy, this system enables laboratories to optimize workflows, predict bottlenecks, plan resource allocation, and answer strategic questions about staffing and equipment investments.

## Key Capabilities

- **Process Modeling**: Convert SOPs into discrete simulation steps with resource requirements
- **Resource Optimization**: Model equipment, staff, and supply constraints with realistic scheduling
- **Project Management**: Generate work breakdown structures, network diagrams, and critical path analysis
- **Progress Tracking**: Real-time burn charts comparing planned vs. actual progress
- **Strategic Analysis**: Simulate "what-if" scenarios for staffing, equipment, and workflow changes
- **Multi-Lab Coordination**: Model projects spanning internal and external laboratory partners

## Architecture Overview

### Core Design Principles

1. **SimPy Integration**: All resources, processes, and events leverage SimPy's discrete event framework
2. **Modular Composition**: Equipment, automation, and data generation use composition patterns for flexibility
3. **Resource Abstraction**: Unified modeling of human, equipment, and supply resources
4. **Data-Driven Workflows**: Steps and processes defined declaratively for easy modification
5. **Real-Time Tracking**: Live progress monitoring and visualization during simulation execution

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Simulation    │    │     Project     │    │  Visualization  │
│   Controller    │    │   Management    │    │    Engine       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Environment   │    │ • WBS Generator │    │ • Burn Charts   │
│ • Lab Registry  │    │ • Network Diag  │    │ • Dashboards    │
│ • Metrics       │    │ • Critical Path │    │ • Gantt Charts  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                               │
┌─────────────────────────────────────────────────────────────────┐
│                      Core Simulation Engine                      │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Lab Model     │  Resource Model │ Process Model   │  Sample   │
│                 │                 │                 │   Flow    │
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ • Internal Lab  │ • Equipment     │ • Steps         │ • Stores  │
│ • External Lab  │ • Staff         │ • Methods       │ • Queues  │
│ • Multi-Lab     │ • Instruments   │ • Workflows     │ • Batches │
│   Projects      │ • Supplies      │ • Dependencies  │ • Routes  │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

## Core Components

### 1. Simulation Foundation

#### `LabSimulation`
- **Purpose**: Central simulation controller and environment manager
- **Key Features**: 
  - SimPy environment management
  - Lab registry and coordination
  - Global metrics collection
  - Disruption management (failures, sick leave)

#### `Lab` 
- **Purpose**: Container for resources and local processes
- **Types**: `InternalLab`, `ExternalLab`
- **Key Features**:
  - Resource pools (equipment, staff, supplies)
  - Sample intake/processing queues
  - Local scheduling optimization

### 2. Resource Modeling

#### `Equipment`
- **Purpose**: Physical equipment with operational states
- **Key Features**:
  - SimPy Resource integration
  - State management (idle, running, maintenance, broken)
  - Failure/repair lifecycle processes
  - Setup, run, and cleanup time modeling

#### `Staff`
- **Purpose**: Human resources with skills and availability
- **Key Features**:
  - Skill-based assignment capabilities
  - Availability disruptions (sick leave, vacation)
  - PreemptiveResource for emergency situations
  - Training and expertise levels

#### `Instrument`
- **Purpose**: Sophisticated analytical equipment abstraction
- **Key Features**:
  - Composition-based design (sample handling + automation + data generation)
  - Multiple automation levels (manual, semi-automated, fully automated)
  - Diverse data outputs (spectra, images, quantitative values)
  - Calibration and maintenance scheduling

### 3. Process Modeling

#### `Step`
- **Purpose**: Atomic unit of work with resource requirements
- **Key Features**:
  - Polymorphic resource requirements (equipment, staff, supplies, data)
  - Input/output artifact tracking
  - Duration estimates (min/most likely/max for PERT)
  - Batching capabilities

#### `Workflow`
- **Purpose**: Directed graph of steps with dependencies
- **Key Features**:
  - Dependency management
  - Data flow mapping between steps
  - Network diagram generation
  - Critical path identification

#### `Method/SOP`
- **Purpose**: Standardized operating procedures
- **Key Features**:
  - SimPy process generators
  - Resource allocation and release
  - Phase-based execution (setup, run, cleanup)

### 4. Project Management

#### `Project`
- **Purpose**: Multi-lab project orchestration
- **Key Features**:
  - Sample set management
  - Cross-lab coordination
  - Progress tracking and milestone management
  - Resource-constrained scheduling

#### `ProjectNetworkDiagram`
- **Purpose**: Critical path analysis and scheduling
- **Key Features**:
  - CPM algorithm implementation
  - Resource-constrained scheduling
  - Float time calculation
  - Critical path identification

#### `WorkBreakdownStructure`
- **Purpose**: Hierarchical task decomposition
- **Key Features**:
  - Automatic generation from workflows
  - Category-based grouping
  - Work package creation for batched operations

### 5. Progress Tracking

#### `BurnChartTracker`
- **Purpose**: Real-time progress monitoring during simulation
- **Key Features**:
  - Planned vs. actual progress curves
  - Multiple metrics (sample count, percentage completion)
  - Variance calculation and early warning
  - Live dashboard data generation

#### `ProjectTimeline`
- **Purpose**: Schedule management and progress recording
- **Key Features**:
  - Planned completion curves
  - Actual progress recording
  - Milestone tracking
  - Performance variance analysis

### 6. Sample Flow Management

#### `Sample`
- **Purpose**: Physical or digital samples with properties
- **Key Features**:
  - Hierarchical relationships (parent samples → derivative samples)
  - State tracking (whole rock → powder → analyzed)
  - Property inheritance and transformation

#### `Artifact`
- **Purpose**: Inputs/outputs of processing steps
- **Key Features**:
  - Type classification (physical samples, data files, reports)
  - Property schemas for validation
  - Dependency tracking between steps

## Implementation Checklist

### Phase 1: Core Infrastructure
- [ ] SimPy environment setup and basic resource modeling
- [ ] Base Lab class with sample queues (SimPy Stores)
- [ ] Equipment class with basic state management
- [ ] Staff class with skill-based resource allocation
- [ ] Simple Step and Method classes

### Phase 2: Process Modeling
- [ ] Comprehensive Step class with resource requirements
- [ ] Workflow class with dependency management
- [ ] Artifact system for input/output tracking
- [ ] Data flow validation between steps
- [ ] Basic batching capabilities

### Phase 3: Instrument Framework
- [ ] Base Instrument class with composition architecture
- [ ] SampleHandler implementations (manual, autosampler, continuous)
- [ ] AutomationController implementations
- [ ] DataGenerator implementations for different output types
- [ ] Maintenance and calibration lifecycle processes

### Phase 4: Project Management
- [ ] Project class for multi-lab coordination
- [ ] ProjectNetworkDiagram with CPM algorithm
- [ ] WorkBreakdownStructure generation
- [ ] Resource-constrained scheduling
- [ ] Critical path analysis

### Phase 5: Progress Tracking
- [ ] BurnChartTracker with real-time updates
- [ ] ProjectTimeline with planned vs. actual curves
- [ ] Variance calculation and alerting
- [ ] Dashboard data generation

### Phase 6: Disruption Modeling
- [ ] DisruptionManager for equipment failures
- [ ] Staff availability modeling (sick leave, vacation)
- [ ] Supply chain disruptions
- [ ] Emergency priority handling

### Phase 7: Visualization & Analysis
- [ ] Burn chart visualization components
- [ ] Network diagram rendering
- [ ] Resource utilization dashboards
- [ ] Scenario comparison tools

### Phase 8: Advanced Features
- [ ] External lab integration
- [ ] Multi-project resource sharing
- [ ] Advanced optimization algorithms
- [ ] Machine learning for duration prediction

## Example Usage Scenarios

### Resource Planning
```python
# Simulate impact of additional equipment
baseline_sim = LabSimulation(current_lab_config)
enhanced_sim = LabSimulation(current_lab_config + additional_saw)
compare_throughput(baseline_sim, enhanced_sim)
```

### Staffing Optimization
```python
# Determine optimal cross-training strategy
scenarios = [
    (2, "xrf_specialists", 0, "cross_trained"),
    (1, "xrf_specialists", 1, "cross_trained"),
    (0, "xrf_specialists", 2, "cross_trained")
]
for scenario in scenarios:
    sim = LabSimulation(configure_staff(scenario))
    results = sim.run_project(sample_set_100)
    analyze_results(scenario, results)
```

### Workflow Optimization
```python
# Compare different workflow strategies
parallel_workflow = create_parallel_workflow()
sequential_workflow = create_sequential_workflow()
compare_workflows([parallel_workflow, sequential_workflow])
```

## Terms and Definitions

### General Terms
- **Discrete Event Simulation (DES)**: Modeling approach where system state changes only at discrete points in time when events occur
- **Resource**: Any entity required to perform work (equipment, staff, supplies, data)
- **Process**: Sequence of steps that transform inputs into outputs
- **Bottleneck**: Resource or process step that limits overall system throughput

### Laboratory Terms
- **SOP**: Standard Operating Procedure - documented method for performing laboratory tasks
- **Sample Prep**: Physical preparation of samples before analysis (cutting, grinding, mounting)
- **Batch Processing**: Analyzing multiple samples together to improve efficiency
- **Cross-contamination**: Unwanted transfer of material between samples
- **QC**: Quality Control - procedures to ensure data accuracy and reliability

### Project Management Terms
- **WBS**: Work Breakdown Structure - hierarchical decomposition of project work
- **PND**: Project Network Diagram - visual representation of task dependencies
- **CPM**: Critical Path Method - algorithm for identifying longest sequence of dependent tasks
- **Float Time**: Amount of time a task can be delayed without affecting project completion
- **Burn Chart**: Progress tracking chart showing planned vs. actual completion over time

### Analytical Chemistry Terms
- **XRF**: X-Ray Fluorescence - technique for elemental analysis
- **XRD**: X-Ray Diffraction - technique for mineral/crystal structure analysis
- **CT**: Computed Tomography - 3D imaging technique
- **Thin Section**: Very thin slice of rock for optical microscopy
- **Micronization**: Process of reducing particle size to powder

### Simulation Terms
- **Event**: Instantaneous occurrence that changes system state
- **Process**: Time-consuming activity in the simulation
- **Resource**: Limited capacity entity that processes can use
- **Queue**: Waiting line for resources or processing
- **Utilization**: Percentage of time a resource is actively working

### Statistical Terms
- **PERT**: Program Evaluation and Review Technique - uses three time estimates (optimistic, most likely, pessimistic)
- **MTBF**: Mean Time Between Failures - average operational time between equipment breakdowns
- **MTTR**: Mean Time To Repair - average time required to fix broken equipment
- **Variance**: Difference between planned and actual performance

### Technology Acronyms
- **SimPy**: Python-based discrete-event simulation framework
- **API**: Application Programming Interface
- **JSON**: JavaScript Object Notation - data interchange format
- **CSV**: Comma-Separated Values - tabular data format
- **GUI**: Graphical User Interface

## File Structure

```
lab_simulation/
├── core/
│   ├── simulation.py          # LabSimulation, Environment management
│   ├── lab.py                 # Lab classes (Internal, External)
│   └── project.py             # Project orchestration
├── resources/
│   ├── equipment.py           # Equipment base classes
│   ├── instruments.py         # Instrument abstraction framework
│   ├── staff.py               # Human resource modeling
│   └── supplies.py            # Supply chain and consumables
├── processes/
│   ├── steps.py               # Step definitions and requirements
│   ├── methods.py             # SOP implementations
│   ├── workflows.py           # Workflow and dependency management
│   └── artifacts.py           # Sample and data artifacts
├── scheduling/
│   ├── network_diagram.py     # PND and critical path analysis
│   ├── wbs.py                 # Work breakdown structure
│   └── resource_scheduler.py  # Resource-constrained scheduling
├── tracking/
│   ├── burn_chart.py          # Progress tracking and variance
│   ├── metrics.py             # Performance measurement
│   └── dashboard.py           # Real-time visualization data
├── disruptions/
│   ├── failures.py            # Equipment failure modeling
│   ├── absences.py            # Staff availability disruptions
│   └── supply_chain.py        # Material shortage handling
└── visualization/
    ├── charts.py              # Chart generation
    ├── dashboards.py          # Interactive dashboards
    └── reports.py             # Analysis and reporting
```

## Getting Started

1. **Install Dependencies**: SimPy, NumPy, Pandas, NetworkX, Matplotlib/Plotly
2. **Define Your Lab**: Create equipment, staff, and instrument configurations
3. **Build Workflows**: Define steps, methods, and dependencies for your processes
4. **Configure Projects**: Set up sample sets and multi-lab coordination
5. **Run Simulations**: Execute scenarios and collect performance metrics
6. **Analyze Results**: Generate burn charts, resource utilization reports, and optimization recommendations

## Contributing

This design document serves as the foundation for implementation. Each component should be developed with:
- Comprehensive unit tests
- SimPy integration validation
- Performance benchmarking
- Documentation and examples
- Visualization capabilities

The system is designed to be extensible - new instrument types, process steps, and analysis capabilities can be added through the established composition patterns and abstract base classes.