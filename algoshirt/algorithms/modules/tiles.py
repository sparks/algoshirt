# shuffle elements of the list, allow small number of duplicates, 
# variables for the percentage of probabilaty that the same gets repeated
# mostly stay on the same column or row, occasional change 
# avoir une fonction qui dermine un poids dependant de la position dans le grid
#add offset
#vary col and row size

from algoshirt.util import webscrapper
import cairo, math, colorsys, random

def imageDrawRect(source, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY):
	here = cr.get_matrix()
	cr.translate(destX-sourceX, destY-sourceY)
	cr.rectangle(sourceX,sourceY,sourceWidth,sourceHeight)
	cr.set_source_surface(source, 0, 0)
	cr.fill()
	cr.set_matrix(here)

def imageDrawCircle(source, sourceX, sourceY, rad, destX, destY):
	here = cr.get_matrix()
	cr.translate(destX-sourceX, destY-sourceY)
	cr.arc(sourceX+rad, sourceY+rad, rad, 0, 2*math.pi)
	cr.set_source_surface(source, 0, 0)
	cr.fill()
	cr.set_matrix(here)
	
def colorDrawRect(source, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY):
	here = cr.get_matrix()
	cr.translate(destX-sourceX, destY-sourceY)
	cr.rectangle(sourceX,sourceY,sourceWidth,sourceHeight)
	cr.set_source_rgb(0, 0, 0)
	cr.fill()
	cr.set_matrix(here)

def colorDrawCircle(rad, destX, destY):
	here = cr.get_matrix()
	cr.translate(destX, destY)
	cr.arc(rad, rad, rad, 0, 2*math.pi)
	cr.set_source_rgb(random.random(), random.random(), random.random())
	cr.fill()
	cr.set_matrix(here)

class Shuffler(object):
	def __init__(self, randParDist, randParNum):
		self.randParDist = randParDist
		self.randParNum = randParNum
		
	def shuffleFn(self, grid, originTuple):
		randPar = self.randParDist
		if random.random() <= self.randParNum:
			if ((len(grid) < 5 and len(grid[0]) < 5) or (len(grid) < 3 or len(grid[0]) < 3)):
				x = random.choice([0,1])
				if x == 0:
					self.shuffleSameCol(grid, originTuple, randPar)
				elif x == 1:
					self.shuffleSameRow(grid, originTuple, randPar)
			else:
				self.shuffleAnywhere(grid, originTuple, randPar)

		# moveSameCol = 0
		# moveSameRow = 0
		# moveAnywhere = 0
		# stay = 1
		# if randPar >= 0.1:
		# 	moveSameCol += randPar*10
		# if randPar >= 0.2:
		# 	moveSameRow += randPar*10
		# elif randPar >= 0.3:
		# 	moveSameCol = 0
		# 	moveSameRow = 0
		# 	moveAnywhere += randPar*10	
		# allProb = float(moveSameCol+moveSameRow+moveAnywhere+stay)
		# limit1 = moveSameCol/allProb
		# limit2 = (moveSameCol+moveSameRow)/allProb
		# limit3 = (moveSameCol+moveSameRow+moveAnywhere)/allProb
		# limit4 = 1.
		# thresh = 3  # how close the swap will be


	def swap(self, grid, origin, dest):
		swap = grid[origin[0]][origin[1]]
		grid[origin[0]][origin[1]] = grid[dest[0]][dest[1]]
		grid[dest[0]][dest[1]] = swap

	def randParToGrid(self, length, randPar):
		thresh = 0
		# conv = 10
		# limit = 0.5
		# 
		# if randPar <= limit:
		# 	thresh = math.floor(randPar*conv)
		# elif randPar > limit:
		# 	minRange = math.floor(limit*conv)
		# 	thresh = round(float(randPar-limit)/float(1-limit)*(length-minRange)+minRange)

		thresh = round(randPar*length)				
		thresh = int(thresh)
		if thresh >= length:
			thresh = length-1
		
		return thresh
	
	def shuffleSameCol(self, grid, originTuple, randPar):
		thresh = self.randParToGrid(len(grid[0]), randPar)
		
		if len(grid[0]) <= thresh: #define range
			thresh = len(grid[0])-1
		
		swapRow = random.randint(originTuple[1]-round(thresh/2),originTuple[1]+round(thresh/2))
		
		if (swapRow < 0):
			swapRow = 0
		elif swapRow > len(grid[0])-1:
			swapRow = len(grid[0])-1
			
		self.swap(grid, originTuple, [originTuple[0], swapRow])

	def shuffleSameRow(self, grid, originTuple, randPar):
		thresh = self.randParToGrid(len(grid), randPar)
		
		if len(grid) <= thresh:  #define range
			thresh = len(grid)-1
		
		swapCol = random.randint(originTuple[0]-round(thresh/2), originTuple[0]+round(thresh/2))
		
		if swapCol < 0: 
			swapCol = 0
		elif swapCol > len(grid)-1:
			swapCol = len(grid)-1
		
		self.swap(grid, originTuple, [swapCol, originTuple[1]])
	
	def shuffleAnywhere(self, grid, originTuple, randPar):
		x = random.uniform(0, randPar)
		y = randPar - x
		self.shuffleSameRow(grid, originTuple, x)
		self.shuffleSameCol(grid, originTuple, y)
	
def shuffleGrid(grid, shuffler):
	for i in range(len(grid)):	# shuffle grid	
		for j in range(len(grid[i])):
			shuffler.shuffleFn(grid,(i,j))
		
# def colorGrid():
	
# def colorGridItem():	

class Tiles(object):
	
	default_params = {
		"cols":
			{
				"value": 2,
				"type": "int",
				"min": 1,
				"max": 30,
				"automate": "true"
			},
		"rows":
			{
				"value": 2,
				"type": "int",
				"min": 1,
				"max": 30,
				"automate": "true"
			},
		"shape":
			{
				"value": 0, # of list ['rect','circle']
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"randParDist":
			{
				"value": 0.5,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"randParNum":
			{
				"value": 0.5,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			}
		
	}

	shapes = ("rect", "circle")
	
	def __init__(self, params = default_params):
		self.params = params

	def tiling(self):
		images = webscrapper.rss_to_image_surface()
		image = images[random.randint(0,len(images)-1)]

		width = image.get_width()
		height = image.get_height()
		border = 0
		cols = self.params["cols"]["value"]
		rows = self.params["rows"]["value"]
		maxCols = self.params["cols"]["max"]
		maxRows = self.params["rows"]["max"]
		destWidth = 1000
		destHeight = 1000
		shape = Tiles.shapes[self.params["shape"]["value"]]

		ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, destWidth, destHeight)
		cr = cairo.Context(ps)
	
		if(shape == 'rect'):
			width = image.get_width()/cols
			height = image.get_height()/rows
			border = random.randint(0,10)
			destWidth = image.get_width()+(cols+1)*border
			destHeight = image.get_height()+(rows+1)*border
	
		elif(shape == 'circle' or 'square'):
			shapeWidth = image.get_width()/random.randint(1,maxCols)
			print math.floor(image.get_width()/shapeWidth)
			cols = int(math.floor(image.get_width()/shapeWidth))
			rows = int(math.floor(image.get_height()/shapeWidth))
			border = random.randint(0,10)
			destWidth = shapeWidth*cols+(cols+1)*border
			destHeight = shapeWidth*rows+(rows+1)*border
	
	
		grid = []
		#fill grid
		for k in range(cols):
			currentCol = []
			for l in range(rows):
				currentCol.append([k,l])
	
		shuffler = Shuffler(random.random(), random.random())	
		shuffleGrid(grid, shuffler)

		print "grid", grid
	
		if (shape =='rect'):
			for i in range(cols):
				for j in range (rows):
					# if i < j/(random.randint(1,4)) or j < i/(random.randint(1,2)):
					# x = random.random()
					# 		if x > 0.5:
					imageDrawRect(image, grid[i][j][0]*width, grid[i][j][1]*height, width, height, 
					i*(image.get_width()/cols)+(i+1)*border, j*(image.get_height()/rows)+(j+1)*border)
	
		if (shape == 'circle'):
			for i in range(cols):
				for j in range (rows):
					# if j*6 < i:
					# if j < i:
					x = random.random()
					if x > 0.3:
						imageDrawCircle(image, grid[i][j][0]*shapeWidth, grid[i][j][1]*shapeWidth, shapeWidth/2, 
						i*shapeWidth+(i+1)*border, j*shapeWidth+(j+1)*border)	
					else:
						colorDrawCircle(shapeWidth/2, i*shapeWidth+(i+1)*border, j*shapeWidth+(j+1)*border)

		return ps