from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DATETIME, Float, or_
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from database.connector import SessionLocal, engine
from pydantic import BaseModel

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
    def find_all(cls, offset: int = None, limit: int = None):
        query = db.query(cls)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query.all()
    
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
    
    @classmethod
    def db(cls):
        return db

class Region(Entity):
    __tablename__ = 'regions'
    
    code = Column(String(3), nullable=False, unique=True)
    name = Column(String(50), nullable=False)

    departments = relationship('Department', back_populates='region')

class Department(Entity):
    __tablename__ = 'departments'
    
    code = Column(String(3), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    region_code = Column(String(3), ForeignKey('regions.code'), nullable=False)
    
    region = relationship('Region', back_populates='departments')
    cities = relationship('City', back_populates='department')

class City(Entity):
    __tablename__ = 'cities'
    
    name = Column(String(250))
    zip_code = Column(String(6))
    gps_lat = Column(Float())
    gps_lng = Column(Float())

    department_code = Column(String(3), ForeignKey('departments.code'), nullable=False)

    department = relationship('Department', back_populates='cities')
    annonces = relationship('Annonce', back_populates='city')

    @classmethod
    def find_by_name(cls, name):
        name = name.lower().strip()
        name = name.replace('st.', 'Saint')
        name = name.replace('st-', 'Saint-')
        name = name.replace("’", "'")
        
        city = City.query().filter(
            or_(City.name.like(name), City.zip_code.like(name))
        ).all()
        if(len(city) > 0):
            return city[0]
        return None

class Source(Entity):
    __tablename__ = 'sources'
    name = Column(String(50))
    annonces = relationship('Annonce', back_populates='source')

    @classmethod
    def sources(cls):
        return { 'apec': 1, 'pole-emploi': 2, 'linkedin': 3 }

class Contrat(Entity):
    __tablename__ = 'contrats'
    name = Column(String(50))
    annonces = relationship('Annonce', back_populates='contrat')

    # annonces = relationship('Annonce', back_populates='contrat')
    @classmethod
    def contracts(cls):
        return {'cdi': 1, 'cdd': 2, 'stage': 3, 'alternance': 4}

class Activity(Entity):
    __tablename__ = "activities"

    name = Column(String(250))
    annonces = relationship('Annonce', back_populates='activity')

    @classmethod
    def find_by_name(cls, name):
        name = name.lower().strip()
        
        activity = cls.query().filter(cls.name.like(f"%{name}%")).all()
        if(len(activity) > 0):
            return activity[0]
        return None

class Job(Entity):
    __tablename__ = 'jobs'

    name = Column(String(250))
    annonces = relationship('Annonce', back_populates='job')

    @classmethod
    def find_by_name(cls, name):
        name = name.lower().strip()
        
        job = cls.query().filter(cls.name.like(f"%{name}%")).all()
        if(len(job) > 0):
            return job[0]
        return None

class Annonce(Entity):
    __tablename__ = 'annonces'

    url = Column(String(250))
    title = Column(String(250))
    company_name = Column(String(250))
    date = Column(DATETIME())
    description = Column(String(250))
    profile = Column(String(250))
    skills = Column(String(250))
    
    activity_id = Column(Integer, ForeignKey('activities.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    contrat_id = Column(Integer, ForeignKey('contrats.id'), nullable=False)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)

    source = relationship('Source', back_populates='annonces')
    contrat = relationship('Contrat', back_populates='annonces')
    city = relationship('City', back_populates='annonces')
    activity = relationship('Activity', back_populates='annonces')
    job = relationship('Job', back_populates='annonces')


class Chat(BaseModel):
    text: str = ''

# end