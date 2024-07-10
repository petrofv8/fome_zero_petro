#Importando as bibliotecas necessárias 
import pandas as pd 
import numpy as np 
import inflection 
import plotly.express as px 
import streamlit as st 
import folium 
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from PIL import Image


st.set_page_config(page_title='Main_page', layout='wide')

#================================================
#Importando o date set 
#================================================

df = pd.read_csv('zomato.csv')
df1 = df.copy()

#================================================
#Funções
#================================================

# Essa função traduz os códigos da coluna country_code para o nome dos países.


COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

#Essa função cria uma nova coluna baseada na coluna price_range.

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    


#Essa função transformma os códigos das cores em string

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

#Essa função renomeia , e limpa os espaços das colunas.


def rename_columns(df1):
    df = df1.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df

#================================================
#Criando as colunas 
#================================================
#Mostrando todas as colunas 
pd.set_option('display.max_columns', 21)
#Chamando função de rename.columns 
df_aux = rename_columns(df1)
#Separando a coluna Cuisines em uma nova coluna
df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
#Criando uma nova coluna com o tipo de comida baseado no preço 
df1["type_food"] = df1.loc[:, "price_range"].apply(lambda x: create_price_tye(","))
#Croiando uma nova coluna baseado no código do país 
df1["country_name"] = df1.loc[:,"country_code"].apply(lambda x: country_name(x))


#================================================
#Barra Lateral
#================================================
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



st.sidebar.markdown('# Países')
#================ Filtros ======================

countries_options = st.sidebar.multiselect(
    'Selecione o país que deseja:',
    df1['country_name'].unique(),
    default =['Brazil','Australia','Canada','Qatar','South Africa']
)
#ligando os filtros ao dataframe
linhas_seleciondas  = df1['country_name'].isin(countries_options)
df1 = df1.loc[linhas_seleciondas, :]   

st.sidebar.markdown('___')
rating_options = st.sidebar.slider(
    'Qual país ?',
    value = df1['aggregate_rating'].mean()
)

linhas_seleciondas2  = df1['aggregate_rating'] <= rating_options
df1 = df1.loc[linhas_seleciondas2, :]   

st.sidebar.markdown('___')
st.sidebar.markdown('##### Powered by CDS')
#--------- iniciando parte lógica do código -------------------
#================================================
#Layout do Streamlit
#================================================


with st.container():
    st.markdown('### Métricas gerais')
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
    #Quantidade de restaurantes cadastrados 
        restaurant_1= df1.loc[:,'restaurant_name'].nunique()
        col1.metric('Restaurantes cadastrados',restaurant_1)
        
    with col2:
        #Quantidade de países cadastrados 
        qnt_countries = df1.loc[:,'country_code'].nunique()
        col2.metric('Países cadastrados',qnt_countries)
    with col3:
        #Quantidade de cidades cadastrads 
        qnt_cities = df1.loc[:,'city'].nunique()
        col3.metric('Cidades cadastradas',qnt_cities)
    with col4:
        #Avaliações feitas na plataforma 
        count = df1['votes'].sum()
        col4.metric('Avaliações feitas',count)
    with col5:
        #tipos de culinárias oferecidas 
        qnt_types = df1['cuisines'].nunique()
        col5.metric('Culinárias cadastradas',qnt_types)

with st.container():
    st.markdown('___')
    st.subheader('Localização dos restaurantes')
    # criando mapa com a localização dos restaurantes 

    df_aux = df1.loc[:,['city','restaurant_name','latitude','longitude']].groupby(['city','restaurant_name']).median().reset_index()

    map = folium.Map()
    cluster = MarkerCluster().add_to(map)

    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['latitude'],
                 location_info['longitude']]).add_to(cluster)

    folium_static(map) # mostrando o map