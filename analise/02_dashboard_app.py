import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard - Tema Integrador VII (UNIG)", layout="wide")

st.title("📊 Panorama Regional: Segurança Digital, Tecnologias e ODS")
st.markdown("**Curso:** Bacharelado em Ciência da Computação (UNIG) | **Disciplina:** Tema Integrador VII")

@st.cache_data
def load_data():
    return pd.read_csv("../dados/dados_tratados.csv")

try:
    df = load_data()

    # Filtro Lateral por Faixa Etária (Q2)
    st.sidebar.header("🔍 Filtros da Pesquisa")
    if "faixa_etaria" in df.columns:
        opcoes_idade = df["faixa_etaria"].dropna().unique().tolist()
        selecao_idade = st.sidebar.multiselect("Faixa Etária:", options=opcoes_idade, default=opcoes_idade)
        df = df[df["faixa_etaria"].isin(selecao_idade)]

    # KPIs no Topo (Médias de 1 a 5)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Participantes (N)", len(df))
    if "interesse_ia" in df.columns:
        c2.metric("Interesse em IA (1-5)", f"{df['interesse_ia'].mean():.2f}")
    if "conhecimento_lgpd" in df.columns:
        c3.metric("Conhecimento LGPD (1-5)", f"{df['conhecimento_lgpd'].mean():.2f}")
    if "relevancia_ti_ods" in df.columns:
        c4.metric("Impacto da TI nos ODS (1-5)", f"{df['relevancia_ti_ods'].mean():.2f}")

    st.divider()

    # Linha 1 de Gráficos
    col_esq, col_dir = st.columns(2)
    with col_esq:
        st.subheader("🚧 Barreiras Tecnológicas na Região (Q4)")
        if "barreiras_tec" in df.columns:
            barreiras = df["barreiras_tec"].dropna().str.split(r",\s*(?=[A-Z])|;").explode().str.strip()
            st.bar_chart(barreiras.value_counts())

    with col_dir:
        st.subheader("🔐 Médias de Segurança Digital e Nuvem (1 a 5)")
        cols_seg = ["frequencia_2fa", "higiene_senhas", "conhecimento_lgpd", "uso_nuvem"]
        existentes = [c for c in cols_seg if c in df.columns]
        if existentes:
            medias_seg = df[existentes].mean().rename({
                "frequencia_2fa": "Uso de 2FA",
                "higiene_senhas": "Higiene de Senhas",
                "conhecimento_lgpd": "Direitos LGPD",
                "uso_nuvem": "Serviços em Nuvem"
            })
            st.bar_chart(medias_seg)

    st.divider()

    # Linha 2: ODS Prioritários e Respostas Abertas
    col_ods, col_aberta = st.columns(2)
    with col_ods:
        st.subheader("🌍 Metas ODS Prioritárias para o Município (Q10)")
        if "ods_prioritarios" in df.columns:
            ods = df["ods_prioritarios"].dropna().str.split(r",\s*(?=ODS)|;").explode().str.strip()
            st.bar_chart(ods.value_counts())

    with col_aberta:
        st.subheader("💬 Relatos da Comunidade (Questão 11)")
        if "problema_realidade" in df.columns:
            respostas = df[["faixa_etaria", "problema_realidade"]].dropna()
            st.dataframe(respostas, use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.info("Aguardando exportação do arquivo `dados/dados_tratados.csv` para carregar os gráficos.")