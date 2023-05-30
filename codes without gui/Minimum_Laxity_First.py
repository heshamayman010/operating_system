def rangeFloat(start, end, step):
    rangelist = [start]
    if step !=0:
        while True:
            start += step
            if start > end:
                break
            rangelist.append(round(start, 2))
    return rangelist

class OS:
    def __init__(self, tasks, maxtime):

        self.tasks = tasks
        self.maxtime = maxtime
        #list containing the slackTime of each task during the whole execution
        self.tasksSlackTimes =[]
        #curent time in execution
        self.currentTime = 0
        self.executeList = []
        # execute as long as the current execution time is less than the maximum time required
        while self.currentTime < maxtime:
            # getting the task with the minimum slack time
            minSlackTask = self.getMinSlackTime()
            # executing the task with the minimum slack time
            self.execute(minSlackTask)

    def getMinSlackTime(self):
        # list to contain the slack time for each task at the current execution time
        tasksSlackTime =[]
        tasksReadyTimes = [(task, task.readyTimes[0]) for task in self.tasks]
        # calculating the slack time for each task and add them to the list
        for task, readytime in tasksReadyTimes:
            if readytime <= self.currentTime:
                self.executeList.append(task)
                task.readyTimes.pop(0)
                task.remainingExecution = task.executionTime
            task.updateDeadline(self.currentTime)
            tasksSlackTime.append(task.calcSlackTime(self.currentTime))

        # making a copy of the list
        tasksSlackTime2 = tasksSlackTime.copy()
        # removing slack time of tasks that has no remaining execution at the current execution time from the copied list
        for taskSlacktime in tasksSlackTime:
            # if slack time of a task = None indicates that the task remaining execution time = 0
            if taskSlacktime==None:
                tasksSlackTime2.remove(None)

        # if there is no item in the copied list means that at the current execution time there will be no task running
        if not tasksSlackTime2:
            # updating current execution time to the nearest job of task to be ready to be executed
            tasksNextReadyTime = [task.readyTimes[0] for task in self.tasks]
            self.currentTime = min(tasksNextReadyTime)

            # updating remaining execution time of tasks that has job at the current time to be renewed
            self.updateTasksRemainingExecution()
            # after updating the current execution time we call the function again to provide the min slack time task to the execution
            return self.getMinSlackTime()


        # getting the index of the minimum slack time task
        minSlackIndex= tasksSlackTime.index(min(tasksSlackTime2))
        # saving information of the slack times of each task
        self.tasksSlackTimes.append((tasksSlackTime, self.currentTime))

        return self.tasks[minSlackIndex]

    def updateTasksRemainingExecution(self):
        for task in self.tasks:
            if task.readyTimes[0] <= self.currentTime:
                if task.remainingExecution == 0 or task.deadlineBroken:
                    self.executeList.append(task)
                    task.remainingExecution = task.executionTime
                    task.readyTimes.pop(0)
                task.updateDeadline(self.currentTime)

    def execute(self, task):
        # defining start time and end time of execution of the task
        startTime = self.currentTime

        # calling getTimeToStop function to calculate the when the task will stop execution
        endTime = self.getTimeToStop(task)

        #updating the task remaining execution time
        task.remainingExecution -= (endTime-startTime)
        #ensuring that the end time doesn't pass the maximum time
        if endTime > self.maxtime:
            task.executionTimes.append([startTime, self.maxtime])
        else:
            task.executionTimes.append([startTime, endTime])

        if task.remainingExecution == 0:
            self.executeList.remove(task)
        # checking if task has passed its deadline
        self.checkDeadline(endTime)
        # after execution the current execution time updated to the end time of the task
        self.currentTime = endTime

        self.updateTasksRemainingExecution()



    def getTimeToStop(self, task):
        # creating a list to contain the nearest ready time to be executed for each task
        tasksNextReadyTime = []
        for t in self.tasks:
            tasksNextReadyTime.append(t.readyTimes[0])

        # getting the nearest job to be ready from the current execution time
        nearestReadyTime = min(tasksNextReadyTime)


        if self.currentTime + task.remainingExecution < nearestReadyTime:
            #execution of task finished before the nearest job to be ready time
            return self.currentTime + task.remainingExecution
        else:
            # execution of the task will be stopped at the nearest job to be ready time,
            # because we need to calculate the slack time of all tasks to determine which one to execute.
            return nearestReadyTime

    def checkDeadline(self, t):
        for task in self.tasks:
            if task.remainingExecution != 0 and task.deadLine <= t:
                if not task.deadLine in task.brokenDeadlines:
                    task.brokenDeadlines.append(task.deadLine)
                    task.deadlineBroken = True
            else:
                task.deadlineBroken = False

    def getResults(self):
        exedict = {}
        results = []
        negativeSlackdict = {}
        brokenDeadlinesdict = {}
        for task in self.tasks:
            exedict[f"{task.taskName}"]=task.executionTimes
            negativeSlackdict[f"{task.taskName}"] = f"{task.negativeSlackTimes} "
            brokenDeadlinesdict[f"{task.taskName}"] = task.brokenDeadlines
        results.append(exedict)
        results.append(self.tasksSlackTimes)
        results.append(brokenDeadlinesdict)
        results.append(negativeSlackdict)

        for task in tasks:
           print(f"{task.taskName} execute (from, to): {task.executionTimes}")
           if task.negativeSlackTimes:
               print(f"{task.taskName} negative slack times (time slack time calculated, slack time): {task.negativeSlackTimes} ")
               print(task.brokenDeadlines)
        print(f"([slack time of each task], time slack calculated): {self.tasksSlackTimes}")

        return results

class Task:
    def __init__(self, taskName, releaseTime, period, executionTime, deadLine, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        #assuming that the period of a task is the same as its deadline
        self.period = period
        # executionTime of task.
        self.executionTime = executionTime
        # remaining of executionTime
        self.remainingExecution = 0
        # deadLine of a task.
        self.deadLine = deadLine
        self.deadlineBroken = False
        # list of times where a new job of the task is ready to execute.
        self.readyTimes = [time for time in rangeFloat(self.releaseTime, maxTime+1, self.period)]
        self.readyTimes.append(self.readyTimes[-1] + period)
        #list that contain all deadline of the task during execution
        self.deadlines = [time + self.deadLine for time in self.readyTimes]
        #list that contains times of execution
        self.executionTimes = []
        # list that contains the times where slack time of a task is a negative number
        self.negativeSlackTimes = []
        self.brokenDeadlines = []
    def calcSlackTime(self, t):
        # if task has already finished execution means there is no need to calculate its slack time and return -1
        if self.remainingExecution!=0:
            # if there is sill remaining execution time we calculate the slack time of the task then return it.
            slackTime = (self.deadLine - t)-self.remainingExecution
            if slackTime<0:
                self.negativeSlackTimes.append((t, slackTime)) # broken deadlines
            return slackTime
        return None

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadLine = deadline
                break

maxtime = 28
tasks = [Task("T1", 0, 4, 1.5, 4,maxtime), Task("T2", 0, 10, 3, 10,maxtime), Task("T3",0,12,3, 12,maxtime)]
mlf = OS(tasks, maxtime)
#uncomment the below line to get the results in the CLI
mlf.getResults()