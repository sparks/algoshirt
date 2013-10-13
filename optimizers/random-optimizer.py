#!/usr/bin/env python
import subprocess, argparse, random, json, os, uuid

parser = argparse.ArgumentParser()
parser.add_argument("-uuid", type=str, default=str(uuid.uuid4()), help="(optional) uuid for this run")
parser.add_argument("-rd", "--renders_dir", type=str, default="../renders", help="directory to put renders in")
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
			continue

		min_val = params[key]["min"]
		max_val = params[key]["max"]

		params[key]["value"] = (max_val-min_val)*random.random()+min_val

		if type == "int":
			params[key]["value"] = int(params[key]["value"])

	filename = "random-optimizer-params-"+args.uuid+".json"

	param_filename = os.path.join(args.renders_dir, filename)
	params_file = open(param_filename, "w")
	json.dump(params, params_file)
	params_file.close()

	result = subprocess.check_output([args.command, "-u", args.uuid, "-rd", args.renders_dir, param_filename])
	files = result.split("\n")
	for file in files:
		if len(file) > 0:
			print file
	print param_filename