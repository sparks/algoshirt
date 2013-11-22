#!/usr/bin/env python
from base import BaseRenderer
import cairo, os, math, uuid, argparse, colorsys, json

parser = argparse.ArgumentParser()
parser.add_argument("-rd", "--renders_dir", type=str, default="../../renders", help="directory to put renders in")
parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
parser.add_argument("params", type=str, default="./fractal-dots-v1-params.json", help="configuration parameters for the algorithm")

class FractalDots(BaseRenderer):

	def __init__(self, params):
		super(FractalDots, self).__init__(params)

	def render_to_surface(self, surface, w, h):
		cr = cairo.Context(surface)
		cr.translate(w/2, h/2)
		self.circle(
			cr,
			cr.get_matrix(),
			self.params["number"],
			self.params["angle"],
			self.params["scale"],
			self.params["distance"],
			self.params["fill_hue"],
			self.params["fill_hue_incr"],
			self.params["stroke_hue"],
			self.params["stroke_hue_incr"],
			0,
			self.params["depth"]
		)

	def circle(self, cr, matrix, number, angle, scale, distance, fill_hue, fill_hue_incr, stroke_hue, stroke_hue_incr, depth, max_depth):
		if depth >= max_depth:
			return

		cr.set_matrix(matrix)

		cr.arc(0, 0, 100, 0, 2*math.pi)

		stroke_color = colorsys.hsv_to_rgb(stroke_hue, 0.5, 0.2)

		cr.set_source_rgb(stroke_color[0], stroke_color[1], stroke_color[2])
		cr.set_line_width(40)
		cr.stroke_preserve()

		fill_color = colorsys.hsv_to_rgb(fill_hue, 1, 1)

		cr.set_source_rgb(fill_color[0], fill_color[1], fill_color[2])
		cr.fill()

		for i in range(number):
			cr.set_matrix(matrix)
			cr.rotate(angle*i)
			cr.translate(distance*100, 0)
			cr.scale(scale, scale)
			sub_matrix = cr.get_matrix()
			self.circle(cr, sub_matrix, number, angle, scale, distance, fill_hue+fill_hue_incr, fill_hue_incr, stroke_hue+stroke_hue_incr, stroke_hue_incr, depth+1, max_depth)

if __name__ == "__main__":
	args = parser.parse_args()
	renders_dir = args.renders_dir

	if not os.path.exists(renders_dir):
		os.makedirs(renders_dir)

	params_file = open(args.params)
	jsonParams = json.load(params_file)
	params_file.close()

	filename = "fractal-dots-v1-"+args.uuid

	png_path = os.path.join(renders_dir, filename+".png")
	svg_path = os.path.join(renders_dir, filename+".svg")

	params = {}

	params["width"]  = jsonParams["width"]["value"]
	params["height"] = jsonParams["height"]["value"]

	ps = cairo.SVGSurface(svg_path, params["width"], params["height"])
	cr = cairo.Context(ps)

	params["fill_hue"]        = jsonParams["fill_hue"]["value"]
	params["fill_hue_incr"]   = jsonParams["fill_hue_incr"]["value"]
	params["stroke_hue"]      = jsonParams["stroke_hue"]["value"]
	params["stroke_hue_incr"] = jsonParams["stroke_hue_incr"]["value"]
	params["number"]          = jsonParams["number"]["value"]
	params["angle"]           = jsonParams["angle"]["value"]
	params["scale"]           = jsonParams["scale"]["value"]
	params["distance"]        = jsonParams["distance"]["value"]
	params["depth"]           = jsonParams["depth"]["value"]

	dots = FractalDots(params)
	dots.render_to_surface(ps, params["width"], params["height"])

	ps.write_to_png(png_path)
	ps.finish()

	print(svg_path)
	print(png_path)