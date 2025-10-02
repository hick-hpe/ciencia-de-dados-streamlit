import streamlit as st
import pandas as pd

# Carregar dados
base = pd.read_csv("https://raw.githubusercontent.com/mvinoba/notebooks-for-binder/master/dados.csv")

st.title('Apartamentos')

# Filtro por bairros
apto_bairros = base['bairro'].unique()
bairros_selecionados = st.multiselect("Bairros", apto_bairros)

# Aplicar filtro de bairros
aptos_bairro_escolhidos = base[base['bairro'].isin(bairros_selecionados)] if bairros_selecionados else base

# Slider de intervalo de preço
menor_preco = int(base['preco'].min())
maior_preco = int(base['preco'].max())

preco_min, preco_max = st.slider(
    "Selecione o intervalo de preço",
    min_value=menor_preco,
    max_value=maior_preco,
    value=(menor_preco, maior_preco)
)

# Aplicar filtro de preço
aptos_filtrados = aptos_bairro_escolhidos[
    (aptos_bairro_escolhidos['preco'] >= preco_min) &
    (aptos_bairro_escolhidos['preco'] <= preco_max)
]

# Exibir resultados
st.dataframe(aptos_filtrados)
