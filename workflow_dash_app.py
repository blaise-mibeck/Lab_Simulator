import dash
from dash import html
import dash_cytoscape as cyto
import csv
import networkx as nx

# Define colors for different process types
PROCESS_COLORS = {
    'sample entry': 'gold',
    'sample prep': 'orange',
    'instrument': 'skyblue',
    'data analysis': 'violet',
    'data review': 'limegreen',
    'reporting': 'red',
    'start': 'gray',
    'stop': 'gray',
}

def build_elements(csv_path):
    nodes = []  # Initialize nodes list
    edges = []  # Initialize edges list
    G = nx.DiGraph()  # Directed graph for critical path calculation
    step_durations = {}  # Dictionary to store step durations

    # Read CSV and build initial nodes and edges
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for row in reader:
            label = row['Step Name']
            duration = row['Time (min)']
            ttype = row['Task Type']
            color = PROCESS_COLORS.get(ttype, 'gray')

            # Multi-line label for CPM/PERT style
            es = ef = ls = lf = slack = '?'  # Placeholders for CPM values
            node_label = f"ES|Dur|EF\n{label}\nLS|Float|LF"
            nodes.append({
                'data': {'id': label, 'label': node_label},
                'classes': ttype.replace(' ', '_'),
                'style': {'background-color': color}
            })
            step_durations[label] = int(duration) if duration.isdigit() else 0

        # Create edges and add to graph
        for row in reader:
            label = row['Step Name']
            for nxt in row['Next Task'].replace(';', ',').split(','):
                nxt = nxt.strip()
                if nxt and nxt.lower() != 'none':
                    edges.append({'data': {'source': label, 'target': nxt, 'id': f'{label}->{nxt}'}})
                    G.add_edge(label, nxt)

    # Add start/stop nodes and edges
    nodes.append({'data': {'id': 'START', 'label': 'START'}, 'style': {'background-color': 'gray'}})
    edges.append({'data': {'source': 'START', 'target': 'Sample Entry', 'id': 'START->Sample Entry'}})
    nodes.append({'data': {'id': 'STOP', 'label': 'STOP'}, 'style': {'background-color': 'gray'}})
    edges.append({'data': {'source': 'Report', 'target': 'STOP', 'id': 'Report->STOP'}})
    G.add_edge('START', 'Sample Entry')
    G.add_edge('Report', 'STOP')

    # Compute critical path
    try:
        cp = nx.algorithms.dag.dag_longest_path(G, weight=lambda u, v, d: step_durations.get(u, 0))
        cp_edges = set((cp[i], cp[i+1]) for i in range(len(cp)-1))
    except Exception:
        cp_edges = set()

    # Mark critical path edges
    for edge in edges:
        if (edge['data']['source'], edge['data']['target']) in cp_edges:
            edge['classes'] = 'critical'

    return nodes + edges

# Build elements from CSV
elements = build_elements('Rock_Workflow_CLEAN.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H2('Interactive Project Network Diagram (Dash Cytoscape)'),
    cyto.Cytoscape(
        id='cytoscape-workflow',
        elements=elements,
        layout={'name': 'breadthfirst', 'directed': True, 'padding': 20, 'spacingFactor': 1.5},
        style={'width': '100%', 'height': '900px'},
        stylesheet=[
            {'selector': 'node', 'style': {
                'label': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'shape': 'rectangle',
                'width': 120,
                'height': 60,
                'font-size': 14,
                'border-width': 2,
                'border-color': '#333',
            }},
            {'selector': 'edge', 'style': {
                'width': 3,
                'line-color': '#888',
                'target-arrow-color': '#888',
                'target-arrow-shape': 'triangle',
            }},
            {'selector': '.critical', 'style': {
                'line-color': 'crimson',
                'target-arrow-color': 'crimson',
                'width': 5,
            }},
        ]
    )
])

# Run app
if __name__ == '__main__':
    app.run(debug=True)
