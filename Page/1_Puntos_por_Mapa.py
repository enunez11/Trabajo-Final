import streamlit as st

import pydeck as pdk
import numpy as np

# Se importan funcionalidades desde librería propia
from utils import tur_data

# Obtener datos desde cache
data_puntos = tur_data()

# Generar listado de horarios ordenados
atractivos_puntos = data_puntos["NOMBRE"].sort_values().unique()

# Generar listado de comunas ordenadas
region_puntos = data_puntos["REGION"].sort_values().unique()

with st.sidebar:
  st.write("##### Filtros de Información")
  st.write("---")

  # Multiselector de comunas
  region_sel = st.multiselect(
    label="Regiones con Atractivos",
    options=region_puntos,
    default=[]
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not region_sel:
    region_sel = region_puntos.tolist()

  # Multiselector de horarios
  atractivo_sel = st.multiselect(
    label="Atractivos Turísticos",
    options=atractivos_puntos,
    default=atractivos_puntos
  )
  # Se establece la lista completa en caso de no seleccionar ninguna
  if not atractivo_sel:
    atractivo_sel = atractivos_puntos.tolist()



# Aplicar Filtros
atrac_data = data_puntos.query(" Atractivos==@atractivo_sel and Region==@region_sel")

if atrac_data.empty:
  # Advertir al usuario que no hay datos para los filtros
  st.warning("#### No hay registros para los filtros usados!!!")
else:
  # Desplegar Mapa
  # Obtener el punto promedio entre todas las georeferencias
  avg_x = np.median(atrac_data["PUNTO_X"])
  avg_y = np.median(atrac_data["PUNTO_Y"])

  puntos_mapa = pdk.Deck(
      map_style=None,
      initial_view_state=pdk.ViewState(
          latitude=avg_x,
          longitude=avg_y,
          zoom=10,
          min_zoom=10,
          max_zoom=15,
          pitch=20,
      ),
      layers=[
        pdk.Layer(
          "ScatterplotLayer",
          data=atrac_data,
          pickable=True,
          auto_highlight=True,
          get_position='[PUNTO_X, PUNTO_Y]',
          filled=True,
          opacity=0.6,
          radius_scale=10,
          radius_min_pixels=3,
          get_fill_color=["NOMBRE", 90, 200]
        )      
      ],
      tooltip={
        "html": "<b>Nombre: </b> {NOMBRE} <br /> "
                "<b>Dirección: </b> {DIRECCION} <br /> "
                "<b>Comuna: </b> {COMUNA} <br /> "
                "<b>Región: </b> {REGION} <br /> "
                "<b>Tipo: </b> {TIPO} <br /> "
                "<b>Georeferencia (Lat, Lng): </b>[{PUNTO_X}, {PUNTO_Y}] <br /> ",
        "style": {
          "backgroundColor": "steelblue",
          "color": "white"
        }
      }
  )

  st.write(puntos_mapa)

