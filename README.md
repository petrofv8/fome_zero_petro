# 1- Problema de negócio

O problema de negócio simula uma contratação de um novo cientista de dados junior em uma empresa fictícia .

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

## Análise dos países

- Quantidade de restaurantes registrados por país
- Quantidade de cidades registradas por país
- Média de avaliações feitas por país
- Custo do preço do prato para dois por país .

## Análise das cidades

- Top 10 cidades com mais restaurantes registrados
- top 7 cidades com restaurantes com média de avaliação acima de 4
- Top 10 cidades com restaurantes com média de avaliação acima de 2,5
- Top 55 cidades com mais restaurantes com tipos de culinárias diferentes.

## Análise culinárias

- Os 5 tipos de culinárias com médias de avaliações mais altas
- os top 10 restaurantes
- Culinárias com maior e menor média de avaliação.

O objetivo é criar um dashboard com conjunto de métricas, gráficos e tabelas para facilitar ao CEO  uma melhor visualização dos dados.

# 2- Premissas do negócio

- Análise foi feita com dados extraídos do site Kaggle, em um dataset auto atualizado chamado Zomato.
- Marketplace foi o modelo de negócio assumido
- As três principais visões foram : Países, cidades e cozinhas.

# 3- Estratégia da solução

O painel estratégico foi desenvolvido utilizando métricas que refletem as 3 principais visões do modelo de negócio da empresa:

1. Visão da quantidade de restaurantes por país 
2. Visões do desenvolvimento dos restaurantes por cada cidade 
3. visão do potencial dos tipos de culinárias baseado em cada país e cidade.

Dentro das visões de negócio essa foram as métricas pra cada tipo:

## Análise dos países

- Quantidade de restaurantes registrados por país
- Quantidade de cidades registradas por país
- Média de avaliações feitas por país
- Custo do preço do prato para dois por país .

## Análise das cidades

- Top 10 cidades com mais restaurantes registrados
- top 7 cidades com restaurantes com média de avaliação acima de 4
- Top 10 cidades com restaurantes com média de avaliação acima de 2,5
- Top 55 cidades com mais restaurantes com tipos de culinárias diferentes.

## Análise culinárias

- Os 5 tipos de culinárias com médias de avaliações mais altas
- os top 10 restaurantes
- Culinárias com maior e menor média de avaliação.

O objetivo é criar um dashboard com conjunto de métricas, gráficos e tabelas para facilitar ao CEO  uma melhor visualização dos dados.

# 4- Top 4 insights de dados

1. A região da índia é a que mais tem restaurantes cadastrados dentro do sistema.
2. A indonésia é que possui o maior valor médio para prato para dois.
3. Brasília, Birmingham e Manchester são as cidades que mais possuem tipos de culinárias diferentes.
4. Others é tipo de culinária que tem a maior média de avalição 

# 5-O produto final do projeto

Painel online, hospedado em um Cloud e disponível para  qualquer dispositivo com acesso a internet.

O painel pode ser acessado pelo link :

https://fomezeropetro.streamlit.app/

# 6- Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e tabelas que mostrem as métricas da melhor forma possível para o CEO 

Da visão de países e cidades podemos concluir que a Índia é o país que mais possuem restaurantes cadastrados no sistema, porém a cidade de Brasília no Brasil é a que possuem os restaurantes com a melhor média de avaliação.

# 7- Próximos passos

- Criar mais visões de négócio
- Criar um filtro que separa por valor médio do prato para dois
- Criar mais gráficos para melhor visualização do dados.
