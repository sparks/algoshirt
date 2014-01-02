from algoshirt.backends.shirtsio import ShirtsIOBatch
from algoshirt.model import AlgoshirtModel, Subscriber
import sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument("imgfile", type=str, help="the image file for the order")
parser.add_argument("db", type=str, help="the database of subscribers")
parser.add_argument("apikey", type=str, help="the shirts.io API key")

if __name__ == "__main__":
	args = parser.parse_args()

	model = AlgoshirtModel("sqlite:///"+args.db)

	session = model.get_session()

	batch = ShirtsIOBatch(
		args.apikey,
		session.query(Subscriber).all(), 
		"./renders/test.png", 
		"./renders/test.jpg", 
		"As large as possible", 
		"Centered",
		"black", 
		11, 
		1
	)

	quote = batch.quote()
	print(quote)
	print("Shirts.IO quote: "+str(quote["total"]))
	test = raw_input("Confirm order ...")

	print(batch.order(quote))

	session.close()
