import Item

class Inventory():
    def __init__(self,size):
        self.size = size
        self.freeSpace = size
        self.occupiedItems = {"NON_STACKABLE":[]}
        self.items = Item.allItems


    def addItem(self,itemName,amount):      #returns the amount of items not accepted
        if self.items[itemName].data["STACKABLE"]:
            if self.occupiedItems.has_key(itemName):
                self.occupiedItems[itemName] += amount
                return 0
            if self.freeSpace > 0:
                self.occupiedItems[itemName] = amount
                return 0
            return amount
        amountTaken = min(self.freeSpace,amount)
        for i in range(0,amountTaken+1):
            self.occupiedItems["NON_STACKABLE"].append(itemName)
        return amount - amountTaken


    def removeItem(self,itemName, amount):
        return True
