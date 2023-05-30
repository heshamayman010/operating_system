from collections import deque
import matplotlib.pyplot as plt

class Task:
    def __init__(self, name, period, release_time, deadline, execution_time):
        self.name = name
        self.period = period
        self.release_time = release_time
        self.deadline = deadline
        self.execution_time = execution_time
        self.remaining_time = execution_time
import math

import math

from collections import deque


release_times=[]
period_times=[]



def schedule_tasks(tasks, time_quantum):
    queue = tasks
    period_queue=tasks
    ready_queue = deque()
    running_queue = deque()
    waiting_time = [0] * len(tasks)
    turnaround_time = [0] * len(tasks)
    total_waiting_time = 0
    total_turnaround_time = 0

    gantt_chart = []
    current_time = 0
    current_task = None

    

    while (queue or current_task or ready_queue or running_queue) and current_time <=14 :
      for w in release_times:
        if current_time >=w:
          for l in queue :
            ready_queue.append(l)
            queue.remove(l)
            get_out=True
            release_times.remove(w)
            break
        if get_out==True:
          get_out=False
          break
      for f in period_times:
        if current_time >=f:
          ready_queue.append(period_queue[period_times.index(f)])
          period_times.remove(f)
          break
      if ready_queue:
        current_task = ready_queue.popleft()
      elif running_queue:
        current_task = running_queue.popleft()
      else:
        current_time+=1
        continue

      if current_task.remaining_time > 0:
          if current_task.remaining_time <= time_quantum:
            time_taken = current_task.remaining_time
            gantt_chart.append((current_task.name, current_time, current_time + time_taken))
            current_time+=time_taken
            current_task=None
          else:
            if len(running_queue)==0:
              current_time += time_quantum
              flag=False
              for s in queue :
                if s.release_time<=current_time:
                  current_task.remaining_time -= time_quantum
                  time_taken = current_task.remaining_time
                  gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum+ time_taken))
                  running_queue.append(current_task)
                  current_task=None
                  flag=True
                  break
              if flag==True:
                flag=False
                continue
              for h in queue:
                if current_task.remaining_time >h.release_time:
                  flag4=False
                  current_task.remaining_time -= h.release_time
                  time_taken = h.release_time
                  gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum+ time_taken))
                  running_queue.append(current_task)
                  current_task=None
                  flag4=True
                  current_time -= time_quantum
                  current_time+=h.release_time
                  break
              if(flag4==True):
                flag4=False
                continue
              time_taken = current_task.remaining_time
              gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum + time_taken))
              current_time += time_taken
              current_task=None 
            else:
              time_taken = time_quantum
              current_task.remaining_time -=time_quantum
              gantt_chart.append((current_task.name, current_time, current_time + time_taken))
              current_time += time_quantum
              running_queue.append(current_task)
              current_task=None

          
    plot_gantt_chart(gantt_chart)


def plot_gantt_chart(gantt_chart):
    fig, gnt = plt.subplots()

    gnt.set_title('Round Robin Scheduling')
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Tasks')

    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    task_colors = {}

    for i, task in enumerate(gantt_chart):
        task_name = task[0]
        start_time = task[1]
        end_time = task[2]
        color = task_colors.get(task_name)

        if color is None:
            color = colors[len(task_colors) % len(colors)]
            task_colors[task_name] = color

        gnt.broken_barh([(start_time, end_time - start_time)], (i, 0.6), facecolors=color, edgecolor='black')
        gnt.text(start_time + (end_time - start_time) / 2, i + 0.3, task_name, ha='center', va='center', color='white', fontsize=8)

    # Set xticks with float intervals
    xticks = [i for i in range(int(gantt_chart[-1][2]) + 2)]
    gnt.set_xticks(xticks)

    plt.yticks(range(len(gantt_chart)), [task[0] for task in gantt_chart])
    plt.grid(True)

    plt.show()


# Example usage
tasks = [
    Task("Task 1", 6, 0, 6, 2),
    Task("Task 2", 8, 1, 8, 2),
    Task("Task 3",15,2,15,4)]
for i in tasks:
      release_times.append(i.release_time)
for i in tasks:
      period_times.append(i.period)
schedule_tasks(tasks,0.25)
