from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DATETIME, Float, or_
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

    @classmethod
    def sources(cls):
        return { 'apec': 1, 'pole-emploi': 2, 'linkedin': 3 }

class Contrat(Entity):
    __tablename__ = 'contrats'
    name = Column(String(50))

    # annonces = relationship('Annonce', back_populates='contrat')
    @classmethod
    def contracts(cls):
        return {'cdi': 1, 'cdd': 2, 'stage': 3, 'alternance': 4}

class Annonce(Entity):
    __tablename__ = 'annonces'

    url = Column(String(250))
    title = Column(String(250))
    company_name = Column(String(250))
    date = Column(DATETIME())
    descripiton = Column(String(250))
    poste = Column(String(250))
    activity = Column(String(250))
    profile = Column(String(250))
    skills = Column(String(250))
    
    contrat_id = Column(Integer, ForeignKey('contrats.id'), nullable=False)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)

    city = relationship('City', back_populates='annonces')

# end