import cherrypy
from ..model import AlgoshirtModel, Subscriber
from mako.template import Template
import json
import os
from algoshirt.backends.shirtsio import ShirtsIOBatch

current_dir = os.path.dirname(os.path.abspath(__file__))

class AppGlobals(object):
    pass
g = AppGlobals()

class Root(object):
    pass

class API(object):
    pass

class Order(object):
    exposed = True

    def __init(self):
        self.batch = None

    @cherrypy.tools.json_out()
    def GET(self):
        return "comingsoon"

    @cherrypy.tools.json_out()
    def POST(self):
        req = json.load(cherrypy.request.body)
        if "action" in req:
            if req["action"] == "prepare":
                return "prepare!"
            elif req["action"] == "quote":
                self.batch = ShirtsIOBatch(
                    g.apikey, 
                    g.model.subscribers(), 
                    "./renders/test.png", 
                    "./renders/test.jpg", 
                    "As large as possible", 
                    "Centered",
                    "black", 
                    11, 
                    1
                )
                return self.batch.quote()
            elif req["action"] == "place":
                if "args" in req and self.batch != None:
                    return self.batch.order(req["args"])

class Subscribers(object):
    exposed = True

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, id=None):
        self.CORS()
        if id == None:
            out = []
            subscribers = g.model.subscribers()
            for subscriber in subscribers:
                out.append(subscriber.to_dict())
            return out
        else:
            subscriber = g.model.subscriber(int(id))
            return subscriber.to_dict()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self, id=None):
        self.CORS()
        if id == None:
            info = json.load(cherrypy.request.body)
            subscriber = Subscriber(info)
            g.model.addSubscriber(subscriber)
            return subscriber.to_dict()
        else:
            info = json.load(cherrypy.request.body)
            subscriber = g.model.subscriber(int(id))
            subscriber.update(info)
            g.model.mergeSubscriber(subscriber)
            return subscriber.to_dict()

    @cherrypy.expose
    def DELETE(self, id=None):
        self.CORS()
        g.model.removeSubscriber(id)

    @cherrypy.expose
    def OPTIONS(self, id=None):
        self.CORS()
        return ""

    def CORS(self):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, X-PINGOTHER"

def serve(config, apikey):
    root = Root()

    g.apikey = apikey

    g.application = cherrypy.tree.mount(
        Root(), "/", 
        config
    )

    g.model = AlgoshirtModel(g.application.config["Database"]["url"])
    
    api = API()
    api.subscribers = Subscribers()
    api.order = Order()

    cherrypy.tree.mount(
        api, '/api',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.engine.start()
    cherrypy.engine.block()

