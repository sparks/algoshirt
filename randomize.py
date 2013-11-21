#!/usr/bin/env python
import argparse, os, json, uuid
import algoshirt.optimizers as optimizers
import algoshirt.algorithms as algorithms

parser = argparse.ArgumentParser()
parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
parser.add_argument("-rd", "--renders_dir", type=str, default="./renders", help="directory to put renders in")
args = parser.parse_args()

base_filename = "random-optimizer-{0}".format(args.uuid)
png_filename = os.path.join(args.renders_dir, "{0}.png".format(base_filename))
json_filename = os.path.join(args.renders_dir, "{0}.json".format(base_filename))

random_render_instance = optimizers.randomize(algorithms.FractalDots)

random_render_instance.render_to_png(
	png_filename,
	2000,
	2000
)

params_file = open(json_filename, "w")
json.dump(random_render_instance.params, params_file)
params_file.close()

print(png_filename)
print(json_filename)
