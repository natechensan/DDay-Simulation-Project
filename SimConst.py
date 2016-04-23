class SimConst:
	'''
	Constants for the simulation
	'''
	def __init__(self):

		# RNG
		self.RandomSeed = 100

		# Bunkers
		self.Bunker_Default_Shots = 100
		self.Bunker_Max_Health = 100
		self.Bunker_Health_Decrease_Max = 3
		self.Bunker_Health_Decrease_Min = 1
		self.Bunker_Damaged_Chance = 0.95
		self.Bunker_Default_Health = 1000

		# Soldiers
		self.Soldier_Default_Health = 100
		self.Soldier_Health_Decrease_Max = 3
		self.Soldier_Health_Decrease_Min = 1
		self.Soldier_Health_Decrease_At_Bunker_Max = 30
		self.Soldier_Health_Decrease_At_Bunker_Min = 30
		self.Soldier_Damaged_Chance = 0.95
		self.Soldier_Damaged_Chance_At_Bunker = 0.05

		#Ship
		self.Ship_Speed = 5

		# Cells
		self.Default_Cone_Value = -1

		#Generators
		self.Soldier_per_Generator = 30