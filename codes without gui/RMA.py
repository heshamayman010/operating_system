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
        self.readyTimes.append(self.readyTimes[-1]+period)
        self.deadlines = [readyTime+self.deadline for readyTime in self.readyTimes]
        self.executionTimes = []
        self.brokenDeadlines = []

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadline = deadline
                break


class OS:
    def __init__(self, Tasks, maxTime):
        self.Tasks = Tasks
        self.maxtime = maxTime
        self.currentTime= 0
        self.setPriorities()
        self.executeList = []
        while self.currentTime < self.maxtime:
            task = self.getTaskToExecute()
            self.execute(task)



    def setPriorities(self):
        tasksPeriods = []
        for task in self.Tasks:
            tasksPeriods.append(task.period)

        count = 1
        tasksPriorities = []
        for deadline1 in tasksPeriods:
            for deadline2 in tasksPeriods:
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
                    if task.taskName=="T3":
                        print(f"t: {t}, rt: {task.remainingExecution}")
                    task.brokenDeadlines.append(task.deadline)
                    task.deadlineBroken = True
            else:
                task.deadlineBroken = False

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

maxtime = 56
tasks = [Task("T1", 0, 24, 7, 24, maxtime), Task("T2", 0, 36, 12, 36, maxtime), Task("T3", 0, 48, 4, 48, maxtime)]
rma=OS(tasks, maxtime)
#uncomment the below line to get the results in the CLI
#rma.getResults()