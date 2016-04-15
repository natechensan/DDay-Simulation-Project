# from gen_ped import gen_ped
from ast import literal_eval
import sys
import random

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
        self.steps = 0
        self.bunkers = []
        self.cells = []
        random.seed(100)
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

        conefile = open("image/sword_cone.txt")

        bid = 4
        for line in conefile:
            coords = line.split(";")[:-1]
            for c in coords:
                cone = literal_eval(c)
                self.cells[cone[0]][cone[1]].cone = bid
            bid+=1


        # print(self.cells)

        self.soldierCount = 0
        self.soldierHead = None
        self.soldierTail = None
        for i in range(2000):
            tmp = Soldier(-1, 1000, i, self.bunkers)
            if self.soldierHead == None:
                self.soldierHead = tmp
                self.soldierTail = tmp
            else:
                self.soldierTail.next = tmp
                tmp.prev = self.soldierTail
                self.soldierTail = tmp
            # self.soldiers.append(tmp)
            self.cells[tmp.unit_x][tmp.unit_y].walkable = 0
            self.soldierCount += 1


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
        while(self.bunkersLeft() == True and self.soldierCount > 50):
            self.step()
        
        self.stop_simulation()
    
    def step(self):

        if self.steps % 200 == 0:
            print (str(self.soldierCount)+" soldiers left.")

        s = self.soldierHead
        while s != None:
            if self.bunkers[s.target].dead == True:
                s.findPath(self.bunkers)
            s.move(self.cells, self.bunkers)
            cur_cell = self.cells[s.unit_x][s.unit_y]
            
            if cur_cell.cone > -1 and self.bunkers[cur_cell.cone-4].dead == False:
                if(random.random() > 0.95):
                    s.health -= random.randint(5, 15)
                else:
                    cur_cell.cone = -1

            if cur_cell.cell_type > 3 and self.bunkers[cur_cell.cell_type-4].dead == False:
                self.bunkers[cur_cell.cell_type-4].dead = True
                print ("bunker "+str(cur_cell.cell_type)+" is dead.")
                print (str(self.soldierCount)+" soldiers left.")

            if s.health <= 0:
                tmp = s.next
                if s.prev != None:
                    s.prev.next = s.next
                if s.next != None:
                    s.next.prev = s.prev
                s.prev = None
                s.next = None
                s = tmp
                self.soldierCount -= 1
                continue

            s = s.next

        self.steps += 1

        # print ((self.soldiers[0].unit_x, self.soldiers[0].unit_y))

        return
        

    def stop_simulation(self):
        self.state='stopped'
        print ('simulation over')
        print ('battle lasted: '+str(self.steps)+' seconds')
        if self.soldierCount <= 50:
            print("Germans win. Damn!")
        else:
            print("Allies win!")


class Cell(object):
    def __init__(self,x_pos,y_pos,cellID, cell_type, walkable=1):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.cellID=cellID   #seperate CellID and genID and TargetID, so that we can loop through them seperately
        self.cell_type=cell_type
        self.walkable=walkable #only cell has walkability, cuz there is no obstacle cells in the csv file
        # self.neighbors = neighbors
        # self.FFs = FFs
        self.cone = -1

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

        self.prev = None
        self.next = None

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
        diag_prob = 0.4 # 40% diagonal if dx == dy
        preference.append(diag_prob)
        dx_dy = abs(self.dx)+abs(self.dy)
        prob = (1-diag_prob)*(abs(float(self.dx))/(abs(self.dx)+abs(self.dy)))
        preference.append(prob)
        prob = 1-prob-diag_prob
        preference.append(prob)
        preference.sort(reverse=True)

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

    
    
    