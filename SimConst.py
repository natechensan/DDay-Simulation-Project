class SimConst:
	'''
	Constants for the simulation
	'''
	def __init__(self):
		self.RandomSeed = 100

		self.Bunker_Default_Shots = 100
		self.Bunker_Max_Health = 100
		self.Bunker_Health_Decrease_Max = 3
		self.Bunker_Health_Decrease_Min = 1

		self.Soldier_Health_Decrease_Max = 3
		self.Soldier_Health_Decrease_Min = 1
		self.Soldier_Health_Decrease_At_Bunker_Max = 30
		self.Soldier_Health_Decrease_At_Bunker_Min = 30

		self.Default_Cone_Value = -1