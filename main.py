import time as tm
from threading import Thread

class Notification:
    def __init__(self):
        pass

    @staticmethod
    def showNotify(task):
        print(f'\nNotify: Time Up: {task}')


class Time:
    def __init__(self, time):
        self.__hour, self.__minute, self.__second = self.__extract(time)
        self.val = self.__timeVal()
        self.__time = f'{self.__hour:02}:{self.__minute:02}:{self.__second:02}'

    @staticmethod
    def __extract(time):
        timeObj = map(int, time.split(':'))
        return timeObj
    
    @staticmethod
    def __calcVal(val):
        h = val // 3600
        m = (val % 3600) // 60
        s = (val % 3600) % 60
        return f'{h:02}:{m:02}:{s:02}'
    
    def __timeVal(self):
        val = self.__hour * 3600
        val += self.__minute * 60
        val += self.__second
        return val   
        
    def __sub__(self, other):
        if isinstance(other, Time):
            val = abs(self.val - other.val)
            return Time(self.__calcVal(val))
        elif isinstance(other, Task):
            val = abs(self.val - int(other))
            return Time(self.__calcVal(val))
    
    def __add__(self, other):
        val = self.val + other.val
        return Time(self.__calcVal(val))
    
    def __int__(self):
        return self.val
    
    def __eq__(self, other):
        return self.val == other.val
    
    def __repr__(self):
        return repr(self.__time)


class Task:
    def __init__(self, task: str, time: Time):
        self.__task = task
        self.__time = time

    def __int__(self):
        return int(self.__time)
    
    def __repr__(self):
        return repr(f'Task: {self.__task} | Time: {self.__time}')
    
    def __getitem__(self, key):
        if key.lower() == 'task':
            return self.__task
        elif key.lower() == 'time':
            return self.__time

class QueueTask:
    def __init__(self):
        self.__taskList    : list         = []
        self.__notification: Notification = Notification()
        self.__curNotify   : Task         = None

        Thread(target=self.start, daemon=True).start()

    def start(self):
        while True:
            if (self.__curNotify is None) and (self.__taskList):
                self.__curNotify = self.__selectTask()
                if self.__curNotify:
                    print(f'\nTask: {self.__curNotify["task"]}: START')
            if (self.__curNotify) and self.isTimeUp():
                self.notify()
            

    def addTask(self, task: Task):
        if (self.__taskList is None) or (self.__curNotify is None):            
            self.__taskList.append(task)
        elif int(self.__curNotify['time'] - task['time']) >= 1500:
            self.__taskList.append(task)
        else:
            print('Warning: Task must be 25 minutes after current task')


    def __selectTask(self):
        timeNow = Time(tm.strftime('%H:%M:%S'))
        selected = min(self.__taskList, key=int)
        if int(timeNow - selected) == 0:
            return selected
        return None

    def isTimeUp(self, time=None):
        if self.__curNotify:
            if time is None:
                time = Time(tm.strftime('%H:%M:%S'))
            return int(time - self.__curNotify['time']) >= 1500
        return False

    def notify(self):
        self.__notification.showNotify(self.__curNotify['task'])
        self.__taskList.remove(self.__curNotify)
        self.__curNotify = None
        

class TaskManagement:
    def __init__(self):
        self.__queueTask: QueueTask = QueueTask()
    
    def setTask(self, taskName: str, time: Time):
        task = Task(taskName, time)
        self.__queueTask.addTask(task)
        print(f"[+] Task '{taskName}' added with time {time}")

    def rejectTask(self, taskName: str):
        for task in self.__queueTask._QueueTask__taskList:
            if task['task'].strip().lower() == taskName.strip().lower():
                self.__queueTask._QueueTask__taskList.remove(task)
                print(f"[+] Task '{taskName}' rejected and removed from the queue.")
                return
        print(f"[+] Task '{taskName}' not found in the queue.")


class Controller:
    def __init__(self):
        self.__taskManager = TaskManagement()

    def start(self):
        while True:
            print('-' * 20)
            print('1. Add Task\n2. Reject Task\n3. Exit')
            print('-' * 20)
            choice = input('Choose an option: ')
            if choice.strip() == '1':
                taskName = input('Enter Task Name: ')
                taskTime = input('Enter Task Time (HH:MM:SS): ')
                try:
                    taskTimeObj = Time(taskTime)
                    self.__taskManager.setTask(taskName, taskTimeObj)
                except:
                    print('Error: Invalid time format!')
            elif choice.strip() == '2':
                taskName = input('Enter Task Name To Reject: ')
                self.__taskManager.rejectTask(taskName)
            elif choice.strip() == '3':
                exit()


def main():
    userInterface = Controller()
    userInterface.start()


if __name__ == '__main__':
    main()