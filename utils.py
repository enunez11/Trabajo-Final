import pandas as pd
import os
from sqlalchemy import Column, Float, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, Session
import streamlit as st
import requests
from urllib.parse import quote
from dotenv import load_dotenv



load_dotenv()

datos_clima=os.getenv("API_KEY")

lista_comunas = [
  "ÑUÑOA",
  "LA FLORIDA",
  "RENCA",
  "LAS CONDES",
  "PROVIDENCIA",
  "HUECHURABA"
]
clima = []
pronosticos = []

for ubicacion in lista_comunas:
  # Acá se ajusta el nombre de la comuna para hacerla compatible a consulta a la API.
  # Además se agrega una coma y el código de país al que pertenece la comuna, en este caso "CL" por ser Chile.
  ubicacion = quote(ubicacion) + ",CL"

  URL = f"https://api.openweathermap.org/data/2.5/weather?q={ubicacion}&appid={datos_clima}&units=metric&lang=es"
  datos = requests.get(URL)
  datos_json = datos.json()
  temperatura = datos_json["main"]["temp"]
  pronostico = datos_json["weather"][0]["description"]
  clima.append(temperatura)
  pronosticos.append(pronostico)

print("Comunas: ",lista_comunas)
print("Climas: ", clima)
print("Pronósticos: ", pronosticos)
print(lista_comunas)





def asigna_clima(data):
  comuna=data["Comuna"]

  if(comuna=="ÑUÑOA"):
    return clima
  elif(comuna=="LA FLORIDA"):
    return clima
  elif(comuna=="RENCA"):
    return clima
  elif(comuna=="LAS CONDES"):
    return clima
  elif(comuna=="PROVIDENCIA"):
    return clima
  elif(comuna=="HUECHURABA"):
    return clima

def asigna_pronostico(data):
  comuna=data["Comuna"]

  if(comuna=="ÑUÑOA"):
    return pronosticos
  elif(comuna=="LA FLORIDA"):
    return pronosticos
  elif(comuna=="RENCA"):
    return pronosticos
  elif(comuna=="LAS CONDES"):
    return pronosticos
  elif(comuna=="PROVIDENCIA"):
    return pronosticos
  elif(comuna=="HUECHURABA"):
    return pronosticos

@st.cache
def tur_data():
  # Se lee Excel de datos
 atrac=pd.read_excel("Tabla_atrac_utm.xlsx", header=0)

  # Obtener columnas de datos
 data_turist = atrac[ ["FID","JERARQUIA", "TIPO", "NOMBRE", "REGION", "DIRECCION", "COMUNA", "POINT_x", "POINT_y"]]

  # Corregir los nombres de las columnas
 tur_data_turist = data_turist.rename(columns={
    "JERARQUIA": "ESCALA", 
    "POINT_X": "PUNTO_X", 
    "POINT_Y": "PUNTO_Y"
  })

 tur_data_turist["FECHA DE PROCESO"] = "18-11-2022"

  # Asignar valores de horarios a la columna de Horario,
  # para esto se aplica una lógica usando todas las columnas de cada registro
 tur_data_turist["CLIMA"] = tur_data_turist.apply(asigna_clima, axis=1)
 tur_data_turist["PRONOSTICO"] = tur_data_turist.apply(asigna_pronostico, axis=1)

 return(tur_data_turist)


 

ruta_mi_bd = os.path.abspath("./cargas.db")
mi_bd = f"sqlite:///{ruta_mi_bd}"
#Conectar a la BD

engine = create_engine(mi_bd, echo=True, future=True)

#lectura del dataframe
turist = pd.DataFrame(tur_data)

# Grabar DataFrame en BD
turist.to_sql(con=engine, name="AtractivosTuristos", if_exists="replace", index_label="FID")

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
    CLIMA = Column(Integer)
    PRONOSTICO = Column(Integer)
    PUNTO_X = Column(Float)
    PUNTO_Y = Column(Float)

    def __repr__(self) -> str:
      return f" AtractTurist(FID={self.FID}, ESCALA={self.ESCALA}, NOMBRE={self.NOMBRE}, " \
      + f"REGION={self.REGION}, DIRECCION={self.DIRECCION}, COMUNA={self.COMUNA}," \
      + f"TEMPERATURA={self.TEMPERATURA}, PRONOSTICO={self.PRONOSTICO}, PUNTO_X={self.PUNTO_X}, PUNTO_Y={self.PUNTO_Y}" \
      + ")"















