import json
import algoshirt.optimizers as optimizers
import algoshirt.algorithms as algorithms
import cherrypy
import uuid
from ..model import AlgoshirtModel, Subscriber, Render, Order
from mako.template import Template
import json
import os
import datetime
from algoshirt.backends.shirtsio import ShirtsIOBatch
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))

class RenderThread(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)

    def run(self):
        base_filename = "random-optimizer-{0}".format(args.uuid)
        png_filename = os.path.join(args.renders_dir, "{0}.png".format(base_filename))
        json_filename = os.path.join(args.renders_dir, "{0}.json".format(base_filename))

        random_render_instance = optimizers.randomize(algorithms.FractalDots)

        random_render_instance.render_to_png(
            png_filename,
            2000,
            2000
        )

        params_file = open(json_filename, "w")
        json.dump(random_render_instance.params, params_file)
        params_file.close()

class AppGlobals(object):
    pass
g = AppGlobals()

class Root(object):
    pass

class API(object):
    pass

class Renders(object):
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        CORS()
        session = g.model.get_session()

        if id == None:
            out = []
            renders = session.query(Render).all()
            for render in renders:
                out.append(render.to_dict())
            session.close()
            return out
        else:
            subscriber = session.query(Render).filter(Render.id == int(id)).first()
            s_dict = subscriber.to_dict()
            session.close()            
            return s_dict

    @cherrypy.tools.json_out()
    def POST(self):
        CORS()
        session = g.model.get_session()

        render_path = os.path.join(g.renders_dir, uuid.uuid4())
        render = Render({"description": "basic render", "date": datetime.datetime.now(), "working_dir": render_path, "status": 0})

        session.add(render)
        session.commit() # commit now so we get an id
        s_dict = render.to_dict()
        session.close()
        return s_dict

    @cherrypy.expose
    def DELETE(self, id=None):
        CORS()
        session = g.model.get_session()
        render = session.query(Render).filter(Render.id == int(id)).first()
        session.delete(render)
        session.commit()
        session.close()  

    @cherrypy.expose
    def OPTIONS(self, id=None):
        CORS()

class Orders(object):
    exposed = True

    def __init(self):
        self.batch = None

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        CORS()
        session = g.model.get_session()

        if id == None:
            out = []
            renders = session.query(Render).all()
            for render in renders:
                out.append(render.to_dict())
            session.close()
            return out
        else:
            subscriber = session.query(Render).filter(Render.id == int(id)).first()
            s_dict = subscriber.to_dict()
            session.close()            
            return s_dict

    @cherrypy.tools.json_out()
    def POST(self):
        CORS()
        # req = json.load(cherrypy.request.body)
        # if "action" in req:
        #     if req["action"] == "prepare":
        #         return "prepare!"
        #     elif req["action"] == "quote":
        #         self.batch = ShirtsIOBatch(
        #             g.apikey, 
        #             g.model.subscribers(), 
        #             "./renders/test.png", 
        #             "./renders/test.jpg", 
        #             "As large as possible", 
        #             "Centered",
        #             "black", 
        #             11, 
        #             1
        #         )
        #         return self.batch.quote()
        #     elif req["action"] == "place":
        #         if "args" in req and self.batch != None:
        #             return self.batch.order(req["args"])

    @cherrypy.expose
    def DELETE(self, id=None):
        CORS()
        session = g.model.get_session()
        order = session.query(Order).filter(Order.id == int(id)).first()
        session.delete(order)
        session.commit()
        session.close()

    @cherrypy.expose
    def OPTIONS(self, id=None):
        CORS()

class Subscribers(object):
    exposed = True

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self, id=None):
        CORS()
        session = g.model.get_session()

        if id == None:
            out = []
            subscribers = session.query(Subscriber).all()
            for subscriber in subscribers:
                out.append(subscriber.to_dict())
            session.close()
            return out
        else:
            subscriber = session.query(Subscriber).filter(Subscriber.id == int(id)).first()
            s_dict = subscriber.to_dict()
            session.close()            
            return s_dict

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self, id=None):
        CORS()
        session = g.model.get_session()

        if id == None:
            info = json.load(cherrypy.request.body)
            subscriber = Subscriber(info)
            session.add(subscriber)
            session.commit() # commit now so we get an id
            s_dict = subscriber.to_dict()
            session.close()
            return s_dict
        else:
            info = json.load(cherrypy.request.body)
            subscriber = session.query(Subscriber).filter(Subscriber.id == int(id)).first()
            subscriber.update(info)
            session.commit()
            s_dict = subscriber.to_dict()
            session.close()
            return s_dict

    @cherrypy.expose
    def DELETE(self, id=None):
        CORS()
        session = g.model.get_session()
        subscriber = session.query(Subscriber).filter(Subscriber.id == int(id)).first()
        session.delete(subscriber)
        session.commit()
        session.close()

    @cherrypy.expose
    def OPTIONS(self, id=None):
        CORS()

def CORS():
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
    g.renders_dir = AlgoshirtModel(g.application.config["Render"]["dir"])
    
    api = API()
    api.subscribers = Subscribers()
    api.renders = Renders()
    api.orders = Orders()

    cherrypy.tree.mount(
        api, '/api',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.engine.start()
    cherrypy.engine.block()


    # @cherrypy.tools.json_out()
    # def POST(self):
    #     req = json.load(cherrypy.request.body)
    #     if "action" in req:
    #         if req["action"] == "prepare":
    #             return "prepare!"
    #         elif req["action"] == "quote":
    #             self.batch = ShirtsIOBatch(
    #                 g.apikey, 
    #                 g.model.subscribers(), 
    #                 "./renders/test.png", 
    #                 "./renders/test.jpg", 
    #                 "As large as possible", 
    #                 "Centered",
    #                 "black", 
    #                 11, 
    #                 1
    #             )
    #             return self.batch.quote()
    #         elif req["action"] == "place":
    #             if "args" in req and self.batch != None:
    #                 return self.batch.order(req["args"])
