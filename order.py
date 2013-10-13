from backends.shirtsio import ShirtsIOBatch
from model import AlgoshirtModel
import sys

if __name__ == "__main__":
    imgfile = sys.argv[1]
    db = sys.argv[2]
    apikey = sys.argv[3]

    model = AlgoshirtModel(db)
    batch = ShirtsIOBatch(imgfile, model.subscribers(), apikey)

    quote = batch.quote()
    print(quote["total"])
    batch.order(quote)
    # batch.order({"total":10.00})
