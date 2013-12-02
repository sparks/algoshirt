import cairo, math, os
from algoshirt.util import webscrapper

images = webscrapper.rss_to_image_surface(3)

for i in range(len(images)):
	ps = images[i]
	cr = cairo.Context(ps)
	
	if not os.path.exists("new_renders"):
		os.mkdir("new_renders")
	
	filepath = os.path.join("new_renders","mything"+ str(i)+".png")
	
	
	ps.write_to_png(filepath)
	ps.finish()