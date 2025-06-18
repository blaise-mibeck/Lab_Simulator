import pandas as pd
import matplotlib.pyplot as plt

def plot_gantt(metrics):
    df = pd.DataFrame(metrics)
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, row in df.iterrows():
        ax.barh(row['step'] + f" (batch {row['batch']})", row['duration'], left=row['start'])
    ax.set_xlabel('Simulated Time (minutes)')
    ax.set_ylabel('Step (Batch)')
    ax.set_title('Sample Processing Gantt Chart')
    plt.tight_layout()
    plt.show()

def plot_equipment_utilization(metrics):
    df = pd.DataFrame(metrics)
    eq_usage = df.groupby('equipment')['duration'].sum().sort_values(ascending=False)
    eq_usage.plot(kind='bar', figsize=(8,4))
    plt.ylabel('Total Usage Time (minutes)')
    plt.title('Equipment Utilization')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    import json
    with open('metrics.json', 'r') as f:
        metrics = json.load(f)
    plot_gantt(metrics)
    plot_equipment_utilization(metrics)
