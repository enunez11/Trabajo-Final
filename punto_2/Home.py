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
  <iframe width="100%" height="520" 
    src="https://www.youtube-nocookie.com/embed/gJSPFlH7UgE?modestbranding=1&controls=0&auto=1"
    title="Visita de Metro de Santiago" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>
""", height=520)
