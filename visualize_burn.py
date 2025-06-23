import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from collections import defaultdict

# Helper to color weekends/holidays

def plot_sample_burn(sample_events, calendar, holidays=None):
    holidays = holidays or set()
    fig, ax = plt.subplots(figsize=(14, 6))
    all_dates = set()
    for events in sample_events.values():
        for e in events:
            all_dates.add(e['planned_start'].date())
            all_dates.add(e['planned_end'].date())
    all_dates = sorted(all_dates)
    # Use days from start as x-axis
    day_numbers = [(d - all_dates[0]).days for d in all_dates]
    # Color weekends/holidays and annotate day numbers
    for i, d in enumerate(all_dates):
        if d.weekday() >= 5 or d in holidays or not calendar.is_workday(d):
            ax.axvspan(day_numbers[i] - 0.5, day_numbers[i] + 0.5, color='#f8d7da', alpha=0.4)
        ax.text(day_numbers[i], ax.get_ylim()[1], str(day_numbers[i]), ha='center', va='bottom', fontsize=8, color='gray', rotation=90)
    # Plot per-step activity
    step_counts = defaultdict(lambda: [0]*len(all_dates))
    date_idx = {d: i for i, d in enumerate(all_dates)}
    for events in sample_events.values():
        for e in events:
            step = e['step']
            start = e['planned_start'].date()
            end = e['planned_end'].date()
            for d in all_dates:
                if start <= d <= end:
                    step_counts[step][date_idx[d]] += 1
    # Cumulative per-step activity (burn-up)
    step_cum = defaultdict(lambda: [0]*len(all_dates))
    for step, counts in step_counts.items():
        running = 0
        for i, c in enumerate(counts):
            running += c
            step_cum[step][i] = running
    for step, cum_counts in step_cum.items():
        ax.plot(day_numbers, cum_counts, label=step)
    ax.set_xticks(day_numbers)
    ax.set_xticklabels([f"{d.strftime('%a %m-%d')}" for d in all_dates], rotation=45, ha='right')
    ax.set_xlabel('Days from Start')
    ax.set_ylabel('Cumulative Samples Completed')
    ax.set_title('Per-Sample Burn Plot')
    ax.legend()
    plt.tight_layout()
    plt.show()

def plot_project_burn(sample_events, calendar, holidays=None):
    holidays = holidays or set()
    fig, ax = plt.subplots(figsize=(14, 4))
    all_dates = set()
    for events in sample_events.values():
        for e in events:
            all_dates.add(e['planned_start'].date())
            all_dates.add(e['planned_end'].date())
    all_dates = sorted(all_dates)
    # Use days from start as x-axis
    day_numbers = [(d - all_dates[0]).days for d in all_dates]
    for i, d in enumerate(all_dates):
        if d.weekday() >= 5 or d in holidays or not calendar.is_workday(d):
            ax.axvspan(day_numbers[i] - 0.5, day_numbers[i] + 0.5, color='#f8d7da', alpha=0.4)
        ax.text(day_numbers[i], ax.get_ylim()[1], str(day_numbers[i]), ha='center', va='bottom', fontsize=8, color='gray', rotation=90)
    # Cumulative percent complete (burn-up)
    total_steps = sum(len(events) for events in sample_events.values())
    completed = [0]*len(all_dates)
    date_idx = {d: i for i, d in enumerate(all_dates)}
    for events in sample_events.values():
        for e in events:
            end = e['planned_end'].date()
            idx = date_idx[end]
            completed[idx] += 1
    # Cumulative sum
    for i in range(1, len(completed)):
        completed[i] += completed[i-1]
    percent = [c/total_steps*100 for c in completed]
    ax.plot(day_numbers, percent, label='Project % Complete', color='navy')
    ax.set_xticks(day_numbers)
    ax.set_xticklabels([f"{d.strftime('%a %m-%d')}" for d in all_dates], rotation=45, ha='right')
    ax.set_xlabel('Days from Start')
    ax.set_ylabel('Percent Complete')
    ax.set_title('Project Burn Chart')
    plt.tight_layout()
    plt.show()
