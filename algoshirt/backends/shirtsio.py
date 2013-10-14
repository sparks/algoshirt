''' Order a shirt from the shirts.io API
'''

import os
import json
import requests

API_V1 = "https://www.shirts.io/api/v1"
#API_V1 = "http://localhost:8080"
# API_V1 = "http://localhost:1234"

def shirtsio_encode_r(base, node, result):
    if isinstance(node, dict):
        for k,v in node.iteritems():
            newbase = "{}[{}]".format(base, k)
            shirtsio_encode_r(newbase, v, result)
    elif isinstance(node, list):
        for i,v in enumerate(node):
            newbase = "{}[{}]".format(base, i)
            shirtsio_encode_r(newbase, v, result)
    else:
        # We've reached a root node!
        result[base] = node


def shirtsio_encode(dictionary, prefix=None):
    ''' Encodes the given dictionary into a new flat dictionary in the
    shirtsio style, where arrays get keys that look like their description,
    that is:
        >>> d = {"foo": [{"bar": 17}, {"bar": 16}]}
        >>> encoded = shirtsio_encode(d)
        >>> for k,v in encoded.iteritems():
        ...    print "\"{}\": \"{}\"".format(k,v)
        "foo[0][bar]": 17
        "foo[1][bar]": 16

    '''
    result = {}
    for k,v in dictionary.iteritems():
        shirtsio_encode_r(k, v, result)
    return result

class ShirtsIOBatch(object):
    def __init__(self, imagefile, subscribers, apikey):
        self.imagefile = imagefile
        self.subscribers = subscribers
        self.apikey = apikey

    def quote(self):
        fields = {}
        fields["api_key"] = self.apikey
        fields["garment"] = []
        fields["addresses"] = []
        for i, subscriber in enumerate(self.subscribers):
            garment = {}
            garment["product_id"] = 3
            garment["color"] = "Red"
            garment["sizes"] = {subscriber.size:1}
            fields["garment"].append(garment)

            address = {}
            address["name"] = subscriber.name
            address["company"] = subscriber.company
            address["address"] = subscriber.address
            address["address2"] = subscriber.address2
            address["city"] = subscriber.city
            address["state"] = subscriber.state
            address["country"] = subscriber.country
            address["zip"] = subscriber.postcode
            fields["addresses"].append(address)

        fields["print"] = {"front": {"color_count": 1}}
        fields["address_count"] = len(self.subscribers)

        r = requests.get(API_V1 + "/quote", params=shirtsio_encode(fields))
        #print(r.url)
        #print(r.text)
        return json.loads(r.text).get("result")

    def order(self, quote, test=True):
        fields = {}
        fields["api_key"] = self.apikey
        fields["garment"] = []
        fields["addresses"] = []
        for i, subscriber in enumerate(self.subscribers):
            garment = {}
            garment["product_id"] = 3
            garment["color"] = "Red"
            garment["sizes"] = {subscriber.size:1}
            fields["garment"].append(garment)

            address = {}
            address["name"] = subscriber.name
            address["company"] = subscriber.company
            address["address"] = subscriber.address
            address["address2"] = subscriber.address2
            address["city"] = subscriber.city
            address["state"] = subscriber.state
            address["country"] = subscriber.country
            address["zip"] = subscriber.postcode
            fields["addresses"].append(address)

        fields["print"] = {"front": {"color_count": 1}}
        fields["address_count"] = len(self.subscribers)
        fields["test"] = test
        fields["price"] = quote["total"]

        r = requests.post(API_V1 + "/order/",
                files={"print[front][artwork]": open(self.imagefile, 'rb'), "print[front][proof]": open(self.imagefile, 'rb')},
                data=shirtsio_encode(fields))

        print r.status_code
        print r.url
        print r.text
        return json.loads(r.text).get("result")
