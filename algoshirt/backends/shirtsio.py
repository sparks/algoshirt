''' Order a shirt from the shirts.io API
'''

import os
import json
import requests

API_V1 = "https://www.shirts.io/api/v1"

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
    def __init__(self, apikey, subscribers, front_file, proof_file, dimensions, placement, color, color_count, product_id):
        self.apikey = apikey
        self.subscribers = subscribers
        self.front_file = front_file
        self.proof_file = proof_file
        self.dimensions = dimensions
        self.placement = placement
        self.color = color
        self.color_count = color_count
        self.product_id = product_id

    def build_request(self):
        fields = {}
        fields["api_key"] = self.apikey
        fields["garment"] = []
        fields["addresses"] = []
        for i, subscriber in enumerate(self.subscribers):
            garment = {}
            garment["product_id"] = self.product_id
            garment["color"] = self.color
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
            address["zipcode"] = subscriber.postcode
            fields["addresses"].append(address)

        fields["print"] = {
            "front": {
                "color_count": self.color_count,
                "dimensions": self.dimensions,
                "placement": self.placement
            }
        }

        fields["address_count"] = len(self.subscribers)
        fields["international_garments"] = {"CA": len(self.subscribers)}

        return fields

    def quote(self):
        fields = self.build_request()
        r = requests.get(API_V1 + "/quote", params=shirtsio_encode(fields))
        return json.loads(r.text).get("result")

    def order(self, quote, test=True):
        fields = self.build_request()
        fields["test"] = test
        fields["price"] = quote["total"]

        r = requests.post(API_V1 + "/order/",
                files = {"print[front][artwork]": open(self.front_file, 'rb'), "print[front][proof]": open(self.proof_file, 'rb')},
                data = shirtsio_encode(fields))

        return json.loads(r.text)
