import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Boolean, Integer, create_engine

Base = declarative_base()

class Subscriber(Base):
     __tablename__ = 'subscribers'

     id = Column(Integer, primary_key=True)
     name = Column(String)
     company = Column(String)
     address = Column(String)
     address2 = Column(String)
     city = Column(String)
     state = Column(String)
     postcode = Column(String)
     size = Column(String)
     active = Column(Boolean)

     def __init__(self, name):
         self.name = name

     def __repr__(self):
        return "<User({}, '{}')>".format(self.id, self.name)

class AlgoshirtModel(object):
    def __init__(self, dburl):
        self.engine = create_engine(dburl)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
    def subscribers(self):
        return self.Session().query(Subscriber).all()


