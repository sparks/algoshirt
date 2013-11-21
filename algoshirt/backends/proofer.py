#!/usr/bin/env python
import cairo, math, argparse, os, uuid

parser = argparse.ArgumentParser()
parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
parser.add_argument("-rd", "--renders_dir", type=str, default="../../renders", help="directory to put renders in")
parser.add_argument("proof", type=str, help="the algorithm to generate with")
parser.add_argument("design", type=str, help="the self-describing json parameters for the algorithm")

class ShirtProof():

	def __init__(self, png_filename, x, y, w, h):
		self.image = cairo.ImageSurface.create_from_png(png_filename)

		self.x = float(x)
		self.y = float(y)

		self.w = float(w)
		self.h = float(h)

	def proof_from_surface(self, surface):
		output = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.image.get_width(), self.image.get_height())

		cr = cairo.Context(output)
		cr.set_source_surface(self.image, 0, 0)
		cr.paint()

		ar_shirt = self.w/self.h
		ar_design = surface.get_width()/surface.get_height()

		corrected_ratio = 1

		if ar_shirt < ar_design:
			corrected_ratio = self.w/surface.get_width()
			cr.translate(self.x, self.y+(self.h-surface.get_height()*corrected_ratio)/2)
		else:
			corrected_ratio = self.h/surface.get_height()
			cr.translate(self.x+(self.w-surface.get_width()*corrected_ratio)/2, self.y)

		cr.scale(corrected_ratio, corrected_ratio)

		cr.set_source_surface(surface, 0, 0)
		cr.paint()

		return output

	def proof_from_png(self, png_filename):
		img_design = cairo.ImageSurface.create_from_png(png_filename)
		return self.proof_from_surface(img_design)

if __name__ == "__main__":
	args = parser.parse_args()

	blank = ShirtProof(args.proof, 182, 150, 215, 300)
	proof = blank.proof_from_png(args.design)

	proof.write_to_png(os.path.join(args.renders_dir, "proof-"+args.uuid+".png"))
