from PIL import Image


class ImportImage:

	def __init__(self, width = 1650, height = 400):
		self.width = width
		self.height = height
		self.matrix = [[-1 for x in range(self.height)] for x in range(self.width)]

	def setSea(self):
		im = Image.open("image/map0.bmp").getdata()
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				if im[i] == (0, 0, 0):
					self.matrix[x][y] = 0
				i += 1
	
	def setBeach(self):
		im = Image.open("image/map1.bmp").getdata()
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				if im[i] == (0, 0, 0):
					self.matrix[x][y] = 1
				i += 1

	def setLand(self):
		im = Image.open("image/map2.bmp").getdata()
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				if im[i] == (0, 0, 0):
					self.matrix[x][y] = 2
				i += 1

	def setSlope(self):
		im = Image.open("image/map3.bmp").getdata()
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				if im[i] == (0, 0, 0):
					self.matrix[x][y] = 3
				i += 1

	def setBunker(self, nBunker = 13):
		for t in range(4, 4 + nBunker):
			im = Image.open("image/map" + str(t) + ".bmp").getdata()
			i = 0
			for y in range(self.height):
				for x in range(self.width):
					if im[i] == (0, 0, 0):
						self.matrix[x][y] = t
					i += 1

	def writeFile(self):
		text_file = open("image/map.txt", "w")
		for y in range(self.height):
			for x in range(self.width):
				text_file.write(str(self.matrix[x][y]) + " ")
			text_file.write("\n")



ii = ImportImage()
ii.setSea()
ii.setBeach()
ii.setLand()
ii.setSlope()
ii.setBunker()
ii.writeFile()
