from base import BaseRenderer
from algoshirt.util import webscrapper
import cairo, math, random

class BigPixels(BaseRenderer):
	
	default_params = {
		"pixel_size":
			{
				"value": 5,
				"type": "int",
				"min": 2,
				"max": 10,
				"automate": True
			}
	}
	
	def __init__(self,params = default_params):
		super(BigPixels, self).__init__(params)
		
	def render_to_surface(self, surface, w, h):
		cr = cairo.Context(surface)
		self.pixellize(cr, webscrapper.rss_to_image_surface()[0],self.params["pixel_size"]["value"])
		
	def pixellize(self, cr, image, pixel_size):
		p_size = image.get_width()/(self.params["pixel_size"]["max"]+self.params["pixel_size"]["min"]-pixel_size)
		cols = int(math.floor(float(image.get_width())/p_size))
		rows = int(math.floor(float(image.get_height())/p_size))

		destWidth = cols * p_size
		destHeight = rows * p_size

		pixcount = 0

		for i in range(cols):
			for j in range(rows):
				here = cr.get_matrix()
				grid = p_size
				pixX = random.randint(i*p_size, pixel_size+(i*p_size))
				pixY = random.randint(j*p_size, p_size+(j*p_size))
				for l in range(grid):
					for m in range(grid):
						cr.translate(-(pixX-(i*p_size))+l,-(pixY-(j*p_size))+m)
						cr.set_source_surface(image,0,0)
						cr.rectangle(pixX,pixY,1,1)
						cr.fill()
						pixcount += 1
						cr.set_matrix(here)
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-rd", "--renders_dir", type=str, default="../../renders", help="directory to put renders in")
	parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
	args = parser.parse_args()

	if not os.path.exists(args.renders_dir):
		os.makedirs(args.renders_dir)

	png_path = os.path.join(args.renders_dir, "big-pixels-v1-{0}.png".format(args.uuid))

	pixels = BigPixels()
	pixels.render_to_png(
		png_path,
		2000,
		2000
	)
