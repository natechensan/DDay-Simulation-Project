from sys import maxint
from sets import Set

class Cell:
	def __init__(self, ctype):
		self.cell_type = ctype
		self.fields = [9999.0]*11
		self.neighbors = []
		self.xy = ()

mapfile = open("image/gold.txt", "r+")
data = []
for line in mapfile:
	data.append(line.split(" ")[:-1])

bunkers = {}
cells = []

for i in range(len(data)):
	row = []
	for j in range(len(data[0])):
		c = int(data[i][j])
		cell = Cell(c)
		row.append(cell)
		if c > 3:
			if c in bunkers.keys():
				bunkers[c].append((i,j)) # row, col
			else:
				bunkers[c] = [(i,j)]
	cells.append(row)

print "done loading map"

for tgroup in bunkers.keys(): #group of bunkers
	for t in bunkers[tgroup]: #each target in group
		print t
		visited = [[False for x in range(len(cells[0]))] for y in range(len(cells))]
		queue = []
		cur = None
		queue.append(t)
		visited[t[0]][t[1]] = True
		cells[t[0]][t[1]].fields[tgroup-4] = 0

		while len(queue) > 0:
			cur = queue[0]
			queue = queue[1:]
			cells[cur[0]][cur[1]].xy = (cur[0], cur[1])

			if cur[0] > 0:
				newNeighbor = (cur[0]-1, cur[1])
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]-1][cur[1]] and cells[cur[0]-1][cur[1]].cell_type > 0:
					queue.append((cur[0]-1,cur[1]))
					visited[cur[0]-1][cur[1]] = True
					cells[cur[0]-1][cur[1]].fields[tgroup-4] = min(cells[cur[0]-1][cur[1]].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1)
				#print 't', cur

			if cur[0] < len(cells)-1:
				newNeighbor = (cur[0]+1, cur[1])
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]+1][cur[1]] and cells[cur[0]+1][cur[1]].cell_type > 0:
					queue.append((cur[0]+1,cur[1]))
					visited[cur[0]+1][cur[1]] = True
					cells[cur[0]+1][cur[1]].fields[tgroup-4] = min(cells[cur[0]+1][cur[1]].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1)
				#print 'b', cur

			if cur[1] > 0:
				newNeighbor = (cur[0], cur[1]-1)
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]][cur[1]-1] and cells[cur[0]][cur[1]-1].cell_type > 0:
					queue.append((cur[0],cur[1]-1))
					visited[cur[0]][cur[1]-1] = True
					cells[cur[0]][cur[1]-1].fields[tgroup-4] = min(cells[cur[0]][cur[1]-1].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1)
				#print 'l', cur

			if cur[1] < len(cells[0])-1:
				newNeighbor = (cur[0], cur[1]+1)
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]][cur[1]+1] and cells[cur[0]][cur[1]+1].cell_type > 0:
					queue.append((cur[0],cur[1]+1))
					visited[cur[0]][cur[1]+1] = True
					cells[cur[0]][cur[1]+1].fields[tgroup-4] = min(cells[cur[0]][cur[1]+1].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1)
				#print 'r', cur

			if cur[0] > 0 and cur[1] > 0:
				newNeighbor = (cur[0]-1, cur[1]-1)
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]-1][cur[1]-1] and cells[cur[0]-1][cur[1]-1].cell_type > 0:
					queue.append((cur[0]-1,cur[1]-1))
					visited[cur[0]-1][cur[1]-1] = True
					cells[cur[0]-1][cur[1]-1].fields[tgroup-4] = min(cells[cur[0]-1][cur[1]-1].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1.5)
				#print 'tl', cur

			if cur[0] > 0 and cur[1] < len(cells[0])-1:
				newNeighbor = (cur[0]-1, cur[1]+1)
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]-1][cur[1]+1] and cells[cur[0]-1][cur[1]+1].cell_type > 0:
					queue.append((cur[0]-1,cur[1]+1))
					visited[cur[0]-1][cur[1]+1] = True
					cells[cur[0]-1][cur[1]+1].fields[tgroup-4] = min(cells[cur[0]-1][cur[1]+1].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1.5)
				#print 'tr', cur

			if cur[0] < len(cells)-1 and cur[1] > 0:
				newNeighbor = (cur[0]+1, cur[1]-1)
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]+1][cur[1]-1] and cells[cur[0]+1][cur[1]-1].cell_type > 0:
					queue.append((cur[0]+1,cur[1]-1))
					visited[cur[0]+1][cur[1]-1] = True
					cells[cur[0]+1][cur[1]-1].fields[tgroup-4] = min(cells[cur[0]+1][cur[1]-1].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1.5)
				#print 'bl', cur

			if cur[0] < len(cells)-1 and cur[1] < len(cells[0])-1:
				newNeighbor = (cur[0]+1, cur[1]+1)
				if newNeighbor not in cells[cur[0]][cur[1]].neighbors and cells[newNeighbor[0]][newNeighbor[1]].cell_type > 0:
					cells[cur[0]][cur[1]].neighbors.append(newNeighbor)
				if not visited[cur[0]+1][cur[1]+1] and cells[cur[0]+1][cur[1]+1].cell_type > 0:
					queue.append((cur[0]+1,cur[1]+1))
					visited[cur[0]+1][cur[1]+1] = True
					cells[cur[0]+1][cur[1]+1].fields[tgroup-4] = min(cells[cur[0]+1][cur[1]+1].fields[tgroup-4], cells[cur[0]][cur[1]].fields[tgroup-4]+1.5)
				#print 'br', cur