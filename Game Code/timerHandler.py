class timerHandler():
    def __init__(self):
        self.timers = []

    def Update(self):
        for i in self.timers:
            if i.life == 0:
                i.deathFunc(*i.args)
                self.removeTimer(i)
                continue
            i.life -= 1

    def addTimer(self,timer):
        self.timers.append(timer)

    def removeTimer(self,timer):
        del self.timers[self.timers.index(timer)]

class Timer():
    def __init__(self,life,deathFunc,args,handler):
        self.life = life
        self.deathFunc = deathFunc
        self.args = args
        handler.addTimer(self)

Kronos = timerHandler()
