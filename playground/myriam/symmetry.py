import cairo, math, random, numpy
from algoshirt.util import webscrapper

# parameters: pixel size, Image

def reflection_matrix(point, normal):
    """Return matrix to mirror at plane defined by point and normal vector.

    >>> v0 = numpy.random.random(4) - 0.5
    >>> v0[3] = 1.
    >>> v1 = numpy.random.random(3) - 0.5
    >>> R = reflection_matrix(v0, v1)
    >>> numpy.allclose(2, numpy.trace(R))
    True
    >>> numpy.allclose(v0, numpy.dot(R, v0))
    True
    >>> v2 = v0.copy()
    >>> v2[:3] += v1
    >>> v3 = v0.copy()
    >>> v2[:3] -= v1
    >>> numpy.allclose(v2, numpy.dot(R, v3))
    True

    """
    normal = unit_vector(normal[:3])
    M = numpy.identity(4)
    M[:3, :3] -= 2.0 * numpy.outer(normal, normal)
    M[:3, 3] = (2.0 * numpy.dot(point[:3], normal)) * normal
    return M

outputs = 1
for k in range(outputs):
	numImage=1
	image = webscrapper.rss_to_image_surface(numImage)[numImage-1]
	
	dest_width = image.get_width()
	dest_height = image.get_height()
	
	ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, dest_width, dest_height)
	cr = cairo.Context(ps)
	
	sides = [1,2,3,4]
	axis = random.sample(sides,2)
	axis.sort()
	axis = [1,2]
	print axis
	print 'width, height', image.get_width(), image.get_height()
	
	if axis == [1,2]:
		side1 = (0, random.randint(0,image.get_height()))
		side2 = (random.randint(0,image.get_width()),0)
		axis = [side1,side2]
		print axis
		
		
		
		#NO ROTATION!!!!
		# cr.set_source_surface(image,0,0)
		# cr.paint()
		# 
		# cr.translate(image.get_width()/2,image.get_height()/2)
		# cr.scale(-1,1)
		# cr.translate(-image.get_width()/2,-image.get_height()/2)
		# 	
		# cr.set_source_surface(image,0,0)
		# 
		# cr.translate(image.get_width()/2,image.get_height()/2)
		# cr.scale(-1,1)
		# cr.translate(-image.get_width()/2,-image.get_height()/2)
		# 
		# cr.move_to(side1[0],side1[1])
		# cr.line_to(0,image.get_height())
		# cr.line_to(image.get_width(),image.get_height())
		# cr.line_to(image.get_width(),0)
		# cr.line_to(side2[0],side2[1])
		# cr.line_to(side1[0],side1[1])
		# cr.fill()
		
	elif axis == [1,3]:
		side1 = (0, random.randint(0,image.get_height()))
		side3 = (image.get_width(), random.randint(0,image.get_height()))
		axis = [side1,side3]
		print axis
		
	elif axis == [1,4]:
		side1 = (0, random.randint(0,image.get_height()))
		side4 = (random.randint(0,image.get_width()),image.get_height())
		axis = [side1,side4]
		print axis
		
	elif axis == [2,3]:
		side2 = (random.randint(0,image.get_width()),0)
		side3 = (image.get_width(), random.randint(0,image.get_height()))
		axis = [side2,side3]
		print axis
		
	elif axis == [2,4]:
		side2 = (random.randint(0,image.get_width()),0)
		side4 = (random.randint(0,image.get_width()),image.get_height())
		axis = [side2,side4]
		print axis
		
	elif axis == [3,4]:
		side3 = (image.get_width(), random.randint(0,image.get_height()))
		side4 = (random.randint(0,image.get_width()),image.get_height())
		axis = [side3,side4]
		print axis
		
	# cr.save()
	# # cr.rectangle(0,0,image.get_width(),image.get_height())
	# # cr.fill()
	# cr.translate(image.get_width()/2,image.get_height()/2)
	# cr.scale(-1, -1)
	# 
	# cr.set_source_surface(image,0,0)
	# cr.translate(image.get_width()/2,image.get_height()/2)
	# # cr.translate(-image.get_width()/2,-image.get_height()/2)	
	# # cr.translate(image.get_width()/2,image.get_height()/2)
	# # cr.translate(-image.get_width(),0)
	# cr.paint()
	# # cr.fill()
	# # cr.restore()

	ps.write_to_png("./mything"+str(k)+".png")
	ps.finish()