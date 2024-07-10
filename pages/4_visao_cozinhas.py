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

def cozinhas(df, pais_cozinha):
    ''' Esta função traz os dados do restaurante com maior média de avaliação da culinária especificada
        
        Caso haja mais de um restaurante com a maior média de avaliação o selecionado será aquele com menor ID

        Input:
            - df - dataframe contendo os dados necessários
            - pais_cozinha - especifica qual o tipo de culinária do restaurante

        Output:
            - dados do restaurante com maior média de avaliação
                - nome
                - nota de avaliação
                - país
                - cidade
                - prato_pra_dois - custo do prato para duas pessoas
                - moeda - moeda local
    '''
    df_coz = (df.loc[df['cuisines'] == pais_cozinha, ['restaurant_id', 'restaurant_name', 'aggregate_rating', 'country_name', 'city', 'average_cost_for_two', 'currency']].
                  sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).
                  reset_index(drop=True))
    nome = df_coz.loc[0, 'restaurant_name']
    nota = df_coz.loc[0, 'aggregate_rating']
    pais = df_coz.loc[0, 'country_name']
    cidade = df_coz.loc[0, 'city']
    prato_para_dois = df_coz.loc[0, 'average_cost_for_two']
    moeda = df_coz.loc[0, 'currency']
    
    dados = [nome, nota, pais, cidade, prato_para_dois, moeda]
    
    return dados
def rank_culinarias(df, asc):
    ''' Esta função desenha o gráfico das 10 culinárias com maiores e menores notas médias de avaliação
        
        Ações realizadas:
            - Faz o cálculo das médias e monta o dataframe auxiliar para a construção do gráfico
            - Faz a configuração do gráfico
            - Faz a configuração do título do gráfico
        
        Input:
            - df - dataframe
            - asc - especifica se o gráfico é para as culinárias com maiores ou com menores notas
                - True - para o gráfico com a culinárias com menores notas
                - False - para o gráfico com a culinárias com maiores notas
        
        Output:
            - fig - figura do gráfico para ser exibido           
    
    '''
    df_aux = df.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=asc).reset_index().round(2)

    fig = px.bar(df_aux.iloc[0:10], 
                 x='cuisines', 
                 y='aggregate_rating', 
                 text='aggregate_rating', 
                 labels={'cuisines':'Tipo de Culinária', 
                         'aggregate_rating':'Média da Avaliação Média'})

    if asc == True:
        text = 'Menores'
    else:
        text = 'Maiores'
    
    fig.update_layout(title={'text': f'Top 10 Culinárias com {text} médias de avaliação', 
                             'y':0.95, 
                             'x': 0.5 , 
                             'xanchor': 'center', 
                             'yanchor': 'top'})
    
    return fig


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

st.set_page_config(page_title='visao_cozinhas.py', layout='wide')

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

#Filtro de quantidade de restaurantes 
st.sidebar.markdown('___')
rating_options = st.sidebar.slider(
    'Selecione a quantidade de restaurantes que deseja visualizar:',
    min_value = 0, 
    max_value = 30, 
    value = 10,
    step = 1 
)

# Filtro tipo de culinárias 
#separando os tipos de culinárias 
cuisines_ordem = df1['cuisines'].unique()

#criando o filtro 
culinarias = st.sidebar.multiselect(
    'Selecione o tipo de culinárias',
        options = cuisines_ordem,
        default=[ 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian']
)

df3 = df1.loc[df1['cuisines'].isin(culinarias), :] # altera tabela


#================================================
#------------------ Início da estrutura lógica do código --------------------

with st.container():
    st.markdown('## Melhores Restaurantes das Principais Culinárias')
    col1, col2,col3,col4,col5 = st.columns(5)
    with col1:
        dados = cozinhas(df1, 'Brazilian')
                    
        st.metric(f'Brazilian: {dados[0]}', 
                value=f'{dados[1]}/5.0', 
                help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                            ''')
    
    with col2:
        dados = cozinhas(df1, 'Italian')
                
        st.metric(f'Italian: {dados[0]}', 
                value=f'{dados[1]}/5.0', 
                help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                            ''')
 
    with col3:
        dados = cozinhas(df1, 'American')
                
        st.metric(f'American: {dados[0]}', 
                value=f'{dados[1]}/5.0', 
                help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                            ''')
    
    with col4:
        dados = cozinhas(df1, 'Japanese')
                
        st.metric(f'Japanese: {dados[0]}', 
                  value=f'{dados[1]}/5.0', 
                  help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                        ''')

    with col5:
        dados = cozinhas(df1, 'Arabian')
                
        st.metric(f'Arabian: {dados[0]}', 
                  value=f'{dados[1]}/5.0', 
                  help=f'''
                            País: {dados[2]} \n
                            Cidade: {dados[3]} \n
                            Prato para dois: {dados[4]} {dados[5]}
                        ''')
st.divider()

with st.container():

    st.markdown(f'## Top {rating_options} Restaurantes')
    
    st.dataframe(df3.loc[:, ['restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two',  'aggregate_rating', 'votes']].
                 sort_values(['aggregate_rating', 'restaurant_name'], ascending=[False, True])[0:rating_options], 
                 use_container_width=True, 
                 hide_index=True, 
                 column_config={'restaurant_name':None,
                                 'restaurant_name': st.column_config.TextColumn('Nome do Restaurante'), 
                                 'country': 'País', 
                                 'city': 'Cidade' , 
                                 'cuisines':'Culinária', 
                                 'average_cost_for_two':st.column_config.NumberColumn('Prato para dois', 
                                                                                      width='small', 
                                                                                      help='Preço médio do prato para duas pessoas na moedas locais dos países'), 
                                
                                                                                             'aggregate_rating': 'Nota Média', 
                                                                                             'votes': 'Avaliações'})
    

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = rank_culinarias(df1, False)
        st.plotly_chart(fig)

    with col2:
        fig = rank_culinarias(df1, True)
        st.plotly_chart(fig) 

        