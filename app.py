import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard de Vendas de Supermercado")

# Upload do arquivo pelo usuário
uploaded_file = st.sidebar.file_uploader(
    "Escolha o arquivo de vendas (CSV ou Excel)", 
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # Detecta o tipo de arquivo e lê
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, sep=";", decimal=",")
    else:
        df = pd.read_excel(uploaded_file)
    
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    month = st.sidebar.selectbox("Mês", df["Month"].unique())
    df_filtered = df[df["Month"] == month]

    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)

    fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
    col1.plotly_chart(fig_date, use_container_width=True)

    fig_prod = px.bar(df_filtered, x="Product line", y="Total",
                      color="City", title="Faturamento por tipo de produto",
                      barmode="group")
    col2.plotly_chart(fig_prod, use_container_width=True)

    city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
    fig_city = px.bar(city_total, x="City", y="Total",
                      title="Faturamento por filial")
    col3.plotly_chart(fig_city, use_container_width=True)

    fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                      title="Faturamento por tipo de pagamento")
    col4.plotly_chart(fig_kind, use_container_width=True)

    city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
    fig_rating = px.bar(city_rating, x="City", y="Rating",
                        title="Avaliação média por cidade")
    col5.plotly_chart(fig_rating, use_container_width=True)
else:
    st.info("Faça upload de um arquivo de vendas para começar.")