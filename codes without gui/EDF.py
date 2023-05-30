def rangeFloat(start, end, step):
    # this function is the same as range function the difference is that this function accepts float values
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
        # list of tasks
        self.tasks = tasks
        # maximum time of execution
        self.maxtime = maxtime
        #list containing the Deadlines calculated of each task during the whole execution
        self.tasksDeadlineTimes =[]
        #curent time in execution
        self.currentTime = 0
        #list of tasks to be executed
        self.executeList = []
        # execute as long as the current execution time is less than the maximum time required
        while self.currentTime < maxtime:
            # getting the task with the minimum deadline time
            minDeadlineTask = self.getMinDeadlineTask()
            # executing the task with the minimum deadline time
            self.execute(minDeadlineTask)



    def getMinDeadlineTask(self):
        # list to contain the deadline time for each task at the current execution time
        tasksDeadlineTime =[]
        # list containing the nearest ready time of each task
        tasksReadyTimes = [(task, task.readyTimes[0]) for task in self.tasks]
        # when ready time of task has passed: (append task to execute list, refill remaining execution of task, append deadline of task to tasksDeadlineTime list)
        for task, readytime in tasksReadyTimes:
            if readytime <= self.currentTime:
                self.executeList.append(task)
                task.readyTimes.pop(0)
                task.remainingExecution = task.executionTime
            #task.updateDeadline(self.currentTime)
            tasksDeadlineTime.append(task.getDeadline())

        # making a copy of the tasksDeadline list
        tasksDeadlineTime2 = tasksDeadlineTime.copy()
        # removing deadline time of tasks that has no remaining execution at the current execution time from the copied list
        for taskDeadlinetime in tasksDeadlineTime:
            # if deadline time of a task = None indicates that the task remaining execution time = 0
            if taskDeadlinetime==None:
                tasksDeadlineTime2.remove(None)

        # if there is no item in the copied list means that at the current execution time there will be no task running
        if not tasksDeadlineTime2:
            # updating current execution time to the nearest job of task to be ready to be executed
            tasksNextReadyTime = [task.readyTimes[0] for task in self.tasks]
            self.currentTime = min(tasksNextReadyTime)

            # updating remaining execution time of tasks that has job at the current time renewed
            self.updateTasksRemainingExecution()
            # after updating the current execution time we call the function again to provide the min deadline time task to the execution
            return self.getMinDeadlineTask()


        # getting the minimum deadline time task
        minDeadlineIndex= tasksDeadlineTime.index(min(tasksDeadlineTime2))
        # saving information of the deadline times of each task
        self.tasksDeadlineTimes.append((tasksDeadlineTime, self.currentTime))

        return self.tasks[minDeadlineIndex]

    def updateTasksRemainingExecution(self):
        # looping for each task
        for task in self.tasks:
            # when the nearest ready time of task has passed update the remaining execution, execute list,
            if task.readyTimes[0] <= self.currentTime:
                if task.remainingExecution == 0 or task.deadlineBroken:
                    self.executeList.append(task)
                    task.remainingExecution = task.executionTime
                    task.readyTimes.pop(0)
                task.updateDeadline(self.currentTime)

    def execute(self, task):
        # defining start time and end time of execution of the task
        startTime = self.currentTime

        # calling getTimeToStop function to calculate when the task will stop execution
        endTime = self.getTimeToStop(task)

        #updating the task remaining execution time
        task.remainingExecution -= (endTime-startTime)
        #ensuring end time doesn't pass the max time
        if endTime > self.maxtime:
            task.executionTimes.append([startTime, self.maxtime])
        else:
            task.executionTimes.append([startTime, endTime])
        #when task remaining execution =0 remove task from the execution list
        if task.remainingExecution == 0:
            self.executeList.remove(task)
        #checking if task has passed its deadline after execution
        self.checkDeadline(endTime)
        # after execution the current execution time updated to the end time of the task
        self.currentTime = endTime
        #checking if any task requires any refilling of remaining execution
        self.updateTasksRemainingExecution()



    def getTimeToStop(self, task):
        # creating a list to contain the nearest ready time to be executed for each task ()
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
        brokenDeadlinesdict = {}
        for task in self.tasks:
            exedict[f"{task.taskName}"]= task.executionTimes
            brokenDeadlinesdict[f"{task.taskName}"] = task.brokenDeadlines
        results.append(exedict)
        results.append(self.tasksDeadlineTimes)
        results.append(brokenDeadlinesdict)
        for task in tasks:
           print(f"{task.taskName} execute (from, to): {task.executionTimes}")
           if task.brokenDeadlines:
               print(task.brokenDeadlines)
        print(f"([Deadline time of each task], time deadline calculated): {self.tasksDeadlineTimes}")

        return results

class Task:
    def __init__(self, taskName, releaseTime, period, executionTime, deadLine, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
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
        #list that contains any broken deadlines
        self.brokenDeadlines = []

    def getDeadline(self):
        if self.remainingExecution != 0:
            return self.deadLine
        return None

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadLine = deadline
                break

maxtime = 10
tasks = [Task("T1", 0, 2, 1, 2,maxtime), Task("T2", 0, 5, 3, 5,maxtime)]
edf = OS(tasks, maxtime)
#uncomment the below line to get the results in the CLI
#edf.getResults()