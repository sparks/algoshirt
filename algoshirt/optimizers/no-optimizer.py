#!/usr/bin/env python
import subprocess, argparse

parser = argparse.ArgumentParser()
parser.add_argument("command", type=str, help="the algorithm to generate with")
parser.add_argument("params", type=str, help="the self-describing json parameters for the algorithm")

if __name__ == "__main__":
	args = parser.parse_args()

	result = subprocess.check_output([args.command, args.params])
	files = result.split("\n")
	for file in files:
		if len(file) > 0:
			print file