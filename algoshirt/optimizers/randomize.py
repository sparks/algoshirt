import random, copy

def randomize(renderer):
	rand_params = copy.deepcopy(renderer.default_params)

	for key in rand_params:
		if rand_params[key]["automate"] != True:
			continue

		type = rand_params[key]["type"]
		
		if type == "float":
			min_val = float(rand_params[key]["min"])
			max_val = float(rand_params[key]["max"])

			rand_params[key]["value"] = random.uniform(min_val, max_val)
		elif type == "int":
			min_val = int(rand_params[key]["min"])
			max_val = int(rand_params[key]["max"])

			rand_params[key]["value"] = random.randint(min_val, max_val)
		else:
			continue

	return renderer(rand_params)