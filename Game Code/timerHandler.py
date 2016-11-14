class timerHandler():
    def __init__(self):
        self.timers = []

    def Update(self):
        for i in self.timers:
            if i.life == 0:
                i.deathFunc()
                self.removeTimer(i)
                continue
            i.life -= 1

    def addTimer(self,timer):
        self.timers.append(timer)

    def removeTimer(self,timer):
        del self.timers[self.timers.index(timer)]

class timer():
    def __init__(self,life,deathFunc,handler):
        self.life = life
        self.deathFunc = deathFunc
        handler.addTimer(self)

Kronos = timerHandler()
def testfunc():
    print "hello"
test = timer(6000,testfunc,Kronos)
