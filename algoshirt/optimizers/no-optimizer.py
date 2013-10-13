#!/usr/bin/env python
import subprocess, argparse, uuid

parser = argparse.ArgumentParser()
parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
parser.add_argument("-rd", "--renders_dir", type=str, default="../../renders", help="directory to put renders in")
parser.add_argument("command", type=str, help="the algorithm to generate with")
parser.add_argument("params", type=str, help="the self-describing json parameters for the algorithm")

if __name__ == "__main__":
	args = parser.parse_args()

	result = subprocess.check_output([args.command, "-u", args.uuid, "-rd", args.renders_dir, args.params])
	files = result.split("\n")
	for file in files:
		if len(file) > 0:
			print file