# from gen_ped import gen_ped
from ast import literal_eval
import sys
import random
from bisect import bisect
from ExportImage import exportImage

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
            tmp = Bunker(bid - 4, literal_eval(line))
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
                self.cells[cone[1]][cone[0]].cone = bid - 4
            bid+=1


        # print(self.cells)

        self.soldierCount = 0
        self.soldierHead = None
        self.soldierTail = None
        for i in range(2000):
            tmp = Soldier(-1, i, 1100, self.bunkers)
            if self.soldierHead == None:
                self.soldierHead = tmp
                self.soldierTail = tmp
            else:
                self.soldierTail.next = tmp
                tmp.prev = self.soldierTail
                self.soldierTail = tmp
            # self.soldiers.append(tmp)
            self.cells[tmp.unit_y][tmp.unit_x].walkable = 0
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
                s.findTarget(self.bunkers)
            s.move(self.cells, self.bunkers)
            cur_cell = self.cells[s.unit_y][s.unit_x]
            
            if cur_cell.cone > -1 and self.bunkers[cur_cell.cone].dead == False:
                if(random.random() > 0.95):
                    s.health -= random.randint(1, 3) # (5, 15)

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



        if self.steps % 10 == 0:
            testfi2 = open("images2/test" + str(int(self.steps / 10)) + '.csv', 'w')
            temp = self.soldierHead
            while temp != None:
                testfi2.write(str(temp.unit_x)+','+str(temp.unit_y)+'\n')
                temp = temp.next
            testfi2.close()
            exportImage(int(self.steps / 10))


            

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

        self.findTarget(targets)

        self.prev = None
        self.next = None

    def findTarget(self, targets):
        # distance = pow((targets[0].center[0] - self.unit_x), 2) + pow((targets[0].center[1] - self.unit_y), 2)
        distance = 999999
        self.target = -1
        for t in targets:
            if t.dead == True:
                continue
            newd = pow((t.center[0] - self.unit_x), 2) + pow((t.center[1] - self.unit_y), 2)
            if newd < distance:
                distance = newd
                self.target = t.bID
        # self.dx = targets[self.target].center[0] - self.unit_x
        # self.dy = targets[self.target].center[1] - self.unit_y

    def move(self, cells, targets):
        dx = float(targets[self.target].center[0] - self.unit_x)
        dy = float(targets[self.target].center[1] - self.unit_y)
        dxa = abs(dx)
        dya = abs(dy)
        probs = [0.0] * 8
        maxDiagProb = 0.6 # Tunable
        randomProb = 0.1 # Tunable

        if dxa == 0 and dya == 0:
            return

        pd = maxDiagProb * 2 * min(dxa, dya) / (dxa + dya)
        if dx < dy:
            px = (1 - maxDiagProb - randomProb) * dxa / (dxa + dya)
            py = 1 - randomProb - pd - px
        else:
            py = (1 - maxDiagProb - randomProb) * dya / (dxa + dya)
            px = 1 - randomProb - pd - py

        if dx >= 0 and dy >= 0:
            probs[7] = pd
            probs[4] = px
            probs[6] = py
        elif dx >= 0 and dy < 0:
            probs[2] = pd
            probs[4] = px
            probs[1] = py
        elif dx < 0 and dy < 0:
            probs[0] = pd
            probs[3] = px
            probs[1] = py
        elif dx < 0 and dy >= 0:
            probs[5] = pd
            probs[3] = px
            probs[6] = py

        for i in range(10):
            rng = random.randint(0, 7)
            probs[rng] += randomProb / 10

        cdf = [probs[0]]
        for i in range(1, len(probs)):
            cdf.append(cdf[-1] + probs[i])
        rng = random.random()
        for i in range(8):
            decision = i
            if rng < cdf[i]:
                break

        nx = self.unit_x
        ny = self.unit_y

        if decision == 0:
            nx = self.unit_x - 1
            ny = self.unit_y - 1
        elif decision == 1:
            ny = self.unit_y - 1
        elif decision == 2:
            nx = self.unit_x + 1
            ny = self.unit_y - 1
        elif decision == 3:
            nx = self.unit_x - 1
        elif decision == 4:
            nx = self.unit_x + 1
        elif decision == 5:
            nx = self.unit_x - 1
            ny = self.unit_y + 1
        elif decision == 6:
            ny = self.unit_y + 1
        elif decision == 7:
            nx = self.unit_x + 1
            ny = self.unit_y + 1

        if cells[ny][nx].walkable != 0:
            cells[self.unit_y][self.unit_x].walkable = 1;
            self.unit_x = nx
            self.unit_y = ny
            cells[self.unit_y][self.unit_x].walkable = 0;

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

    
    
    