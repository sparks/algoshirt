import cairo, math, random
from algoshirt.util import webscrapper

# parameters: pixel size, Image
# __all__ = [ 'mise_en_abyme']


def mise_en_abyme(image):
	layers = random.randint(2, 40)
	# centerX= image.get_width()/2
	centerX = random.randint(0, image.get_width())
	centerY = random.randint(0, image.get_height())
	ratio = random.uniform(0.7,0.99)
	for i in range(layers):
		here = cr.get_matrix()
		new_width = canvas.get_width()*pow(ratio,i)
		new_height = canvas.get_height()*pow(ratio,i)
		cr.translate(centerX,centerY)
		cr.scale(ratio,ratio)
		cr.translate(-(new_width/2),-(new_height/2))
		cr.set_source_surface(image,0,0)
		cr.rectangle(0,0,new_width,new_height)
		cr.fill()
		cr.translate(image.get_width()/2,image.get_height()/2)
		cr.scale(1/ratio,1/ratio)
		cr.set_matrix(here)
	
outputs = 20
for k in range(outputs):
	canvas = webscrapper.rss_to_image_surface()[0]
	ps=canvas
	cr = cairo.Context(ps)
	mise_en_abyme(canvas)
	
	ps.write_to_png("./mything"+str(k)+".png")
	ps.finish()