import cherrypy
from ..model import AlgoshirtModel, Subscriber
from mako.template import Template
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

class AppGlobals(object):
    pass
g = AppGlobals()

class Root(object):
    pass

class API(object):
    pass

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
    def POST(self):
        self.CORS()
        info = json.load(cherrypy.request.body)
        subscriber = Subscriber(info=info)
        g.model.addSubscriber(subscriber)
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

def serve(config):
    root = Root()

    g.application = cherrypy.tree.mount(
        Root(), "/", 
        config
    )

    g.model = AlgoshirtModel(g.application.config["Database"]["url"])
    
    api = API()
    api.subscribers = Subscribers()

    cherrypy.tree.mount(
        api, '/api',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.engine.start()
    cherrypy.engine.block()

