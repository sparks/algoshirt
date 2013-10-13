#!/usr/bin/env python
import cairo, math, argparse, os, uuid

parser = argparse.ArgumentParser()
parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
parser.add_argument("-rd", "--renders_dir", type=str, default="../../renders", help="directory to put renders in")
parser.add_argument("proof", type=str, help="the algorithm to generate with")
parser.add_argument("design", type=str, help="the self-describing json parameters for the algorithm")

if __name__ == "__main__":
	args = parser.parse_args()

	img_shirt = cairo.ImageSurface.create_from_png(args.proof)
	img_design = cairo.ImageSurface.create_from_png(args.design)

	cr_shirt = cairo.Context(img_shirt)

	# 215x300

	ar_shirt = 215.0/300.0
	ar_design = img_design.get_width()/img_design.get_height()

	# cr_shirt.translate(90, 60)
	corrected_ratio = 1

	if ar_shirt < ar_design:
		corrected_ratio = 215.0/img_design.get_width()
		cr_shirt.translate(182, 150+(300-img_design.get_height()*corrected_ratio)/2)
	else:
		corrected_ratio = 300.0/img_design.get_height()
		cr_shirt.translate(182+(215-img_design.get_width()*corrected_ratio)/2, 150)

	cr_shirt.scale(corrected_ratio, corrected_ratio)

	cr_shirt.set_source_surface(img_design, 0, 0)
	cr_shirt.paint()

	img_shirt.write_to_png(os.path.join(args.renders_dir, "proof-"+args.uuid+".png"))