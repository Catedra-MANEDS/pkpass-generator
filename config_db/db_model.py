#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base,sessionmaker

#Conexion con la bd
username = "samuel"
password = "hola"
dbname = "passData"
DATABASE_URI = f"postgresql://{username}:{password}@34.175.112.41:5432/{dbname}"
engine = create_engine(DATABASE_URI)

Base = declarative_base()

#Modelos de la bd
class Registrations(Base):
    __tablename__ = 'registrations'
    pkid = Column(Integer, primary_key=True)
    devicelibraryidentifier = Column(String(100))
    passtypeidentifier = Column(String(100))
    serialnumber=Column(String(100))
    updatetimestamp=Column(TIMESTAMP(timezone=False))

class Passes(Base):
    __tablename__ = 'passes'
    pkid = Column(Integer, primary_key=True)
    passtypeidentifier = Column(String(100))
    serialnumber = Column(String(100))
    pkpass_name = Column(String(150))
    pkpass_route = Column(String(200))
    updatetimestamp=Column(TIMESTAMP(timezone=False))
    passdatajson=Column(Text)

    __table_args__ = (
        UniqueConstraint('passtypeidentifier', 'serialnumber', name='unique_passes'),
    )

class Devices(Base):
    __tablename__ = 'devices'
    pkid = Column(Integer, primary_key=True)
    devicelibraryidentifier = Column(String(100))
    pushtoken = Column(String(100))
    updatetimestamp=Column(TIMESTAMP(timezone=False))

class Apilog(Base):
    __tablename__ = 'apilog'
    pkid = Column(Integer, primary_key=True)
    apilog = Column(String(5000))
    timestamp= Column(TIMESTAMP(timezone=False))
    
class Authentication(Base):
    __tablename__ = 'authentication'
    authid = Column(Integer, primary_key=True)
    authenticationtoken = Column(String(100))
    pkpass_name= Column(String(100))

Base.metadata.create_all(engine)
