import cherrypy
from ..model import AlgoshirtModel
from mako.template import Template
import json

class AppGlobals(object):
    pass
g = AppGlobals()

class Root(object):
    @cherrypy.expose
    def index(self):
        return "Hello, World!"

    @cherrypy.expose
    def subscribers(self):
        tmpl = """
        <html>
        <body>
        <ul>
        % for subscriber in subscribers:
           <li>${subscriber.name}</li> 
        % endfor
        </ul>
        </body>
        </html>
        """
        return Template(tmpl).render(subscribers=g.model.subscribers())

class API(object):
    pass

class Subscribers(object):
    exposed = True

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id == None:
            out = []
            subscribers = g.model.subscribers()
            for subscriber in subscribers:
                sobj = {
                    "id": subscriber.id,
                    "name": subscriber.name,
                    "company": subscriber.company,
                    "size": subscriber.size,
                    "address": subscriber.address,
                    "address2": subscriber.address2,
                    "city": subscriber.city,
                    "state": subscriber.state,
                    "postcode": subscriber.postcode,
                    "country": subscriber.country,
                    "active": subscriber.active
                }
                out.append(sobj)
            return out
        else:
            subscriber = g.model.subscriber(int(id))
            sobj = {
                "id": subscriber.id,
                "name": subscriber.name,
                "company": subscriber.company,
                "size": subscriber.size,
                "address": subscriber.address,
                "address2": subscriber.address2,
                "city": subscriber.city,
                "state": subscriber.state,
                "postcode": subscriber.postcode,
                "country": subscriber.country,
                "active": subscriber.active
            }
            return sobj

    @cherrypy.expose
    def POST(self, name, company, size, address, address2, city, subscriber, postcode, country, active):
        return "Create subs"

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

