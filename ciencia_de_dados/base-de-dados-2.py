import streamlit as st
import pandas as pd

base = pd.read_csv("https://raw.githubusercontent.com/mvinoba/notebooks-for-binder/master/dados.csv")

st.title('Apartamentos')

apto_bairros = base['bairro'].unique()
bairros_selecionados = st.multiselect("Bairros", apto_bairros)

aptos_bairro_escolhidos = base[base['bairro'].isin(bairros_selecionados)]
st.dataframe(aptos_bairro_escolhidos)
