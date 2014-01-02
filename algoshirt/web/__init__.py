import os, threading, uuid, datetime, json

import cherrypy
from mako.template import Template

import algoshirt.optimizers as optimizers
import algoshirt.algorithms.renderers as renderers

from algoshirt.model import *
from algoshirt.backends import *

current_dir = os.path.dirname(os.path.abspath(__file__))

class RenderThread(threading.Thread):
    def __init__(self, render_id):
        threading.Thread.__init__(self)
        self.render_id = render_id

    def run(self):
        session = g.model.get_session()

        render = session.query(Render).filter(Render.id == int(self.render_id)).first()
        render.status = "rendering";
        session.commit()

        qualified_working_dir = os.path.join(g.renders_dir, render.working_dir)

        if not os.path.exists(qualified_working_dir):
            os.mkdir(qualified_working_dir)

        render.render_path_front = os.path.join(render.working_dir, "render.png")

        # random_render_instance = optimizers.randomize(renderers.BigPixels)
        random_render_instance = optimizers.randomize(renderers.FractalDots)
        random_render_instance.render_to_png(
            os.path.join(g.renders_dir, render.render_path_front),
            700,
            700
        )

        params_path = os.path.join(qualified_working_dir, "params.json")
        params_file = open(params_path, "w")
        json.dump(random_render_instance.params, params_file)
        params_file.close()

        render.status = "done"
        session.commit()
    
        session.close()            


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
            renders = session.query(Render).order_by(Render.date.desc())
            for render in renders:
                out.append(render.to_dict())
            session.close()
            return out
        else:
            render = session.query(Render).filter(Render.id == int(id)).first()
            s_dict = render.to_dict()
            session.close()            
            return s_dict

    @cherrypy.tools.json_out()
    def POST(self):
        CORS()
        session = g.model.get_session()

        working_dir = str(uuid.uuid4())
        render = Render({"description": "basic render", "date": datetime.datetime.now(), "working_dir": working_dir, "status": "queued"})

        session.add(render)
        session.commit() # commit now so we get an id

        render_thread = RenderThread(render.id)
        render_thread.start()

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

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        CORS()
        session = g.model.get_session()

        if id == None:
            out = []
            orders = session.query(Order).all()
            for order in orders:
                out.append(order.to_dict())
            session.close()
            return out
        else:
            order = session.query(Order).filter(Order.id == int(id)).first()
            s_dict = order.to_dict()
            session.close()            
            return s_dict

    @cherrypy.tools.json_out()
    def POST(self, id=None, action=None):
        CORS()
        session = g.model.get_session()

        if id == None:
            info = json.load(cherrypy.request.body)

            asso_render = session.query(Render).filter(Render.id == info["render_id"]).first()

            if asso_render == None:
                session.close()
                raise cherrypy.HTTPError(400, "Invalid render_id")

            order = Order({"render_id": asso_render.id, "date": datetime.datetime.now(), "status": "noquote"})

            session.add(order)
            session.commit() # commit now so we get an id
            s_dict = order.to_dict()
            session.close()
            return s_dict
        elif action != None:
            order = session.query(Order).filter(Order.id == int(id)).first()

            if order == None:
                session.close()
                raise cherrypy.HTTPError(400, "No such order id")

            if action == "quote":
                render = session.query(Render).filter(Render.id == order.render_id).first()

                order.proof_path_front = os.path.join(render.working_dir, "proof-front.jpg")

                qualified_render_path_front = os.path.join(g.renders_dir, render.render_path_front)
                qualified_proof_path_front = os.path.join(g.renders_dir, order.proof_path_front)
                g.proofer.jpg_from_png(qualified_render_path_front, qualified_proof_path_front)

                batch = ShirtsIOBatch(
                    g.apikey,
                    session.query(Subscriber).all(),
                    qualified_render_path_front,
                    qualified_proof_path_front,
                    "As large as possible",
                    "Centered",
                    "black",
                    11,
                    1
                )

                quote = batch.quote()
                order.data = json.dumps(quote)
                order.cost = quote["total"]
                order.status = "quote"
            elif action == "place":
                render = session.query(Render).filter(Render.id == order.render_id).first()

                qualified_render_path_front = os.path.join(g.renders_dir, render.render_path_front)
                qualified_proof_path_front = os.path.join(g.renders_dir, order.proof_path_front)

                batch = ShirtsIOBatch(
                    g.apikey,
                    session.query(Subscriber).all(),
                    qualified_render_path_front,
                    qualified_proof_path_front,
                    "As large as possible",
                    "Centered",
                    "black",
                    11,
                    1
                )

                quote = json.loads(order.data)
                order.data = json.dumps(batch.order(quote))
                order.status = "placed"
            else:
                session.close()
                raise cherrypy.HTTPError(400, "Malformed request, invalid action given")

            session.commit()
            s_dict = order.to_dict()
            session.close()
            return s_dict
        else:
            session.close()
            raise cherrypy.HTTPError(400, "Malformed request, no action given")

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
    g.renders_dir = g.application.config["Render"]["dir"]
    g.proofer = ShirtProof(g.application.config["Proof"]["path"], 182, 150, 215, 300)
    
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
