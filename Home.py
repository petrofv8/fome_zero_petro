import streamlit as st 
from PIL import Image
import inflection



st.set_page_config(
    page_title ='Home',
    page_icon='📊',
)
st.header('Fome Zero!')
st.markdown('### Seu novo restaraunte é aqui !')
st.markdown('___')

image_path ='logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width = 160)

st.sidebar.markdown('___')

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## A solução dos seus problemas')
st.sidebar.markdown('___')

st.write(
    """
    ## Fome Zero  Dashboard
    ### Nesta página é apresentado um dashboard com os dados analisados pela equipe de dados Fome Zero.
    - Visão Main page :
        - Aqui é apresentado a visão geral com as métricas gerais e a localização dos restaurantes
    
    - Visão países :
        - Aqui é apresentado a visão por países onde temos métricas da distrubuição dos restaurantes por países , cidade 
    e a média do valor para um prato para dois.
    
    - Visão cidades:
        -Aqui são apresentadas gráficos com as top 10 cidades com mais restaurantes e as médias das cidades, bem como
     as cidades que mais tem tipos de culinárias variados.
    
    - Visão cozinhas:
        -Aqui são apresentadas métricas com as médias dos tipos de culinárias, os top 10 restauurantes por tipo de culinária e
     e os gráficos com as médias das top 10 melhores e piores médias de avaliação dos tipos de culinárias.
     
     ## Ask for help 
     - Time date science no discord 
       @petro05560
     """
    
) 
