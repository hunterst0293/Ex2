import math

class Ratemonotonic:
    def __init__(self, taskId, executionTime, period):
        self.taskId = taskId
        self.executionTime = executionTime
        self.period = period
        self.remainingTime = executionTime
        self.nextDeadline = period
        self.completionTimes = []
        self.turnaroundTime = 0
        self.waitingTime = 0
        self.throughput = 0
        self.cpuUtilization = 0
        self.addTime = 0
    
    @staticmethod
    def RMS(tasks, simulationTime):
        tasks.sort(key=lambda x: x.period)  # Sort tasks by period
        time = 0
        schedule = []
        cpuBusyTime = 0

        while time < simulationTime:
            # Find the task with the shortest period
            runnableTasks=[task for task in tasks if task.remainingTime > 0 and time < task.nextDeadline]
            if runnableTasks:
                currentTask = min(runnableTasks, key=lambda x: x.period)
                schedule.append((time, currentTask.taskId))
                currentTask.remainingTime -= 1
                cpuBusyTime += 1
                task.addTime += 1

                if currentTask.remainingTime == 0:
                    currentTask.completionTimes.append(time + 1)
            else:
                schedule.append((time, "Idle"))
                
            time += 1
            for task in tasks:
                if time == task.nextDeadline:
                    if task.remainingTime > 0:
                        print(f"Task {task.taskId} missed its deadline at time {time}.")
                    task.remainingTime = task.executionTime
                    task.nextDeadline += task.period

        totalTurnaroundTime = 0
        totalWaitingTime = 0
        totalTasksCompleted = 0

        print ("Task Info:\n")
        for task in tasks:
            if task.completionTimes:
                turnaroundTime = sum(task.completionTimes) - len(task.completionTimes) * task.period
                waitingTime = turnaroundTime - (len(task.completionTimes) * task.executionTime)
                totalTurnaroundTime += turnaroundTime
                totalWaitingTime += waitingTime
                totalTasksCompleted += len(task.completionTimes)

                print(f"Task {task.taskId}:")
                print(f" Turnaround Time = {turnaroundTime}")
                print(f" Waiting Time = {waitingTime}")

        avgTurnaroundTime = totalTurnaroundTime / totalTasksCompleted if totalTasksCompleted > 0 else 0
        avgWaitingTime = totalWaitingTime / totalTasksCompleted if totalTasksCompleted > 0 else 0
        throughput = totalTasksCompleted / simulationTime
        cpuUtilization = cpuBusyTime / simulationTime * 100

        print(f"\nAverage Turnaround Time: {avgTurnaroundTime}")
        print(f"Average Waiting Time: {avgWaitingTime}")
        print(f"Throughput: {throughput} tasks/unit time")
        print(f"CPU Utilization: {cpuUtilization}%")

        return schedule
    
if __name__ == "__main__":
    tasks = [
        Ratemonotonic('T1', 1, 2),
        Ratemonotonic('T2', 2, 5),
        Ratemonotonic('T3', 1, 8),
    ]

    for i in range(len(tasks)):
        print(f"Task {tasks[i].taskId}: Execution Time = {tasks[i].executionTime}, Period = {tasks[i].period}")

    schedule = Ratemonotonic.RMS(tasks, 20)

    print("Time | Task")
    print("-----------")
    for time, taskNum in schedule:
        print(f"{time:4} | {taskNum}")