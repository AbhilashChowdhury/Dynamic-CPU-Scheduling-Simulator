import matplotlib.pyplot as plt


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = -1  # To record when the process actually starts


def fcfs(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        process.start_time = current_time
        process.completion_time = current_time + process.burst_time
        current_time += process.burst_time
    return processes


def sjf(processes):
    current_time = 0
    completed = []
    ready_queue = []

    while processes or ready_queue:
        # Move all processes that have arrived into the ready queue
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))

        if ready_queue:
            # Select the process with the shortest burst time from the ready queue
            ready_queue.sort(key=lambda x: x.burst_time)  # Shortest Job First
            current_process = ready_queue.pop(0)

            if current_time < current_process.arrival_time:
                current_time = current_process.arrival_time

            current_process.start_time = current_time
            current_process.completion_time = current_time + current_process.burst_time
            current_time += current_process.burst_time
            completed.append(current_process)
        else:
            current_time += 1  # No process is ready, increment time

    return completed



def priority_scheduling(processes):
    current_time = 0
    completed = []
    ready_queue = []

    while processes or ready_queue:
        # Move all processes that have arrived into the ready queue
        while processes and processes[0].arrival_time <= current_time:
            ready_queue.append(processes.pop(0))

        if ready_queue:
            # Select the process with the highest priority from the ready queue
            ready_queue.sort(key=lambda x: x.priority)  # Lower number means higher priority
            current_process = ready_queue.pop(0)

            if current_time < current_process.arrival_time:
                current_time = current_process.arrival_time

            current_process.start_time = current_time
            current_process.completion_time = current_time + current_process.burst_time
            current_time += current_process.burst_time
            completed.append(current_process)
        else:
            current_time += 1  # No process is ready, increment time

    return completed



def calculate_metrics(processes):
    total_burst_time = 0
    total_idle_time = 0
    for process in processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        total_burst_time += process.burst_time
        total_idle_time += (process.start_time - process.arrival_time)

    # Calculate CPU utilization
    total_time = max(p.completion_time for p in processes) - min(p.arrival_time for p in processes)
    cpu_utilization = (total_burst_time / total_time) * 100 if total_time > 0 else 0

    return cpu_utilization


def visualize_detailed_gantt_chart(processes, algorithm_name):
    fig, gnt = plt.subplots()
    gnt.set_title(f"Gantt Chart for {algorithm_name} ( With Waiting Time [Orange] & Turnaround Times [Orange+Blue] )")
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Process ID')

    max_time = max(p.completion_time for p in processes)
    gnt.set_xlim(0, max_time)
    gnt.set_ylim(0, len(processes))

    plt.xticks(range(0, max_time + 1))  # Show time ticks as integers

    for idx, process in enumerate(processes):
        # Plot waiting time (before start time)
        if process.start_time > process.arrival_time:
            gnt.broken_barh([(process.arrival_time, process.start_time - process.arrival_time)],
                            (idx, 1), facecolors=('tab:orange'))  # Waiting time in orange

        # Plot burst time (execution time)
        gnt.broken_barh([(process.start_time, process.burst_time)],
                        (idx, 1), facecolors=('tab:blue'))  # Execution time in blue

        plt.text(process.start_time + process.burst_time / 2, idx + 0.5, f'P{process.pid}', ha='center')

        plt.text(process.completion_time + 0.1, idx + 0.5,
                 f' AT: {process.arrival_time}, BT: {process.burst_time}, \n\n TAT: {process.turnaround_time}, WT: {process.waiting_time}', va='center')

    plt.show()


def print_report(processes, algorithm_name, cpu_utilization):
    print(f"Report for {algorithm_name}")
    print(
        f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Priority':<10}{'Completion':<15}{'Turnaround':<15}{'Waiting':<10}")
    for process in processes:
        print(f"{process.pid:<5}{process.arrival_time:<10}{process.burst_time:<10}{process.priority:<10}"
              f"{process.completion_time:<15}{process.turnaround_time:<15}{process.waiting_time:<10}")
    avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)
    avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)
    print(f"Average Turnaround Time: {avg_turnaround_time}")
    print(f"Average Waiting Time: {avg_waiting_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    return avg_waiting_time, avg_turnaround_time, cpu_utilization


def get_user_input():
    processes = []
    num_processes = int(input("Enter the number of processes : "))

    for _ in range(num_processes):
        pid = int(input(f"\nEnter Process ID : "))
        arrival_time = int(input(f"Enter Arrival Time for process {pid} : "))
        burst_time = int(input(f"Enter Burst Time for process {pid} : "))
        priority = int(input(f"Enter Priority for process {pid} (Higher number means lower priority) : "))

        processes.append(Process(pid, arrival_time, burst_time, priority))

    return processes


def main():
    processes = get_user_input()

    algorithms = {'FCFS': fcfs, 'SJF': sjf, 'Priority': priority_scheduling}
    comparison_data = {}

    for name, algorithm in algorithms.items():
        print(f"\nRunning {name} Scheduling")
        scheduled_processes = algorithm(processes.copy())
        calculate_metrics(scheduled_processes)
        cpu_utilization = calculate_metrics(scheduled_processes)
        visualize_detailed_gantt_chart(scheduled_processes, name)
        avg_waiting_time, avg_turnaround_time, cpu_utilization = print_report(scheduled_processes, name, cpu_utilization)

        comparison_data[name] = {
            'Average Waiting Time': avg_waiting_time,
            'Average Turnaround Time': avg_turnaround_time,
            'CPU Utilization': cpu_utilization
        }

    print("\n---------------------------- Comparison Report ----------------------------")
    print(f"{'Algorithm':<15}{'Avg Waiting Time':<20}{'Avg Turnaround Time':<20}{'CPU Utilization (%)':<20}")
    for algo, metrics in comparison_data.items():
        print(f"{algo:<15}{metrics['Average Waiting Time']:<20}{metrics['Average Turnaround Time']:<20}{metrics['CPU Utilization']:<20}")


if __name__ == '__main__':
    main()