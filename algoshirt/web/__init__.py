import cherrypy
from ..model import AlgoshirtModel
from mako.template import Template

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


def serve(config):
    g.application = cherrypy.tree.mount(Root(), "/", config)
    for k,v in g.application.config.iteritems():
        print k,v
    g.model = AlgoshirtModel(g.application.config["Database"]["url"])
    cherrypy.engine.start()
    cherrypy.engine.block()
    #cherrypy.quickstart(Root(), config=config)
