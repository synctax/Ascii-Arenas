import timerHandler as TH
import Player_Class as pc

class Item():
    def __init__(self,filename,effects):
        self.file = "../Items/"+filename
        self.data = self.fromFile(self.file)
        self.effects = effects

    def fromFile(self,filename):
    	newFile = open(file,'r')
    	data = json.load(newFile)
    	newFile.close()
        return data

    def onUse(self):
        if self.data["USABLE"]:
            for i,v in enumerate(self.data["EFFECTS"].keys()):
                self.effects[v].doEffect(self.data["EFFECTS"][v],pc.mainPlayer,pc.world.players)



class itemEffect():
    def __init__(self,argList,function):
        self.function = function
        self.argList = argList

    def doEffect(self,args,user,allusers):
        funcArgs = []
        target = {"ALL":allusers,"USER":user,"NOT_USER":allusers[1:]}[args["TARGET"]] #requires that the user is 1st in all users
        for i,v in enumerate(self.argList):
            if args[v]:
                funcArgs.append(args[v])
        funcArgs.append(target)
        tuple(funcArgs)
        self.function(*funcArgs)

def heal(health,duration,frequency,target):
    def a(t,h):
        t.stats["HEALTH"] += h
    for i in range(0,int(duration/frequency)+1):
        TH.Timer(i*duration/frequency,a,(target,health), TH.Kronos)

healingEffect = itemEffect(["HEALTH","DURATION","FREQUENCY"],heal)
allEffects = {"PLAYER_HEAL":healingEffect}
