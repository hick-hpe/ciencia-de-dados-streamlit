import streamlit as st
import pandas as pd

base = pd.read_csv("https://raw.githubusercontent.com/mvinoba/notebooks-for-binder/master/dados.csv")

st.title('Apartamentos')

bairros = base['bairro'].unique()
bairro = st.selectbox("Bairros", bairros)

apartamentos_bairro = base[base['bairro'] == bairro]
st.dataframe(apartamentos_bairro)
