import pandas as pd
import os
from sqlalchemy import Column, Float, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, Session
import streamlit as st
import pandas as pd


# Se crea lista de horarios de funcionamiento
# esta información puede venir desde otro Excel, CSV o API

climas = [
  "28.21",
  "28",
  "29.04",
  "27.7",
  "26.78",
  "28.87",
]

pronostico = [
  "cielo claro"
]


def asigna_clima(data):
  comuna=data["Comuna"]

  if(comuna=="ÑUÑOA"):
    return climas[24.5]
  elif(comuna=="LA FLORIDA"):
    return climas[28]
  elif(comuna=="RENCA"):
    return climas[29.04]
  elif(comuna=="LAS CONDES"):
    return climas[23.65]
  elif(comuna=="PROVIDENCIA"):
    return climas[26.78]
  elif(comuna=="HUECHURABA"):
    return climas[28.87]

@st.cache
def atrac_data():
  # Se lee Excel de datos
 atrac=pd.read_excel("Tabla_atrac_utm.xlsx", header=0)

  # Obtener columnas de datos
 data_turist = atrac[ ["FID","JERARQUIA", "TIPO", "NOMBRE", "REGION", "DIRECCION", "COMUNA", "POINT_x", "POINT_y"]]

  # Corregir los nombres de las columnas
 atrac_data_turist = data_turist.rename(columns={
    "JERARQUIA": "ESCALA", 
    "POINT_X": "PUNTO_X", 
    "POINT_Y": "PUNTO_Y"
  })

 atrac_data_turist["FECHA DE PROCESO"] = "18-11-2022"

  # Asignar valores de horarios a la columna de Horario,
  # para esto se aplica una lógica usando todas las columnas de cada registro
 atrac_data_turist["CLIMAS"] = atrac_data_turist.apply(asigna_clima, axis=1)
 atrac_data_turist["PRONOSTICOS"] = pronostico

 print(atrac_data_turist)


 ruta_mi_bd = os.path.abspath("./cargas.db")
 mi_bd = f"sqlite:///{ruta_mi_bd}"
# En caso de ser una base de datos PostgreSQL, el formato sería:
# mi_bd = f"postgres://usuario:clave@servidor/base_de_datos"

# Conectar a la BD
# El parámetro echo=True, muestra en consola lo que genera SQLAlchemy
# El parámetro future=True, activa las funcionalidades de la versión 2.x
 engine = create_engine(mi_bd, echo=True, future=True)

#lectura del dataframe
 turist = pd.DataFrame(atrac_data_turist)

 # Grabar DataFrame en BD
 turist.to_sql(con=engine, name="AtractivosTuristos", if_exists="replace", index_label="FID")

# Crear la tabla en BD
 Base.metadata.create_all(engine)

  # Crear sesión a BD
 
 session = Session(engine)


# Crear clase de Modelo de Datos SQLAlchemy
Base = declarative_base()
class AtracTurist(Base):
   # Nombre de la tabla
    __tablename__ = "AtractivosTuristos"
 
  # Definir cada atributo de la tabla y su tipo de dato
    FID = Column(Integer, primary_key=True)
    ESCALA = Column(String(100))
    NOMBRE = Column(String(100))
    REGION = Column(String(100))
    DIRECCION = Column(String(100))
    COMUNA = Column(String(100))
    TEMPERATURA = Column(Integer)
    PRONOSTICO = Column(Integer)
    PUNTO_X = Column(Float)
    PUNTO_Y = Column(Float)

    def __repr__(self) -> str:
      return f" AtractTurist(FID={self.FID}, ESCALA={self.ESCALA}, NOMBRE={self.NOMBRE}, " \
      + f"REGION={self.REGION}, DIRECCION={self.DIRECCION}, COMUNA={self.COMUNA}," \
      + f"TEMPERATURA={self.TEMPERATURA}, PRONOSTICO={self.PRONOSTICO}, PUNTO_X={self.PUNTO_X}, PUNTO_Y={self.PUNTO_Y}" \
      + ")"
 















