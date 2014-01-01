import random, copy

def randomize(renderer):
	rand_params = copy.deepcopy(renderer.default_params)

	for key in rand_params:
		if rand_params[key]["automate"] != True:
			continue

		type = rand_params[key]["type"]
		
		if type != "float" and type != "int":
			continue

		min_val = rand_params[key]["min"]
		max_val = rand_params[key]["max"]

		rand_params[key]["value"] = (max_val-min_val)*random.random()+min_val

		if type == "int":
			rand_params[key]["value"] = int(rand_params[key]["value"])

	return renderer(rand_params)