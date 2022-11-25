import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import streamlit as st
import requests
from dotenv import load_dotenv


# Leer Excel, desde la fila que corresponde
ARCH = pd.read_excel("Tabla_atrac_utm.xlsx", header=0, index_col=0)
print("ARCH: ", ARCH)

# Corregir nombre de la columna de comunas
# el Excel la tiene como "MAIPU", pero debe indicar "COMUNA"
ARCH.rename(columns={"JERARQUIA": "ESCALA", "POINT_X": "PUNTO_X", "POINT_Y": "PUNTO_Y"}, inplace=True)


print("acá se despliega la información: ", ARCH, "Ya mostré el contenido")

ARCH["FECHA DE PROCESO"] = "18-11-2022"
print(ARCH)