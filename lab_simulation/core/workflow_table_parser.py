import csv
from collections import defaultdict

class WorkflowStep:
    def __init__(self, row):
        self.name = row['Step Name']
        self.prev = [x.strip() for x in row['Previous Task'].split(';') if x.strip()]
        self.deps = [x.strip() for x in row['Dependencies'].split(';') if x.strip()]
        self.next = [x.strip() for x in row['Next Task'].split(';') if x.strip()]
        self.task_type = row['Task Type']
        self.time = int(row['Time (min)'])
        self.tool = row['Tool/Instrument']
        self.attended = row['Attended'].lower() == 'yes'
        self.batch = row['Batch?'].lower() == 'yes'
        self.max_batch = int(row['Max Batch Size']) if row['Max Batch Size'] else 1

    def __repr__(self):
        return f"<WorkflowStep {self.name}>"

def parse_workflow_csv(path):
    steps = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            steps.append(WorkflowStep(row))
    return steps

def build_workflow_graph(steps):
    graph = defaultdict(list)
    for step in steps:
        for nxt in step.next:
            graph[step.name].append(nxt)
    return graph
