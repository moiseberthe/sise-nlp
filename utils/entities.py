from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from database.connector import SessionLocal, engine


Base = declarative_base()
db = SessionLocal()

class Entity(Base):
    __abstract__ = True
    id = Column(Integer, Sequence('entity_id_seq'), primary_key=True)

    @classmethod
    def create_table(cls):
        try:
            cls.__table__.create(engine)
        except OperationalError:
            pass

    def create(self):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    @classmethod
    def find(cls, id: int):
        return db.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def find_all(cls, offset: int = 0, limit: int = 10):
        return db.query(cls).offset(offset).limit(limit).all()
    
    @classmethod
    def delete(cls, id: int):
        entity = cls.find(id)
        if entity:
            db.delete(entity)
            db.commit()
            return entity
    
    @classmethod
    def query(cls):
        return db.query(cls)
    

class Region(Entity):
    __tablename__ = 'regions'
    
    name = Column(String(50))

    departements = relationship('Departement', back_populates='region')

class Departement(Entity):
    __tablename__ = 'departements'
    
    name = Column(String(50))
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    
    region = relationship('Region', back_populates='departements')

class City(Entity):
    __tablename__ = 'cities'
    name = Column(String(50))

    departement_id = Column(Integer, ForeignKey('departements.id'), nullable=False)

class Source(Entity):
    __tablename__ = 'sources'
    name = Column(String(50))

class Contrat(Entity):
    __tablename__ = 'contrats'
    name = Column(String(50))

    # annonces = relationship('Annonce', back_populates='contrat')


class Annonce(Entity):
    __tablename__ = 'annonces'

    url = Column(String(250))
    title = Column(String(250))
    company_name = Column(String(250))
    location = Column(String(250))
    date = Column(String(250))
    descripiton = Column(String(250))
    poste = Column(String(250))
    activity = Column(String(250))
    profile = Column(String(250))
    skills = Column(String(250))
    
    contrat_id = Column(Integer, ForeignKey('contrats.id'), nullable=False)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)

    # contrat = relationship('Contrat', back_populates='annonces')
    # teletravail = Column(BOOLEAN, nullable=False)
