"""
ORM definition
"""
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from engine import engine
Base = declarative_base()


class Coincidence(Base):
    __tablename__ = 'coincidences'
    id = Column(Integer, primary_key=True)
    photons = relationship('Photon', order_by='Photon.index')
    is_scatter = Column(Boolean)

    def __repr__(self):
        return "<Coincidence(id={}, is_scatter={}, photons={})>".format(
            self.id, self.is_scatter, self.photons)


class Photon(Base):
    __tablename__ = 'photons'
    id = Column(Integer, primary_key=True)
    coincidence_id = Column(Integer, ForeignKey('coincidences.id'))
    index = Column(Integer)
    hits = relationship('Hit', order_by='Hit.index')

    def __repr__(self):
        return "<Photon(id={}, index={}, hits={})>".format(
            self.id, self.index, self.hits)


class Hit(Base):
    __tablename__ = 'hits'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
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



Base.metadata.create_all(engine)