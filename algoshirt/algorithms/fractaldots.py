#!/usr/bin/env python
from base import BaseRenderer
import cairo, os, math, uuid, argparse, colorsys

class FractalDots(BaseRenderer):

	default_params = {
		"fill_hue":
			{
				"value": 0,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"fill_hue_incr":
			{
				"value": 0.713,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"stroke_hue":
			{
				"value": 0,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"stroke_hue_incr":
			{
				"value": 0.11,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"number":
			{
				"value": 20,
				"type": "int",
				"min": 2,
				"max": 30,
				"automate": "true"
			},
		"angle":
			{
				"value": 0.31,
				"type": "float",
				"min": 0,
				"max": 3.141592,
				"automate": "true"
			},
		"scale":
			{
				"value": 0.4,
				"type": "float",
				"min": 0,
				"max": 1,
				"automate": "true"
			},
		"distance":
			{
				"value": 6,
				"type": "float",
				"min": 1,
				"max": 6,
				"automate": "true"
			},
		"depth":
			{
				"value": 4,
				"type": "int",
				"min": 1,
				"max": 6,
				"automate": "true"
			}
	}

	def __init__(self, params = default_params):
		super(FractalDots, self).__init__(params)

	def render_to_surface(self, surface, w, h):
		cr = cairo.Context(surface)

		cr.translate(w/2, h/2)
		self.circle(
			cr,
			cr.get_matrix(),
			self.params["number"]["value"],
			self.params["angle"]["value"],
			self.params["scale"]["value"],
			self.params["distance"]["value"],
			self.params["fill_hue"]["value"],
			self.params["fill_hue_incr"]["value"],
			self.params["stroke_hue"]["value"],
			self.params["stroke_hue_incr"]["value"],
			0,
			self.params["depth"]["value"]
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
	parser = argparse.ArgumentParser()
	parser.add_argument("-rd", "--renders_dir", type=str, default="../../renders", help="directory to put renders in")
	parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
	args = parser.parse_args()

	if not os.path.exists(args.renders_dir):
		os.makedirs(args.renders_dir)

	png_path = os.path.join(args.renders_dir, "fractal-dots-v1-{0}.png".format(args.uuid))

	dots = FractalDots()
	dots.render_to_png(
		png_path,
		2000,
		2000
	)

	print(png_path)
	