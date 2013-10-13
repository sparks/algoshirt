import sys, argparse
import algoshirt.web

parser = argparse.ArgumentParser()
parser.add_argument("config", type=str, help="the server configuration file")

if __name__ == "__main__":
	args = parser.parse_args()
	algoshirt.web.serve(args.config)
