class mobAi():
	def __init__(self, client):
		self.client = client

	def Move(self,x,y):
		self.client.movePos(x,y)

	def Attack(self,dir):
		if self.client.weapon:
			self.client.weapon.triggerMain(dir)

	def Special(self,dir):
		if self.client.weapon:
			self.client.weapon.triggerSecondary(dir)

