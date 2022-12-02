import streamlit as st

import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt

# Se importan funcionalidades desde librería propia
from utils import geo_data

# Obtener datos desde cache
data_puntos = geo_data()

# Generar listado de horarios ordenados
horarios_puntos = data_puntos["Horario"].sort_values().unique()

# Generar listado de comunas ordenadas
comunas_puntos = data_puntos["Comuna"].sort_values().unique()

with st.sidebar:
  st.write("##### Filtros de Información")
  st.write("---")

  # Multiselector de comunas
  comuna_sel = st.multiselect(
    label="Comunas en Funcionamiento",
    options=comunas_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not comuna_sel:
    comuna_sel = comunas_puntos.tolist()

  # Multiselector de horarios
  hora_sel = st.multiselect(
    label="Horario de Funcionamiento",
    options=horarios_puntos,
    default=horarios_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not hora_sel:
    hora_sel = horarios_puntos.tolist()


col_bar, col_pie, col_line = st.columns(3, gap="small")

group_comuna = data_puntos.groupby(["Horario"]).size()
# Se ordenan de mayor a menor, gracias al uso del parámetros "ascending=False"
group_comuna.sort_values(axis="index", ascending=False, inplace=True)

def formato_porciento(dato: float):
  return f"{round(dato, ndigits=2)}%"


with col_bar:
  bar = plt.figure()
  group_comuna.plot.bar(
    title="Cantidad de Puntos de Carga por Horario",
    label="Total de Puntos",
    xlabel="Horarios",
    ylabel="Puntos de Carga",
    color="lightblue",
    grid=True,
  ).plot()
  st.pyplot(bar)

with col_pie:
  pie = plt.figure()
  group_comuna.plot.pie(
    y="index",
    title="Cantidad de Puntos de Carga por Horario",
    legend=None,
    autopct=formato_porciento
  ).plot()
  st.pyplot(pie)

with col_line:
  line = plt.figure()
  group_comuna.plot.line(
    title="Cantidad de Puntos de Carga por Horario",
    label="Total de Puntos",
    xlabel="Horarios",
    ylabel="Puntos de Carga",
    color="lightblue",
    grid=True
  ).plot()
  st.pyplot(line)

# Aplicar Filtros
geo_data = data_puntos.query(" Horario==@hora_sel and Comuna==@comuna_sel ")

if geo_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_lat = np.median(geo_data["LATITUD"])
  avg_lng = np.median(geo_data["LONGITUD"])

  puntos_mapa = pdk.Deck(
      map_style=None,
      initial_view_state=pdk.ViewState(
          latitude=avg_lat,
          longitude=avg_lng,
          zoom=10,
          min_zoom=10,
          max_zoom=15,
          pitch=20,
      ),
      layers=[
        pdk.Layer(
          "HeatmapLayer",
          data=geo_data,
          pickable=True,
          auto_highlight=True,
          get_position='[LONGITUD, LATITUD]',
          opacity=0.6,
          get_weight="Horario == '10:00 - 14:00' ? 255 : 10"
        )      
      ],
      tooltip={
        "html": "<b>Negocio: </b> {Negocio} <br /> "
                "<b>Dirección: </b> {Dirección} <br /> "
                "<b>Comuna: </b> {Comuna} <br /> "
                "<b>Horario: </b> {Horario} <br /> "
                "<b>Código: </b> {CODIGO} <br /> "
                "<b>Georeferencia (Lat, Lng): </b>[{LATITUD}, {LONGITUD}] <br /> ",
        "style": {
          "backgroundColor": "steelblue",
          "color": "white"
        }
      }
  )

  st.write(puntos_mapa)

