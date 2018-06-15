"""
ORM definition
"""
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from engine import get_or_create_engine
import hashlib

Base = declarative_base()


class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True)
    hash = Column(String(40))


class Coincidence(Base):
    __tablename__ = 'coincidences'
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    type = Column(SmallInteger)
    events = relationship('Event', order_by='Event.index')

    def __repr__(self):
        return "<Coincidence(id={}, is_scatter={}, photons={})>".format(
            self.id, self.is_scatter, self.photons)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    coincidence_id = Column(Integer, ForeignKey('coincidences.id'))
    photons = relationship('Photon', order_by='Photon.index')

    def __repr__(self):
        return "<Event(id={}, index={}, expr={}, photons={})>".format(
            self.id, self.index, self.experiment.hash[:4], self.photons)


def get_experiment_hash(conincidence_csv, hits_csv):
    sha1 = hashlib.sha1()
    for p in [conincidence_csv, hits_csv]:
        with open(p, 'r') as fin:
            sha1.update(fin.read().encode())
    return sha1.hexdigest()


class Photon(Base):
    __tablename__ = 'photons'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship("Experiment")
    event_id = Column(Integer, ForeignKey('events.id'))
    hits = relationship('Hit', order_by='Hit.index')

    def __repr__(self):
        return "<Photon(id={}, index={}, hits={})>".format(
            self.id, self.index, self.hits)


class Hit(Base):
    __tablename__ = 'hits'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship(Experiment)
    photon_id = Column(Integer, ForeignKey('photons.id'))

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    energy = Column(Float)
    time = Column(Float)

    def __repr__(self):
        return "<Hit(id={}, index={}, x={}, y={}, z={}, energy={}, time={})>".format(
            self.id, self.index, self.x, self.y, self.z, self.energy,
            self.time)

    def to_list(self, columns):
        return [getattr(self, c) for c in columns]


_created = False


def create_all(path):
    global _created
    if not _created:
        Base.metadata.create_all(get_or_create_engine(path))
        _created = True
