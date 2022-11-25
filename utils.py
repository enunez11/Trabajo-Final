import streamlit as st
import pandas as pd

# Se crea lista de horarios de funcionamiento
# esta información puede venir desde otro Excel, CSV o API




def asigna_clima(data):
  comuna=data["Comuna"]

  if(comuna=="ÑUÑOA"):
    return clima[24.5]
  elif(comuna=="LA FLORIDA"):
    return clima[28]
  elif(comuna=="RENCA"):
    return clima[29.04]
  elif(comuna=="LAS CONDES"):
    return clima[23.65]
  elif(comuna=="PROVIDENCIA"):
    return clima[26.78]
  elif(comuna=="HUECHURABA"):
    return clima[28.87]


@st.cache
def atrac_data():
  # Se lee Excel de datos
  atrac=pd.read_excel("tabla_atrac_utm.xlsx", header=0)

  # Obtener columnas de datos
  data_turist = atrac[ ["FID","JERARQUIA", "NOMBRE", "REGION", "DIRECCION", "COMUNA", "POINT_x", "POINT_y"]]

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
  atrac_data_turist["PRONOSTICOS"] = pronostico =["cielo claro"]

  print(atrac_data_turist)
