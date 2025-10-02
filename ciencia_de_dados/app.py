import streamlit as st
import pandas as pd


st.title('Hello World')

nome = st.text_input("Digite algo", "")

st.write(nome or "Seu texto aparecerá aqui")


valores = ['opcao 1', 'opcao 2', 'opcao 3', 'opcao 4']
valor = st.selectbox('Escolha uma opção abaixo', valores)

st.write(valor)

