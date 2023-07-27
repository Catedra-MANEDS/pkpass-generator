#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, Text, Date, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship 

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

"""------------------------------------Campañas------------------------------------------"""
class Clientes(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80))
    edad = Column(Integer)
    correo = Column(String(120))
    fecha_fin_contrato = Column(Date)
    fecha_inicio_contrato = Column(Date)
    genero = Column(String(15))
    ruta_directorio_pass = Column(String(200))

    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'))
    campaign = relationship('Campaigns', backref='clientes')

class Campaigns(Base):
    __tablename__ = 'campaigns'
    campaign_id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_title = Column(String(100), nullable=False)
    begin_date = Column(Date)
    end_date = Column(Date)
    status = Column(Boolean)

    campaign_notifications = relationship('Campaign_notifications', back_populates='campaign')
    campaign_rules = relationship('Campaign_rules', back_populates='campaign')

class Campaign_notifications(Base):
    __tablename__ = 'campaign_notifications'
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'), primary_key=True)
    message = Column(String(255), nullable=False)
    pass_field_to_update = Column(String(150))

    campaign = relationship('Campaigns', back_populates='campaign_notifications')

class Campaign_rules(Base):
    __tablename__ = 'campaign_rules'
    campaign_id = Column(Integer, ForeignKey('campaigns.campaign_id'), primary_key=True)
    age_start = Column(Integer)
    age_end = Column(Integer)
    gender = Column(String(15))
    begin_date = Column(Date)
    end_date = Column(Date)

    campaign = relationship('Campaigns', back_populates='campaign_rules')

Base.metadata.create_all(engine)
