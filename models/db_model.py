#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, Text, Date, Boolean
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

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80))
    edad = Column(Integer)
    correo = Column(String(120))
    fecha_fin_contrato = Column(Date)
    fecha_inicio_contrato = Column(Date)
    genero = Column(String(15))  # Puedes ajustar la longitud según tus necesidades
    mes_registro = Column(String(20))  # Puedes ajustar la longitud según tus necesidades

"""---------------------MODELO DE TABLAS DE CAMPAÑAS DE NOTIFICACIONES------------------"""

# Modelo de la tabla "Campaigns"
class Campaigns(Base):

    __tablename__ = 'Campaigns'

    Campaign_ID = Column(Integer, primary_key=True, autoincrement=True)
    Campaign_title = Column(String(100), nullable=False)
    BeginDate = Column(Date)
    EndDate = Column(Date)
    Status = Column(Boolean)

# Modelo de la tabla "Campaign_notifications"
class Campaign_notifications(Base):

    __tablename__ = 'Campaign_notifications'

    Campaign_ID = Column(Integer, ForeignKey('Campaigns.Campaign_ID'), primary_key=True)
    Message = Column(String(255), nullable=False)
    Pass_field_to_update = Column(String(150))

# Modelo de la tabla "Campaign_rules"
class Campaign_rules(Base):

    __tablename__ = 'Campaign_rules'

    Campaign_ID = Column(Integer, ForeignKey('Campaigns.Campaign_ID'), primary_key=True)
    Age_start = Column(Integer)
    Age_end = Column(Integer)
    Gender = Column(String(15))
    BeginDate = Column(Date)
    EndDate = Column(Date)

# Modelo de la tabla "CampaignsSubscriptions"
class Campaigns_subscriptions(Base):

    __tablename__ = 'Campaigns_subscriptions'

    Campaign_ID = Column(Integer, ForeignKey('Campaigns.Campaign_ID'), primary_key=True)
    serialnumber = Column(String(100))
    passTypeIdentifier = Column(String(100))
    pushToken = Column(String(150))

Base.metadata.create_all(engine)
