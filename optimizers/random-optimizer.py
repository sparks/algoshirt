#!/usr/bin/env python
import subprocess, argparse, random, json

parser = argparse.ArgumentParser()
parser.add_argument("command", type=str, help="the algorithm to generate with")
parser.add_argument("params", type=str, help="the self-describing json parameters for the algorithm")

if __name__ == "__main__":
	args = parser.parse_args()

	params_file = open(args.params)
	params = json.load(params_file)
	params_file.close()

	for key in params:
		if params[key]["automate"] != "true":
			continue

		type = params[key]["type"]
		
		if type != "float" and type != "int":
			print "bounce"
			continue

		min_val = params[key]["min"]
		max_val = params[key]["max"]

		params[key]["value"] = (max_val-min_val)*random.random()+min_val

		if type == "int":
			params[key]["value"] = int(params[key]["value"])

	params_file = open("tmp.json", "w")
	json.dump(params, params_file)
	params_file.close()

	result = subprocess.check_output([args.command, "./tmp.json"])
	files = result.split("\n")
	for file in files:
		if len(file) > 0:
			print file
