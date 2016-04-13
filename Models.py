# from gen_ped import gen_ped
from ast import literal_eval
import sys

class Simulation:
    '''
    This class handles the main simulation events 
    '''

    def __init__(self,state='sleep',time_elapsed=0):
        self.state=state
        self.time_elapsed=time_elapsed


    def warmup(self):
        '''
        handles initial random generation and loading the documents
        '''

        return

    def loadDoc(self):
        return
    
    def run_simulation(self):
        self.state='running'
        self.steps = 0
        self.ped_count = 0
        print ('simulation starts')
        self.execute()
        return

    def execute(self):
        self.stop_simulation()
    
    def step(self):
        return

    def check_targets(self):
        k = self.targets.keys()
        return self.targets[list(k)[0]][0].check_this_target()
        

    def stop_simulation(self):
        self.state='stopped'
        print ('simulation over')
        total_time = self.steps * 0.3
        print ('total evacuation time: '+str(total_time)+' seconds')


class Cell(object):
    def __init__(self,x_pos,y_pos,cellID, cell_type, FFs, neighbors, cones, walkable=1):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.cellID=cellID   #seperate CellID and genID and TargetID, so that we can loop through them seperately
        self.cell_type=cell_type
        self.walkable=walkable #only cell has walkability, cuz there is no obstacle cells in the csv file
        self.neighbors = neighbors
        self.FFs = FFs
        self.cones = cones

class Generator(Cell):
    def __init__(self, shipID, *args):
        super(Generator, self).__init__(*args)
        self.shipID = shipID

class Target(Cell):
    def __init__(self, targetID, bunkerID, *args):
        super(Target, self).__init__(*args)
        self.targetID=self.cell_type
        self.bunkerID = bunkerID

class Land(Cell):
    def __init__(self, height, *args): 
        super(Land, self).__init__(*args)
        self.height = height
        
        
     
class Soldier: 
    def __init__(self, sID, unit_x, unit_y):
        self.sID = sID
        self.unit_x=unit_x
        self.unit_y=unit_y

        self.target = -1 # target dynamically changes during simulation

        self.likeability = []

        #randomize attributes here
        self.speed = 0
        self.health = 100
        self.injured = False
        self.morale = 100

        self.stay = 0 #count turns stayed


class Ship:
    def __init__(self, shipID, unit_x, unit_y, armyID):
        self.unit_x=unit_x
        self.unit_y=unit_y
        self.shipID = shipID
        self.armyID = armyID

class Turret:
    def __init__(self, tID, damage):
        self.tID = tID
        self.damage = damage
    
class Formulae:
    def calc_targetcomp(self,p):
        return

    
    
    