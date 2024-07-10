#Importando as bibliotecas necessárias 
import pandas as pd 
import numpy as np 
import inflection 
import plotly.express as px 
import streamlit as st 
from PIL import Image




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

def conv_moedas(df):
    ''' Esta função faz o câmbio das moedas locais de cada país para valores em Reais (BRL)
    '''
    cambio = {'currency': ['Botswana Pula(P)', 
                           'Brazilian Real(R$)', 
                           'Dollar($)', 
                           'Emirati Diram(AED)', 
                           'Indian Rupees(Rs.)', 
                           'Indonesian Rupiah(IDR)', 
                           'NewZealand($)', 
                           'Pounds(£)',
                           'Qatari Rial(QR)', 
                           'Rand(R)', 
                           'Sri Lankan Rupee(LKR)',
                           'Turkish Lira(TL)'], 
                'taxa_cambio':[0.3995, 1, 5.4283, 1.4777, 0.06504, 0.0003314, 3.3167, 6.8793, 1.4886, 0.2977, 0.01778, 0.1648]}
    cambio = pd.DataFrame(cambio)
    df_conv = df.merge(cambio, on='currency')
    df_conv['average_cost_for_two_brl'] = df_conv['average_cost_for_two']*df_conv['taxa_cambio']
    
    return df_conv

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

st.set_page_config(page_title='visao_Main_page', layout='wide')

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

st.title('Visão Cidades')
st.divider()

with st.container():
    df_aux = df1.loc[:, ['restaurant_name', 'city', 'country_name']].groupby(['city','country_name']).count().sort_values('restaurant_name', ascending=False).reset_index()
    fig = px.bar(df_aux.iloc[0:10], 
                 x='city', 
                 y='restaurant_name', 
                 text='restaurant_name', 
                 labels={'city':'Cidade', 
                         'restaurant_name':'Quantidade de Restaurantes', 
                         'country_name': 'País'}, 
                 color='country_name')
    
    fig.update_layout(title={'text': 'Top 10 Cidades com mais Restaurantes registrados', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    st.plotly_chart(fig)


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        df_aux = df1.loc[df1['aggregate_rating'] >= 4 , ['restaurant_name', 'city', 'country_name']].groupby(['city', 'country_name']).count().sort_values('restaurant_name', ascending=False).reset_index()
        fig = px.bar(df_aux.iloc[0:7], 
                     x='city', 
                     y='restaurant_name', 
                     text='restaurant_name', 
                     labels={'city': 'Cidade', 
                             'restaurant_name':'Quantidade de Restaurantes', 
                             'country_name':'País'}, 
                     color='country_name')
        
        fig.update_layout(title={'text': 'Top 7 Cidades com Restaurantes com Média de Avaliação acima de 4', 
                                 'y':0.95, 
                                 'x': 0.5 , 
                                 'xanchor': 'center', 
                                 'yanchor': 'top'})
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_aux = df1.loc[df1['aggregate_rating'] >= 2.5, ['restaurant_name', 'city', 'country_name']].groupby(['city', 'country_name']).count().sort_values('restaurant_name', ascending=False).reset_index()
        fig = px.bar(df_aux.iloc[0:10], 
                     x='city', 
                     y='restaurant_name', 
                     text='restaurant_name', 
                     labels={'city':'Cidade', 
                             'restaurant_name':'Quantidade de Restaurantes', 
                             'country_name':'País'}, 
                     color='country_name')
        
        fig.update_layout(title={'text': 'Top 10 Cidades com Restaurantes com Média de Avaliação acima de 2.5', 
                                 'y':0.95, 
                                 'x': 0.5 , 
                                 'xanchor': 'center', 
                                 'yanchor': 'top'})
        
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    df_aux = df1.loc[:, ['cuisines', 'city', 'country_name']].groupby(['city', 'country_name']).nunique().sort_values('cuisines', ascending=False).reset_index()
    fig = px.bar(df_aux.iloc[0:5], 
                 x='city', 
                 y='cuisines', 
                 text='cuisines', 
                 labels={'city':'Cidades', 
                         'cuisines':'Quantidade de Tipos Culinários Únicos', 
                         'country':'País'}, 
                 color='country_name')
    
    fig.update_layout(title={'text': 'Top 5 Cidades com mais Restaurantes com tipos de Cullinárias diferentes', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    st.plotly_chart(fig)