import requests
import json
import os
import pandas as pd
import streamlit as st
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

