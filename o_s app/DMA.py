import plotly.express as px
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def rangeFloat(start, end, step):
    rangelist = [start]
    if step !=0:
        while True:
            start += step
            if start > end:
                break
            rangelist.append(round(start, 2))
    return rangelist

class Task:
    def __init__(self, taskName, releaseTime, period, executionTime, deadline, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        self.period = period
        self.executionTime = executionTime
        self.remainingExecution = 0
        self.deadline = deadline
        self.deadlineBroken = False
        self.maxtime = maxTime
        self.priority = None
        self.readyTimes = [time for time in rangeFloat(releaseTime, maxTime+1, period)]
        self.readyTimes.append(self.readyTimes[-1] + period)
        self.deadlines = [readyTime+self.deadline for readyTime in self.readyTimes]
        self.executionTimes = []
        self.brokenDeadlines = []

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadline = deadline
                break


class DMAOS:
    def __init__(self, Tasks, maxTime):
        self.Tasks = Tasks
        self.maxtime = maxTime
        self.currentTime= 0
        self.setPriorities()
        self.executeList = []
        while self.currentTime < self.maxtime:

            task = self.getTaskToExecute()
            self.execute(task)

        self.plot()

    def setPriorities(self):
        tasksDeadlines = []
        for task in self.Tasks:
            tasksDeadlines.append(task.deadline)

        count = 1
        tasksPriorities = []
        for deadline1 in tasksDeadlines:
            for deadline2 in tasksDeadlines:
                if deadline1 > deadline2:
                    count += 1
            tasksPriorities.append(count)
            count = 1

        for index, task in enumerate(self.Tasks):
            task.priority = tasksPriorities[index]

    def getTaskToExecute(self):
        if not self.executeList:
            tasksReadyTime = [(task, task.readyTimes[0]) for task in self.Tasks]

            for task, readyTime in tasksReadyTime:
                if readyTime <= self.currentTime:
                    task.remainingExecution = task.executionTime
                    self.executeList.append(task)
                    task.readyTimes.pop(0)

            if not self.executeList:
                self.currentTime = min(tasksReadyTime, key= lambda readyTime: readyTime[1])[1]
                self.updateTasksRemainingExecution()
                return self.getTaskToExecute()

        priorities = []
        for task in self.executeList:
            priorities.append(task.priority)


        highestPriorityIndex = priorities.index(min(priorities))

        return self.executeList[highestPriorityIndex]

    def updateTasksRemainingExecution(self):
        for task in self.Tasks:
            if task.readyTimes[0] <= self.currentTime:
                if task.remainingExecution == 0 or task.deadlineBroken:
                    self.executeList.append(task)
                    task.remainingExecution = task.executionTime
                    task.readyTimes.pop(0)
                task.updateDeadline(self.currentTime)


    def execute(self, task):
        startTime = self.currentTime
        endTime = self.getTimeToStop(task)


        task.remainingExecution -= (endTime-startTime)

        if endTime > self.maxtime:
            task.executionTimes.append([startTime, self.maxtime])
        else:
            task.executionTimes.append([startTime, endTime])

        if task.remainingExecution == 0:
            self.executeList.remove(task)

        self.checkDeadline(endTime)
        self.currentTime = endTime

        self.updateTasksRemainingExecution()

    def getTimeToStop(self, task):
        tasksReadyTime = [t.readyTimes[0] for t in self.Tasks]
        nearestReadyTime = min(tasksReadyTime)
        if self.currentTime + task.remainingExecution < nearestReadyTime:
            return self.currentTime+task.remainingExecution
        else:
            return nearestReadyTime

    def checkDeadline(self, t):
        for task in self.Tasks:
            if task.remainingExecution != 0 and task.deadline <= t:
                if not task.deadline in task.brokenDeadlines:
                    task.brokenDeadlines.append(task.deadline)
                    task.deadlineBroken = True
            else:
                task.deadlineBroken = False
    def returnTasks(self):
        return self.Tasks

    def getResults(self):
        exedict = {}
        tasksPriorities ={}
        results = []
        brokenDeadlinesdict = {}
        for task in self.Tasks:
            exedict[f"{task.taskName}"] = task.executionTimes
            brokenDeadlinesdict[f"{task.taskName}"] = task.brokenDeadlines
            tasksPriorities[f"{task.taskName}"] = task.priority
        results.append(exedict)
        results.append(tasksPriorities)
        results.append(brokenDeadlinesdict)
        for task in self.Tasks:
            print(f"{task.taskName} execute times (from, to): {task.executionTimes}")
            if task.brokenDeadlines:
                print(f"{task.taskName} broken deadlines: {task.brokenDeadlines}")

        return results
    
    def plot(self):
        exedict={}
        for task in self.Tasks:
            exedict[f"{task.taskName}"]= task.executionTimes

        plt.figure(figsize=(maxtime, 7))
        colors = [ 'blue', 'orange',"purple"]

        # Draw the timing diagram with distinct colors
        for i, (task, intervals) in enumerate(exedict.items()):
            for interval in intervals:
                start, end = interval
                duration = end - start
                rect = Rectangle((start, 0.2*i), duration, 0.6, edgecolor='black', facecolor=colors[i % len(colors)])
                plt.gca().add_patch(rect)

                # Add task label in the middle of the rectangle
                plt.text(start + duration / 2, 0.5 + 0.2*i, task, ha='center', va='center')

        # Set the x-axis limits
        plt.xlim(0, maxtime)

        # Remove y-axis ticks and labels
        plt.yticks([])

        # Add gridlines
        plt.grid(True)

        # Show the plot
        plt.show()    

maxtime = 70
tasks = [Task("T1", 0, 60, 25, 50, maxtime), Task("T2", 15, 60, 10, 40, maxtime), Task("T3", 20, 60, 15, 60, maxtime)]

dma = DMAOS(tasks, maxtime)
#uncomment the below line to get the results in the CLI
#dma.getResults()