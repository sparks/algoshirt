import cairo, math, random
from algoshirt.util import webscrapper

# parameters: pixel size, Image

outputs = 10
for k in range(outputs):
	numImage=1
	image = webscrapper.rss_to_image_surface(numImage)[numImage-1]
	pixelSize = random.randint(10,image.get_width()/5)
	
	cols = int(math.floor(float(image.get_width())/pixelSize))
	rows = int(math.floor(float(image.get_height())/pixelSize))
	
	destWidth = cols * pixelSize
	destHeight = rows * pixelSize
	
	print destWidth, destHeight, pixelSize
	print cols, rows
	
	ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, destWidth, destHeight)
	cr = cairo.Context(ps)
	
	pixcount = 0

	for i in range(cols):
		for j in range(rows):
			here = cr.get_matrix()
			grid = pixelSize
			pixX = random.randint(i*pixelSize, pixelSize+(i*pixelSize))
			pixY = random.randint(j*pixelSize, pixelSize+(j*pixelSize))
			for l in range(grid):
				for m in range(grid):
					cr.translate(-(pixX-(i*pixelSize))+l,-(pixY-(j*pixelSize))+m)
					cr.set_source_surface(image,0,0)
					cr.rectangle(pixX,pixY,1,1)
					cr.fill()
					pixcount += 1
					cr.set_matrix(here)
	
	print "grid", cols*rows, "totalpix", cols*rows*pixelSize*pixelSize, "pixcount",pixcount
	ps.write_to_png("./mything"+str(k)+".png")
	ps.finish()