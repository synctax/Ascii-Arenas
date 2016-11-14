import Item

class Inventory():
    def __init__(self,size):
        self.size = size
        self.freeSpace = size
        self.items = self.populateList()

    def populateList(self):
        set = {}
        for i,v in enumerate(Item.allItems.keys()):
            set[v] = {"AMOUNT": 0, "STACKABLE":Item.allItems[v].data["STACKABLE"]}
        return set

    def addItem(self,itemName,amount):      #returns the amount of items not accepted
        if self.items[itemName]["STACKABLE"]:
            if self.items[itemName]["AMOUNT"] == 0:
                self.freeSpace -= 1
            self.items[itemName]["AMOUNT"] += 1
            return 0
        amountTaken = min(self.freeSpace,amount)
        self.items[itemName]["AMOUNT"] += amountTaken
        self.freeSpace -= amountTaken
        return amount - amountTaken

    def removeItem(self,itemName, amount):
        if self.items[itemName]["STACKABLE"]:
            if self.items[itemName]["AMOUNT"] > amount:
                self.items[itemName]["AMOUNT"] -= amount
                amountTaken = amount
                if self.items[itemName]["AMOUNT"] <= amount:
                    amountTaken = amount - self.items[itemName]["AMOUNT"]
                    self.items[itemName]["AMOUNT"] = 0
                    if self.items[itemName]["STACKABLE"]:
                        self.freeSpace += 1
            if not self.items[itemName]["STACKABLE"]:
                self.freeSpace += amountTaken
            return amountTaken
