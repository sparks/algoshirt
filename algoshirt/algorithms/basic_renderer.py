from base import BaseRenderer 
from algoshirt.algorithms.modules import Tiles
import cairo, math, random

class Basic(BaseRenderer):
	
	def __init__(self):
		super(Basic, self).__init__(params)
		
	def render_to_surface(self, surface, w, h):
		t = Tiles(params)
		tiled_sur = t.tiling()
		
		sf = ScaleAndFit()
		sf.render(tiled_sur, surface)m
		
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
