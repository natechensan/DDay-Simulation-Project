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
        self.bunkers = []
        self.cells = []
        self.loadDoc()

        return

    def loadDoc(self):
        
        bunkerFile = open("image/sword_target.txt")
        bid = 4
        for line in bunkerFile:
            tmp = Bunker(bid, literal_eval(line))
            self.bunkers.append(tmp)
            bid += 1

        mapfile = open("image/sword.txt")
        row = 0
        for line in mapfile:
            col = 0
            tmp = line.split(" ")[:-1]
            row_cell = []
            for t in tmp:
                ctype = int(t)
                if ctype > 3:
                    target = Target(ctype, ctype, row, col, -1, ctype)
                    row_cell.append(target)
                else:
                    cell = Cell(row, col, -1, ctype)
                    row_cell.append(cell)
                col+=1
            row+=1
            self.cells.append(row_cell)

        # print(self.cells)

        self.soldiers = []
        for i in range(100):
            tmp = Soldier(-1, 1000, i, self.bunkers)
            self.soldiers.append(tmp)
            self.cells[tmp.unit_x][tmp.unit_y].walkable = 0


        return
    
    def run_simulation(self):
        self.state='running'
        self.steps = 0
        self.ped_count = 0
        print ('simulation starts')
        self.execute()
        return

    def bunkersLeft(self):
        for b in self.bunkers:
            if b.dead == False:
                return True
        return False

    def execute(self):
        while(self.bunkersLeft() == True):
            self.step()
        
        self.stop_simulation()
    
    def step(self):

        for s in self.soldiers:
            if self.bunkers[s.target].dead == True:
                s.findPath(self.bunkers)
            s.move(self.cells, self.bunkers)
            cur_cell = self.cells[s.unit_x][s.unit_y]
            if cur_cell.cell_type > 3:
                self.bunkers[cur_cell.cell_type-4].dead = True

        print ((self.soldiers[0].unit_x, self.soldiers[0].unit_y))

        return
        

    def stop_simulation(self):
        self.state='stopped'
        print ('simulation over')
        total_time = self.steps * 0.3
        print ('total evacuation time: '+str(total_time)+' seconds')


class Cell(object):
    def __init__(self,x_pos,y_pos,cellID, cell_type, cones=None, walkable=1):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.cellID=cellID   #seperate CellID and genID and TargetID, so that we can loop through them seperately
        self.cell_type=cell_type
        self.walkable=walkable #only cell has walkability, cuz there is no obstacle cells in the csv file
        # self.neighbors = neighbors
        # self.FFs = FFs
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

class Bunker:
    def __init__(self, bID, center):
        self.bID = bID
        self.health = 100
        self.center = center
        self.dead = False
        
     
class Soldier: 
    def __init__(self, sID, unit_x, unit_y, targets):
        self.sID = sID
        self.unit_x=unit_x
        self.unit_y=unit_y

        self.likeability = []

        #randomize attributes here
        self.speed = 0
        self.health = 100
        self.injured = False
        self.morale = 100

        self.stay = 0 #count turns stayed

        self.findPath(targets)

    def findPath(self, targets):
        # distance = pow((targets[0].center[0] - self.unit_x), 2) + pow((targets[0].center[1] - self.unit_y), 2)
        distance = 999999
        self.target = -1
        for i in range(len(targets)):
            if targets[i].dead == True:
                continue
            newd = pow((targets[i].center[0] - self.unit_x), 2) + pow((targets[i].center[1] - self.unit_y), 2)
            if newd < distance:
                distance = newd
                self.target = i
        self.dx = targets[self.target].center[0] - self.unit_x
        self.dy = targets[self.target].center[1] - self.unit_x

    def move(self, cells, targets):
        preference = []
        diag_prob = 0.5*abs(float(self.dx)/self.dy) # 50% diagonal if dx == dy
        preference.append(diag_prob)
        dx_dy = abs(self.dx)+abs(self.dy)
        prob = (1-diag_prob)*(abs(float(self.dx))/(abs(self.dx)+abs(self.dy)))
        preference.append(prob)
        prob = (1-diag_prob)*(abs(float(self.dy))/(abs(self.dx)+abs(self.dy)))
        preference.append(prob)
        preference.sort()

        # below should change to likablilty
        for p in preference:
            newCell = [0]*2
            if p == diag_prob: #diagonal
                if self.unit_x < targets[self.target].center[0]:
                    newCell[0] = self.unit_x + 1
                else:
                    newCell[0] = self.unit_x - 1
                if self.unit_y < targets[self.target].center[1]:
                    newCell[1] = self.unit_y + 1
                else:
                    newCell[1] = self.unit_y - 1

            elif p == prob: #vertical
                newCell[0] = self.unit_x
                if self.unit_y < targets[self.target].center[1]:
                    newCell[1] = self.unit_y + 1
                else:
                    newCell[1] = self.unit_y - 1

            else: #horizontal
                newCell[1] = self.unit_y
                if self.unit_x < targets[self.target].center[0]:
                    newCell[0] = self.unit_x + 1
                else:
                    newCell[0] = self.unit_x - 1

            if cells[newCell[0]][newCell[1]].walkable < 1:
                continue
            else:
                cells[self.unit_x][self.unit_y].walkable = 1;
                self.unit_x = newCell[0]
                self.unit_y = newCell[1]
                cells[self.unit_x][self.unit_y].walkable = 0;
                break

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

    
    
    