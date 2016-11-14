class Item():
    def __init__(self,filename):
        self.file = "../Items/"+filename
        self.data = self.fromFile(self.file)

    def fromFile(self,filename):
    	newFile = open(file,'r')
    	data = json.load(newFile)
    	newFile.close()
        return data

class itemEffect():
    def __init__(self,argList,function,user,allusers):
        self.functions = functions
        self.argList = argList

    def doEffect(self,args):
        funcArgs = []
        self.target = {"ALL":allusers,"USER":user,"NOT_USER":allusers[1:]}[args["TARGET"]]
        for i,v in enumerate(self.argList):
            if args[v]:
                funcArgs.append(args[v])
        tuple(funcArgs)
        self.functions(*funcArgs)
