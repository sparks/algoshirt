import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, create_engine
import datetime
import dateutil.parser

Base = declarative_base()

class Render(Base):
    __tablename__ = 'renders'

    id                = Column(Integer, primary_key=True)

    description       = Column(String)
    date              = Column(DateTime)
    working_dir       = Column(String)
    render_path_front = Column(String)
    render_path_back  = Column(String)

    status      = Column(String)

    def __init__(self, info=None):
        self.update(info)

    def update(self, info=None):
        if (info != None):
            if "id" in info: self.id = info["id"]

            if "description" in info: self.description = info["description"]
            if "date" in info: 
                if isinstance(info["date"], datetime.datetime):
                    self.date = info["date"]
                else:
                    self.date = dateutil.parser.parse(info["date"])

            if "working_dir" in info: self.working_dir = info["working_dir"]
            if "render_path_front" in info: self.render_path_front = info["render_path_front"]
            if "render_path_back" in info: self.render_path_back = info["render_path_back"]

            if "status" in info: self.status = info["status"]

    def to_dict(self):
        return {
            "id":                self.id,

            "description":       self.description,
            "date":              self.date.isoformat(),
            "working_dir":       self.working_dir,
            "render_path_front": self.render_path_front,
            "render_path_back":  self.render_path_back,

            "status":            self.status,
        }

class Order(Base):
    __tablename__ = 'orders'

    id               = Column(Integer, primary_key=True)

    date             = Column(DateTime)
    cost             = Column(Float)
    render_id        = Column(Integer)
    data             = Column(String)

    proof_path_front = Column(String)
    proof_path_back  = Column(String)

    status           = Column(String)

    def __init__(self, info=None):
        self.update(info)

    def update(self, info=None):
        if (info != None):
            if "id" in info: self.id = info["id"]

            if "date" in info: 
                if isinstance(info["date"], datetime.datetime):
                    self.date = info["date"]
                else:
                    self.date = dateutil.parser.parse(info["date"])
            if "cost" in info: self.cost = info["cost"]
            if "render_id" in info: self.render_id = info["render_id"]
            if "data" in info: self.data = info["data"]

            if "proof_path_front" in info: self.proof_path_front = info["proof_path_front"]
            if "proof_path_back" in info: self.proof_path_back = info["proof_path_back"]

            if "status" in info: self.status = info["status"]

    def to_dict(self):
        return {
            "id":               self.id,

            "date":             self.date.isoformat(),
            "cost":             self.cost,
            "render_id":        self.render_id,
            "data":             self.data,

            "proof_path_front": self.proof_path_front,
            "proof_path_back":  self.proof_path_back,
            
            "status":           self.status,
        }

class Subscriber(Base):
    __tablename__ = 'subscribers'

    id       = Column(Integer, primary_key=True)

    name     = Column(String)
    company  = Column(String)

    size     = Column(String)

    address  = Column(String)
    address2 = Column(String)
    city     = Column(String)
    state    = Column(String)
    postcode = Column(String)
    country  = Column(String)

    active   = Column(Boolean)

    def __init__(self, info=None):
        self.update(info)

    def update(self, info=None):
        if (info != None):
            if "id" in info: self.id = info["id"]

            if "name" in info: self.name = info["name"]
            if "company" in info: self.company = info["company"]

            if "size" in info: self.size = info["size"]

            if "address" in info: self.address = info["address"]
            if "address2" in info: self.address2 = info["address2"]
            if "city" in info: self.city = info["city"]
            if "state" in info: self.state = info["state"]
            if "postcode" in info: self.postcode = info["postcode"]
            if "country" in info: self.country = info["country"]

            if "active" in info: self.active = info["active"]

    def __repr__(self):
        return "<User({}, '{}')>".format(self.id, self.name)

    def to_dict(self):
        return {
            "id":       self.id,

            "name":     self.name,
            "company":  self.company,

            "size":     self.size,

            "address": self.address,
            "address2": self.address2,
            "city":     self.city,
            "state":    self.state,
            "postcode": self.postcode,
            "country":  self.country,

            "active":   self.active
        }

class AlgoshirtModel(object):

    def __init__(self, dburl):
        self.engine = create_engine(dburl)
        self.Session = sessionmaker(bind = self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()
