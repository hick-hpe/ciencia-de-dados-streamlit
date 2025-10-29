import streamlit as st
import pandas as pd
from tratar_e_limpar_dados import get_base_tratada

# carregar base tratada
base = get_base_tratada()

# configurar página
st.set_page_config(page_title="Steam Games Dashboard", layout="wide")
st.title("Steam Games Data Dashboard")
st.write(f'Esta base de dados é referente à plataforma **Steam**, uma das maiores lojas digitais de jogos para PC. Ela contém informações detalhadas sobre os jogos disponíveis, incluindo título, data de lançamento, gênero, desenvolvedor, preço, avaliações, suporte a sistemas operacionais e muito mais.')


# ================================================ VISÃO GERAL ================================================
st.header("Visão Geral dos Jogos")

# ------------------------- gráfico dos 5 jogos mais populares -------------------------
st.subheader("Top 5 jogos mais populares da steam")
top5_jogos = base.nlargest(5, 'overall_review_count')
st.bar_chart(top5_jogos.set_index('title')['overall_review_count'])


# ------------------------- quais são os gêneros mais comuns na Steam? -------------------------
st.subheader('Gêneros mais comuns na Steam')

# garantir que seja string e "explodir"
base['genres'] = base['genres'].astype(str)
generos_explode = base['genres'].str.split(',').explode().str.strip()

# contar os mais comuns
top5_generos = generos_explode.value_counts().head(5)

# exibir gráfico
st.bar_chart(top5_generos)


# ------------------------- quais publishers publicam mais jogos? -------------------------
st.subheader('Quais publishers publicam mais jogos?')
top5_publisher = base['publisher'].value_counts().head(5)
st.bar_chart(top5_publisher)


# ------------------------- quais categorias (ex: "Multiplayer", "Single Player") são mais populares? -------------------------
st.subheader('Quais categorias (ex: "Multiplayer", "Single Player") são mais populares?')
base['categories'] = base['categories'].astype(str)
categorias_explode = base['categories'].str.split(',').explode().str.strip()

# contar os mais comuns
top5_categorias = categorias_explode.value_counts().head(5)

# exibir gráfico
st.bar_chart(top5_categorias)

# -------------- jogos com maiores descontos (`discount_percentage`) têm melhores avaliações (`overall_review_%`)?---------------
# st.subheader("Relação entre desconto e avaliações gerais")

# # garantir que as colunas estejam no tipo numérico
# base['discount_percentage'] = pd.to_numeric(base['discount_percentage'], errors='coerce')
# base['overall_review_%'] = pd.to_numeric(base['overall_review_%'], errors='coerce')

# # remover linhas nulas
# base_limp = base.dropna(subset=['discount_percentage', 'overall_review_%'])

# # calcular correlação
# correlacao = base_limp['discount_percentage'].corr(base_limp['overall_review_%'])

# # exibir resultado numérico
# st.metric("Correlação entre desconto e avaliação geral", f"{correlacao:.2f}")

# # exibir gráfico de dispersão
# st.scatter_chart(base_limp[['discount_percentage', 'overall_review_%']])

# # interpretação automática
# if correlacao > 0.5:
#     interpretacao = "Jogos com maiores descontos tendem a ter **melhores avaliações**."
# elif correlacao < -0.5:
#     interpretacao = "Jogos com maiores descontos tendem a ter **piores avaliações**."
# else:
#     interpretacao = "Não há relação significativa entre descontos e avaliações."

# st.write(interpretacao)

# --------------------------------------- jogos com DLCs tendem a ser mais caros? ---------------------------------------


# --------------------- quais gêneros estão crescendo ou diminuindo em lançamentos? ---------------------
st.subheader("Quais gêneros estão crescendo ou diminuindo em lançamentos?")
base['release_date'] = pd.to_datetime(base['release_date'], errors='coerce')
base['ano_lancamento'] = base['release_date'].dt.year

# remover nulos
df_lancamentos = base.dropna(subset=['ano_lancamento'])

# explode genres
df_lancamentos['genres'] = df_lancamentos['genres'].astype(str)
generos_explode = df_lancamentos.assign(genres=df_lancamentos['genres'].str.split(',')).explode('genres')
generos_explode['genres'] = generos_explode['genres'].str.strip()

# contar lançamentos por gênero e ano
lancamentos_por_ano = generos_explode.groupby(['ano_lancamento', 'genres']).size().unstack(fill_value=0)

# calcular top 5 gêneros recentes
ultimo_ano = int(df_lancamentos['ano_lancamento'].max())
anos_recentes = [ultimo_ano, ultimo_ano-1, ultimo_ano-2]
recentes = generos_explode[generos_explode['ano_lancamento'].isin(anos_recentes)]
top5 = recentes['genres'].value_counts().nlargest(5)

# filtrar apenas os top5 gêneros para o gráfico
lancamentos_top5 = lancamentos_por_ano[top5.index]

st.write("Evolução dos lançamentos desses gêneros ao longo dos anos:")
st.line_chart(lancamentos_top5)

st.dataframe(top5)


# --------------------- desenvolvedores com mais jogos publicados tendem a manter qualidade constante? ---------------------
st.subheader("Desenvolvedores com mais jogos publicados e avaliação média")

# contar jogos por developer
dev_counts = base['developer'].value_counts()

# pegar top 5 desenvolvedores
top5_devs = dev_counts.nlargest(5).index

# calcular média de avaliação para esses devs
media_avaliacao = base.groupby('developer')['overall_review_%'].mean().loc[top5_devs]

# criar DataFrame para exibir
df_dev = pd.DataFrame({
    'Jogos Publicados': dev_counts.loc[top5_devs],
    'Avaliação Média (%)': media_avaliacao
})

# exibir tabela
st.write("Top 5 desenvolvedores por número de jogos")
st.dataframe(df_dev)

# gráfico de barras para Avaliação Média
st.bar_chart(df_dev['Avaliação Média (%)'])


# --------------------- os jogos lançados recentemente têm mais ou menos descontos? ---------------------
st.subheader("Jogos lançados recentemente têm mais ou menos descontos?")

# garantir que release_date seja datetime
base['release_date'] = pd.to_datetime(base['release_date'], errors='coerce')

# filtrar dados válidos
df_desconto = base[['title', 'release_date', 'discount_percentage']].dropna()

# criar coluna de ano de lançamento
df_desconto['ano_lancamento'] = df_desconto['release_date'].dt.year

# agrupar por ano: mínimo, médio e máximo
desconto_ano = df_desconto.groupby('ano_lancamento')['discount_percentage'].mean()

# exibir tabela
st.write("Desconto por ano de lançamento (mínimo, médio e máximo)")
st.dataframe(desconto_ano)

# gráfico interativo com Streamlit
st.line_chart(desconto_ano)

st.write(
    "Observação: De 1997 a 2005, os jogos não apresentavam descontos registrados. "
    "A partir de 2006, surgem descontos médios entre 3% e 8%, com leve variação ao longo dos anos. "
    "Os lançamentos mais recentes não apresentam descontos significativamente maiores que os mais antigos, "
    "indicando que a média de desconto se mantém relativamente estável ao longo do tempo."
)


# ================================================ FILTROS ================================================
st.header("Fitro dos Jogos")

# escolher colunas para exibir
colunas = ['title', 'content_descriptor', 'genres', 'release_date', 'original_price', 'discounted_price', 'discount_percentage', 'overall_review_%', 'overall_review_count']
base_exibir = base[colunas]

# filtro de jogos
nomes_jogos = base['title'].unique()
jogos_selecionados = st.multiselect("Escolha os jogos", nomes_jogos)

# filtrar base
if jogos_selecionados:
    jogos_filtrados = base_exibir[base_exibir['title'].isin(jogos_selecionados)]
else:
    jogos_filtrados = base_exibir

# --------------------- filtro de faixa de preços ---------------------
# pegar mínimo e máximo da base
preco_min_df, preco_max_df = int(base['original_price'].min()), 5000
print(f'Faixa de preço (R$): {(preco_min_df, preco_max_df)}')

# slider com limites baseados nos dados
preco_min, preco_max = st.slider(
    "Faixa de preço (R$)",
    min_value=preco_min_df,
    max_value=preco_max_df,
    value=(preco_min_df, preco_max_df)
)

# filtrar jogos pela faixa de preço
jogos_filtrados = jogos_filtrados[
    (jogos_filtrados['original_price'] >= preco_min) & 
    (jogos_filtrados['original_price'] <= preco_max)
]

# exibir quantidade de jogos encontrados
num_jogos_encontrados = jogos_filtrados.shape[0]
st.write(f'Jogos encontrados nessa faixa de preço: {num_jogos_encontrados}')

# filtro por avaliação geral
avaliacao_min = st.slider("Avaliação mínima (%)", 0, 100, 50)
jogos_filtrados = jogos_filtrados[jogos_filtrados['overall_review_%'] >= avaliacao_min]

# filtro por gênero ou categoria
generos = base['genres'].str.split(',').explode().str.strip().unique()
generos_selecionados = st.multiselect("Filtrar por gênero", generos)

if generos_selecionados:
    jogos_filtrados = jogos_filtrados[jogos_filtrados['genres'].str.contains('|'.join(generos_selecionados))]

# filtro por conteúdo (idade, descriptor)
conteudos = base['content_descriptor'].unique()
conteudo_selecionado = st.multiselect("Filtrar por conteúdo", conteudos)

if conteudo_selecionado:
    jogos_filtrados = jogos_filtrados[jogos_filtrados['content_descriptor'].isin(conteudo_selecionado)]

# filtro por ano de lançamento
# garantir que release_date seja datetime
base['release_date'] = pd.to_datetime(base['release_date'], errors='coerce')

# extrair o ano
base['ano_lancamento'] = base['release_date'].dt.year

# agora você pode usar o slider
ano_min, ano_max = st.slider(
    "Ano de lançamento",
    int(base['ano_lancamento'].min()),
    int(base['ano_lancamento'].max()),
    (2010, 2025)
)

# filtrar
jogos_filtrados = jogos_filtrados[
    jogos_filtrados['release_date'].dt.year.between(ano_min, ano_max)
]

# exibir tabela
st.dataframe(jogos_filtrados)
