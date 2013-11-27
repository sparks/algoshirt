from algoshirt.backends.shirtsio import ShirtsIOBatch
from algoshirt.model import AlgoshirtModel
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("imgfile", type=str, help="the image file for the order")
parser.add_argument("db", type=str, help="the database of subscribers")
parser.add_argument("apikey", type=str, help="the shirts.io API key")

if __name__ == "__main__":
	args = parser.parse_args()

	model = AlgoshirtModel("sqlite:///"+args.db)
	batch = ShirtsIOBatch(args.imgfile, model.subscribers(), args.apikey)

	quote = batch.quote()

	print("Shirts.IO quote: "+str(quote["total"]))
	test = raw_input("Confirm order ...")

	batch.order(quote)
