# shuffle elements of the list, allow small number of duplicates, 
# variables for the percentage of probabilaty that the same gets repeated
# mostly stay on the same column or row, occasional change 
# avoir une fonction qui dermine un poids dependant de la position dans le grid
#add offset
#vary col and row size

# PROBLEMS
# verify aiguillage for the foreign tiles

from algoshirt.util import webscrapper
import cairo, math, colorsys, random

def imageDrawRect(ctx, source, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY):
	here = ctx.get_matrix()
	ctx.translate(destX-sourceX, destY-sourceY)
	ctx.rectangle(sourceX,sourceY,sourceWidth,sourceHeight)
	ctx.set_source_surface(source, 0, 0)
	ctx.fill()
	ctx.set_matrix(here)

def imageDrawCircle(ctx, source, sourceX, sourceY, rad, destX, destY):
	here = ctx.get_matrix()
	ctx.translate(destX-sourceX, destY-sourceY)
	ctx.arc(sourceX+rad, sourceY+rad, rad, 0, 2*math.pi)
	ctx.set_source_surface(source, 0, 0)
	ctx.fill()
	ctx.set_matrix(here)
	
def colorDrawRect(ctx, sourceX, sourceY, sourceWidth, sourceHeight, destX, destY):
	r = 1
	g = 0
	b = 0
	here = ctx.get_matrix()
	ctx.translate(destX-sourceX, destY-sourceY)
	ctx.rectangle(sourceX,sourceY,sourceWidth,sourceHeight)
	ctx.set_source_rgb(r, g, b)
	ctx.fill()
	ctx.set_matrix(here)

def colorDrawCircle(ctx, rad, destX, destY):
	here = ctx.get_matrix()
	ctx.translate(destX, destY)
	ctx.arc(rad, rad, rad, 0, 2*math.pi)
	ctx.set_source_rgb(random.random(), random.random(), random.random())
	ctx.fill()
	ctx.set_matrix(here)

class Shuffler(object):
	def __init__(self, rand_par_dist, rand_par_num):
		self.rand_par_dist = rand_par_dist
		self.rand_par_num = rand_par_num
		
	def shuffleFn(self, grid, originTuple):
		randPar = self.rand_par_dist
		if random.random() <= self.rand_par_num:
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
				"automate": True
			},
		"rows":
			{
				"value": 2,
				"type": "int",
				"min": 1,
				"max": 30,
				"automate": True
			},
		"shape":
			{
				"value": 0, # of list ['rect','circle']
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"rand_par_dist":
			{
				"value": 0.5,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"rand_par_num":
			{
				"value": 0.5,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"holes":
			{
				"value": 0,
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"holes_fct":
			{
				"value": 0,
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": True
			},	
		"color":
			{
				"value": 0,
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"color_fct":
			{
				"value": 1,
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": False
			},
		"image":
			{
				"value": 0,
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"image_fct":
			{
				"value": 0,
				"type": "int",
				"min": 0,
				"max": 1,
				"automate": True
			},
		"foreign_random":
			{
				"value": 0,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": True
			}
		}

	shapes = ('rect', 'circle')
	
	def __init__(self, params = default_params):
		self.params = params
		self.bands_list = []
	
	def create_bands_list(self):
		bands = []
		for i in range(self.params["cols"]["value"]):
			bands.append(random.randint(1,self.params["rows"]["value"]))
		return bands
			
	def get_color(self):
		color = [0,0,0]
		return color
	
	def bands(self, x, y, type):
		if y > self.bands_list[x-1]:
			return True
		else: return False
	
	def random_position(self,x,y,type):
		a = self.params["foreign_random"]["value"]
		r = random.uniform(0.1,1)
		if r > a:
			return True
		else: return False
					
	def switch(self,x,y):
		if self.params["holes_fct"]["value"] == 0:
			if self.bands(x,y,"holes"):
				return True
		if self.params["holes_fct"]["value"] == 1:
			if self.random_position(x,y,"holes"):
				return True
		if self.params["color_fct"]["value"] == 0:
			if self.bands(x,y,"color"):
				return True
		if self.params["color_fct"]["value"] == 1:
			if self.random_position(x,y,"color"):
				return True
		if self.params["image_fct"]["value"] == 0:
			if self.bands(x,y,"image"):
				return True
		if self.params["image_fct"]["value"] == 1:
			if self.random_position(x,y,"image"):
				return True

	def tiling(self):
		images = webscrapper.rss_to_image_surface()
		image = images[random.randint(0,len(images)-1)]
		image2 = images[random.randint(0,len(images)-1)]

		width = image.get_width()
		height = image.get_height()
		border = 0
		cols = self.params["cols"]["value"]
		rows = self.params["rows"]["value"]
		maxCols = self.params["cols"]["max"]
		maxRows = self.params["rows"]["max"]
		destWidth = width
		destHeight = height
		shape = Tiles.shapes[self.params["shape"]["value"]]
		print shape
		
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
	
		ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, destWidth, destHeight)
		cr = cairo.Context(ps)
	
		grid = []
		#fill grid
		for k in range(cols):
			currentCol = []
			for l in range(rows):
				currentCol.append([k,l])
			grid.append(currentCol)

		shuffler = Shuffler(random.random(), random.random())	
		shuffleGrid(grid, shuffler)

		# print "grid", grid
		
		if self.params["holes_fct"]["value"] == 1 or self.params["color_fct"]["value"] == 1 or self.params["image_fct"]["value"] == 1:
			self.bands_list = self.create_bands_list()
	
		if (shape =='rect'):
			for i in range(cols):
				for j in range (rows):
					if self.params["holes"]["value"] == 1:
						if self.switch(i,j):
							continue
					elif self.params["color"]["value"] == 1:
						if self.switch(i,j):
							colorDrawRect(cr, grid[i][j][0]*width, grid[i][j][1]*height, width, height, 
							i*(image.get_width()/cols)+(i+1)*border, j*(image.get_height()/rows)+(j+1)*border)	
					elif self.params["image"]["value"] == 1:
						if self.switch(i,j):
							imageDrawRect(cr,image, grid[i][j][0]*width, grid[i][j][1]*height, width, height, 
							i*(image.get_width()/cols)+(i+1)*border, j*(image.get_height()/rows)+(j+1)*border)
					else:
						imageDrawRect(cr,image, grid[i][j][0]*width, grid[i][j][1]*height, width, height, 
						i*(image.get_width()/cols)+(i+1)*border, j*(image.get_height()/rows)+(j+1)*border)
	
		if (shape == 'circle'):
			for i in range(cols):
				for j in range (rows):
					# if j*6 < i:
					# if j < i:
					x = random.random()
					if x > 0.3:
						imageDrawCircle(cr,image, grid[i][j][0]*shapeWidth, grid[i][j][1]*shapeWidth, shapeWidth/2, 
						i*shapeWidth+(i+1)*border, j*shapeWidth+(j+1)*border)	
					else:
						colorDrawCircle(cr, shapeWidth/2, i*shapeWidth+(i+1)*border, j*shapeWidth+(j+1)*border)

		return ps