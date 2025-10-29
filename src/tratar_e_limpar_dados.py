import streamlit as st
import pandas as pd

# base de dados
LINK_BASE = 'base/steam-games.csv'
base = pd.read_csv(LINK_BASE)
print("Colunas disponíveis:", base.columns.tolist())

def tratar_campos():
    global base

    # tratar colunas de preços

    # taxa de conversão - converter de rúpias indianas para reais
    taxa_rupia_brl = 0.060
    
    colunas = [
        'original_price', 'discounted_price'
    ]
    for coluna in colunas:
        base[coluna] = (
            base[coluna]
            .astype("str")
            .str.strip()
            .str.replace('₹', '', regex=False)
            .str.replace(',', '', regex=False)
            .replace(['nan', 'None', 'Free', ''], '0', regex=False)
            .astype(float) * taxa_rupia_brl
        )
    
    # tratar colunas de textos
    base['content_descriptor'] = base['content_descriptor'].astype(str).str.strip()
    base['content_descriptor'] = base['content_descriptor'].replace('nan', 'Sem descrição')

    # tratar coluna de desconto
    base['discount_percentage'] = base['discount_percentage'].fillna('0%')
    base['discount_percentage'] = base['discount_percentage'].astype(str).str.strip()
    base['discount_percentage'] = base['discount_percentage'].replace(['', 'None'], '0%')
    base['discount_percentage'] = base['discount_percentage'].str.replace('%', '', regex=False).astype(float).abs()
    print('list_discount: ', base['discount_percentage'])

    # tratar colunas de avaliações
    base['recent_review_count'] = pd.to_numeric(base['recent_review_count'], errors='coerce').fillna(0).astype(int)
    base['recent_review_%'] = pd.to_numeric(base['recent_review_%'], errors='coerce').fillna(0)
    base['recent_review'] = base['recent_review'].fillna('Sem review')

    # tratar coluna de data
    base['release_date'] = pd.to_datetime(base['release_date'], errors='coerce')
    base['release_date'] = base['release_date'].dt.strftime('%d/%m/%Y')

def tratar_base(): 
    global base

    # info basicas e tratar/limpar dados duplicados
    base = base.drop_duplicates()

    print(f"BASE: {base.shape}")

    # calcular nulos absolutos e percentuais
    nulos_abs = base.isna().sum()
    nulos_pct = (base.isna().mean() * 100).round(2)

    # juntar tudo em um DataFrame
    diagnostico = pd.DataFrame({
        'Valores Nulos': nulos_abs,
        '% Nulos': nulos_pct,
        'Valores Preenchidos': base.shape[0] - nulos_abs,
        '% Preenchidos': (100 - nulos_pct).round(2)
    })

    # exibir no terminal
    print("\n===== Diagnóstico de Valores Nulos =====")
    print(diagnostico.sort_values('% Nulos', ascending=False))
    
def get_base_tratada():
    tratar_base()
    tratar_campos()
    return base

