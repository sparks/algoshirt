import cairo, os, math, uuid, argparse, colorsys, random, json

def circle(matrix, number, angle, scale, distance, fill_hue, fill_hue_incr, stroke_hue, stroke_hue_incr, depth, max_depth):
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
		circle(sub_matrix, number, angle, scale, distance, fill_hue+fill_hue_incr, fill_hue_incr, stroke_hue+stroke_hue_incr, stroke_hue_incr, depth+1, max_depth)

parser = argparse.ArgumentParser()
parser.add_argument("-rd", "--renders_dir", type=str, default="../renders", help="directory to put renders in")
parser.add_argument("params", type=str, default="./params.json", help="configuration parameters for the algorithm")

if __name__ == "__main__":
	args = parser.parse_args()
	renders_dir = args.renders_dir

	if not os.path.exists(renders_dir):
		os.makedirs(renders_dir)

	json_params = open(args.params)
	params = json.load(json_params)
	json_params.close()

	filename = "fractal1-"+str(uuid.uuid4())
	png_path = os.path.join(renders_dir, filename+".png")
	svg_path = os.path.join(renders_dir, filename+".svg")

	width  = params["width"]
	height = params["height"]

	ps = cairo.SVGSurface(svg_path, width, height)
	cr = cairo.Context(ps)

	fill_hue        = params["fill_hue"]
	fill_hue_incr   = params["fill_hue_incr"]
	stroke_hue      = params["stroke_hue"]
	stroke_hue_incr = params["stroke_hue_incr"]
	number          = params["number"]
	angle           = params["angle"]
	scale           = params["scale"]
	distance        = params["distance"]
	depth           = params["depth"]

	cr.translate(width/2, height/2)
	circle(cr.get_matrix(), number, angle, scale, distance, fill_hue, fill_hue_incr, stroke_hue, stroke_hue_incr, 0, depth)

	ps.write_to_png(png_path)
	ps.finish()

	print svg_path
	print png_path