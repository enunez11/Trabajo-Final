import streamlit as st
import streamlit.components.v1 as components

# Se configura la página
st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide",
  
)


st.sidebar.write("## Challenge de Visualizaciones")

st.write("### Atractivos turísticos de Chile")

components.html("""
  <iframe width="560" height="315" src="https://www.youtube.com/embed/ZVe80q5gt1Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
""", height=520)
