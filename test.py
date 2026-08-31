import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise de Acidentes 2025", layout="wide")

# Leitura e preparação dos dados
df = pd.read_csv('csv/acidentes2025.csv', encoding='latin1', sep=';')
df['data_inversa'] = pd.to_datetime(df['data_inversa'])
df['hora'] = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.hour
df['idade'] = pd.to_numeric(df['idade'], errors='coerce')
df['feridos_graves'] = pd.to_numeric(df['feridos_graves'], errors='coerce')
df['mortos'] = pd.to_numeric(df['mortos'], errors='coerce')

st.title("🚦 Análise de Acidentes de Trânsito - Brasil 2025")

# --- SIDEBAR PARA FILTROS ---
st.sidebar.header("Filtros")

# Filtro UF
selected_uf = st.sidebar.multiselect(
    "Selecione UF",
    df['uf'].unique(),
    default=df['uf'].unique(),
    key="filtro_uf"
)

# Filtro Tipo de Acidente
selected_tipo_acidente = st.sidebar.multiselect(
    "Tipo de Acidente",
    df['tipo_acidente'].unique(),
    default=df['tipo_acidente'].unique(),
    key="filtro_tipo"
)

# Filtragem inicial
df_temp = df[(df['uf'].isin(selected_uf)) & (df['tipo_acidente'].isin(selected_tipo_acidente))]

# --- Filtro com busca por Município ---
st.sidebar.subheader("Filtro por Município")

# Campo de busca de texto
city_search = st.sidebar.text_input("Digite parte do nome do município:")

# Filtra os municípios disponíveis com base na busca
available_cities = sorted(df_temp['municipio'].unique())
if city_search:
    available_cities = [m for m in available_cities if city_search.lower() in m.lower()]

# Multiselect com resultado filtrado
selected_cities = st.sidebar.multiselect(
    "Selecione Município",
    available_cities,
    default=available_cities,
    key="filtro_municipio"
)

# Aplicando todos os filtros
df_filtered = df_temp[df_temp['municipio'].isin(selected_cities)]

# --- Acidentes por UF ---
uf_counts = df_filtered['uf'].value_counts().reset_index()
uf_counts.columns = ['UF', 'Quantidade']
st.subheader("Acidentes por Estado (UF)")
fig = px.bar(uf_counts, x='UF', y='Quantidade', text='Quantidade')
st.plotly_chart(fig, use_container_width=True)

# --- Distribuição por horário ---
st.subheader("Distribuição por Hora do Dia")
fig2 = px.histogram(df_filtered, x='hora', nbins=24, title="Acidentes por Hora")
st.plotly_chart(fig2, use_container_width=True)

# --- Principais causas ---
st.subheader("Principais Causas de Acidentes")
causa_counts = df_filtered['causa_acidente'].value_counts().head(10).reset_index()
causa_counts.columns = ['Causa', 'Quantidade']
fig3 = px.bar(causa_counts, x='Causa', y='Quantidade', text='Quantidade')
st.plotly_chart(fig3, use_container_width=True)

# --- Acidentes por dia da semana ---
st.subheader("Acidentes por Dia da Semana")
dia_counts = df_filtered['dia_semana'].value_counts().reindex([
    'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira',
    'sexta-feira', 'sábado', 'domingo'
]).reset_index()
dia_counts.columns = ['Dia', 'Quantidade']
fig4 = px.bar(dia_counts, x='Dia', y='Quantidade', text='Quantidade')
st.plotly_chart(fig4, use_container_width=True)

# --- Acidentes por fase do dia ---
st.subheader("Acidentes por Fase do Dia")
fase_counts = df_filtered['fase_dia'].value_counts().reset_index()
fase_counts.columns = ['Fase', 'Quantidade']
fig5 = px.pie(fase_counts, names='Fase', values='Quantidade', title="Distribuição por Fase do Dia")
st.plotly_chart(fig5, use_container_width=True)

# --- Acidentes graves ou mortes ---
st.subheader("Acidentes Graves ou com Mortes")
df_severo = df_filtered[(df_filtered['feridos_graves'] > 0) | (df_filtered['mortos'] > 0)]
fig6 = px.scatter(
    df_severo,
    x='hora',
    y='municipio',
    size='mortos',
    color='feridos_graves',
    hover_data=['tipo_acidente', 'causa_acidente', 'uf'],
    title="Acidentes Graves e Mortes"
)
st.plotly_chart(fig6, use_container_width=True)

# --- Cidades com mais acidentes graves ou mortes ---
st.subheader("Cidades com Mais Acidentes Graves ou Mortes")

severe_cities = (
    df_severo.groupby('municipio')[['feridos_graves', 'mortos']]
    .sum()
    .reset_index()
)
severe_cities['total'] = severe_cities['feridos_graves'] + severe_cities['mortos']
severe_cities = severe_cities.sort_values('total', ascending=False)

fig_cidades = px.bar(
    severe_cities.head(15),
    x='municipio',
    y='total',
    text='total',
    color='mortos',
    title="Top 15 Cidades com Acidentes Graves ou Mortes",
    labels={'total': 'Total de Casos (Graves + Mortes)', 'municipio': 'Município'}
)
st.plotly_chart(fig_cidades, use_container_width=True)

st.markdown("#### 🔍 Tabela detalhada de cidades com casos graves ou mortes")
st.dataframe(severe_cities, use_container_width=True, hide_index=True)

# --- Tipos de veículos mais envolvidos ---
st.subheader("Tipos de Veículos Envolvidos")
veiculo_counts = df_filtered['tipo_veiculo'].value_counts().reset_index()
veiculo_counts.columns = ['Veículo', 'Quantidade']
fig7 = px.bar(veiculo_counts, x='Veículo', y='Quantidade', text='Quantidade')
st.plotly_chart(fig7, use_container_width=True)

# --- Faixa etária das vítimas ---
st.subheader("Faixa Etária das Vítimas")

# Limita valores plausíveis
df_idade = df_filtered[(df_filtered['idade'] >= 0) & (df_filtered['idade'] <= 120)]

# Agrupa em faixas etárias
bins = [0, 12, 17, 25, 35, 45, 55, 65, 75, 120]
labels = ['0-12', '13-17', '18-25', '26-35', '36-45', '46-55', '56-65', '66-75', '75+']
df_idade['faixa_etaria'] = pd.cut(df_idade['idade'], bins=bins, labels=labels, right=False)

faixa_counts = df_idade['faixa_etaria'].value_counts().sort_index().reset_index()
faixa_counts.columns = ['Faixa Etária', 'Quantidade']

fig8 = px.bar(
    faixa_counts,
    x='Faixa Etária',
    y='Quantidade',
    text='Quantidade',
    title="Distribuição de Acidentes por Faixa Etária",
)
st.plotly_chart(fig8, use_container_width=True)

# --- Sexo das vítimas ---
st.subheader("Acidentes por Sexo")
sexo_counts = df_filtered['sexo'].value_counts().reset_index()
sexo_counts.columns = ['Sexo', 'Quantidade']
fig9 = px.pie(sexo_counts, names='Sexo', values='Quantidade', title="Distribuição por Sexo")
st.plotly_chart(fig9, use_container_width=True)

# --- Rodapé fixo ---
with open('footer.html', 'r', encoding='utf-8') as file:
    footer = file.read()

st.markdown(footer, unsafe_allow_html=True)
