import csv
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from networkx.drawing.nx_agraph import graphviz_layout

# Color map for process types
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

def read_workflow_csv(path):
    steps = {}
    edges = set()
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            step = row['Step Name']
            steps[step] = row
            # Next Task edges
            next_tasks = [x.strip() for x in row['Next Task'].replace(';', ',').split(',') if x.strip() and x.strip().lower() != 'none']
            for nxt in next_tasks:
                edges.add((step, nxt))
            # Dependency edges (for joins)
            dependencies = [x.strip() for x in row['Dependencies'].replace(';', ',').split(',') if x.strip() and x.strip().lower() != 'none']
            for dep in dependencies:
                edges.add((dep, step))
    # Add start/stop nodes
    if 'Sample Entry' in steps:
        edges.add(('START', 'Sample Entry'))
        steps['START'] = {'Step Name': 'START', 'Task Type': 'start', 'Time (min)': '0'}
    if 'Report' in steps:
        edges.add(('Report', 'STOP'))
        steps['STOP'] = {'Step Name': 'STOP', 'Task Type': 'stop', 'Time (min)': '0'}
    return steps, edges

def compute_pert_times(G, steps):
    # Forward pass (early start/finish)
    es = {n: 0 for n in G.nodes}
    ef = {n: 0 for n in G.nodes}
    for n in nx.topological_sort(G):
        duration = int(steps[n].get('Time (min)', '0')) if n in steps else 0
        es[n] = max([ef[p] for p in G.predecessors(n)] or [0])
        ef[n] = es[n] + duration
    # Backward pass (late start/finish)
    max_ef = max(ef.values())
    lf = {n: max_ef for n in G.nodes}
    ls = {n: max_ef for n in G.nodes}
    for n in reversed(list(nx.topological_sort(G))):
        duration = int(steps[n].get('Time (min)', '0')) if n in steps else 0
        lf[n] = min([ls[s] for s in G.successors(n)] or [max_ef])
        ls[n] = lf[n] - duration
    # Slack
    slack = {n: ls[n] - es[n] for n in G.nodes}
    return es, ef, ls, lf, slack

def find_critical_path(G, steps):
    # Assign durations
    durations = {n: int(steps[n].get('Time (min)', '0')) for n in G.nodes if n in steps}
    # Use networkx's dag_longest_path for critical path
    cp = nx.algorithms.dag.dag_longest_path(G, weight=lambda u, v, d: durations.get(u, 0))
    return cp

def assign_grid_positions(G):
    # Assign nodes to grid positions by topological order and layer
    layers = list(nx.topological_generations(G))
    pos = {}
    for y, layer in enumerate(layers):
        for x, node in enumerate(layer):
            pos[node] = (x, -y)  # left-to-right, top-to-bottom
    return pos

def draw_pert_node(ax, x, y, width, height, label, duration, es, ef, ls, lf, slack, color, is_critical):
    # Draw rectangle
    rect = Rectangle((x - width/2, y - height/2), width, height, linewidth=2 if is_critical else 1, edgecolor='crimson' if is_critical else 'black', facecolor=color, zorder=2)
    ax.add_patch(rect)
    # Draw horizontal lines
    ax.plot([x - width/2, x + width/2], [y + height/6, y + height/6], color='black', lw=1, zorder=3)
    ax.plot([x - width/2, x + width/2], [y - height/6, y - height/6], color='black', lw=1, zorder=3)
    # Draw vertical lines
    ax.plot([x - width/6, x - width/6], [y + height/2, y - height/2], color='black', lw=1, zorder=3)
    ax.plot([x + width/6, x + width/6], [y + height/2, y - height/2], color='black', lw=1, zorder=3)
    # Top row: ES | Dur | EF
    ax.text(x - width/3, y + height/3, f"{es}", ha='center', va='center', fontsize=8, zorder=4)
    ax.text(x, y + height/3, f"{duration}", ha='center', va='center', fontsize=8, zorder=4)
    ax.text(x + width/3, y + height/3, f"{ef}", ha='center', va='center', fontsize=8, zorder=4)
    # Middle row: Label
    ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)
    # Bottom row: LS | Slack | LF
    ax.text(x - width/3, y - height/3, f"{ls}", ha='center', va='center', fontsize=8, zorder=4)
    ax.text(x, y - height/3, f"{slack}", ha='center', va='center', fontsize=8, zorder=4)
    ax.text(x + width/3, y - height/3, f"{lf}", ha='center', va='center', fontsize=8, zorder=4)

def plot_network(steps, edges):
    G = nx.DiGraph()
    G.add_nodes_from(steps.keys())
    G.add_edges_from(edges)
    pos = assign_grid_positions(G)
    es, ef, ls, lf, slack = compute_pert_times(G, steps)
    cp = find_critical_path(G, steps)
    fig, ax = plt.subplots(figsize=(max(14, 2*len(pos)), 10))
    # Draw edges first
    for u, v in G.edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        color = 'crimson' if u in cp and v in cp and cp.index(v) == cp.index(u) + 1 else 'black'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=color, lw=2 if color=='crimson' else 1), zorder=1)
    # Draw nodes as rectangles with lines
    width, height = 1.6, 1.2
    for node in G.nodes:
        ttype = steps.get(node, {}).get('Task Type', '').lower()
        color = PROCESS_COLORS.get(ttype, 'white')
        duration = steps[node].get('Time (min)', '') if node in steps else ''
        draw_pert_node(ax, pos[node][0], pos[node][1], width, height, node, duration, es[node], ef[node], ls[node], lf[node], slack[node], color, node in cp)
    ax.set_xlim(min(x for x, y in pos.values()) - 1, max(x for x, y in pos.values()) + 1)
    ax.set_ylim(min(y for x, y in pos.values()) - 1, max(y for x, y in pos.values()) + 1)
    ax.axis('off')
    plt.title('Traditional Project Network Diagram (PERT/CPM Nodes, Critical Path Highlighted)')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    steps, edges = read_workflow_csv('Rock_Workflow_CLEAN.csv')
    plot_network(steps, edges)
