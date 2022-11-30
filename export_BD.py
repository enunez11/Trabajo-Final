import os

import streamlit as st
import pandas as pd

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from utils import AtracTurist

# Esto solo para hacer referencia a una base de datos SQLlite local:
ruta_mi_bd = os.path.abspath("./cargas.db")
mi_bd = f"sqlite:///{ruta_mi_bd}"

# Crear conexión a BD
# Se quita el parámetro "future=True", por compatibilidad con Pandas 1.x
engine = create_engine(mi_bd)
# Crear sesión a BD
session = Session(engine)

# Consultar por registros
sql_turist = select(AtracTurist)

arch_csv = open("Atractivos.csv","w", encoding="utf-8")
arch_csv.write(sql_turist)

arch_excel = open("Atractivos.xlsx")
arch_excel.write(sql_turist)