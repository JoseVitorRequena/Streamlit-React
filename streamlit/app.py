import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from streamlit.components.v1 import components

# Configuração inicial
st.set_page_config(page_title="Análise Educacional", layout="wide")

st.header("🎓 Painel Interativo")

# Caminho para o build do React  -------------------------------------------------------------------------------------------------------------------------
is_dev = os.getenv("ENV") == "development"

# try is_dev:
# except
react_component = components.declare_component(
    "Streamlit", 
    path= os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend/meu-app-react/build")
)

react_component(key=None)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

CSV_PATH = "../backend/data/dados.csv"
df = pd.read_csv(CSV_PATH)

# Sidebar com filtros
st.sidebar.header("Filtros")
school_filter = st.sidebar.selectbox("Escola", ["Todas"] + list(df['school'].unique()))
sex_filter = st.sidebar.selectbox("Gênero", ["Todos"] + list(df['sex'].unique()))
age_filter = st.sidebar.slider("Idade", min_value=15, max_value=22, value=(15, 22))

# Aplicar filtros
filtered_df = df.copy()
if school_filter != "Todas":
    filtered_df = filtered_df[filtered_df['school'] == school_filter]
if sex_filter != "Todos":
    filtered_df = filtered_df[filtered_df['sex'] == sex_filter]
filtered_df = filtered_df[(filtered_df['age'] >= age_filter[0]) & (filtered_df['age'] <= age_filter[1])]

# Mostrar dados
st.header("📋 Visão Geral dos Dados")
st.write(f"Total de estudantes: {len(filtered_df)}")
st.dataframe(filtered_df.head(), height=210)

# Configuração de estilo para todos os gráficos
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (8, 4)
plt.rcParams['font.size'] = 9

# Análise de Desempenho
st.header("📈 Análise de Desempenho")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Média G1", round(filtered_df['G1'].mean(), 2))
with col2:
    st.metric("Média G2", round(filtered_df['G2'].mean(), 2))
with col3:
    st.metric("Média G3", round(filtered_df['G3'].mean(), 2))

# Gráfico de evolução das notas
fig, ax = plt.subplots(figsize=(6, 3))
sns.lineplot(data=filtered_df[['G1', 'G2', 'G3']].mean(), ax=ax, marker='o')
ax.set_title("Evolução das Notas Médias", fontsize=10)
ax.set_ylabel("Nota Média", fontsize=9)
ax.set_xlabel("Avaliação", fontsize=9)
st.pyplot(fig)

# Distribuição das notas
st.subheader("Distribuição das Notas")
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
sns.histplot(filtered_df['G1'], kde=True, ax=axes[0], bins=15)
sns.histplot(filtered_df['G2'], kde=True, ax=axes[1], bins=15)
sns.histplot(filtered_df['G3'], kde=True, ax=axes[2], bins=15)
axes[0].set_title("G1", fontsize=9)
axes[1].set_title("G2", fontsize=9)
axes[2].set_title("G3", fontsize=9)
plt.tight_layout()
st.pyplot(fig)

# Análise por características
st.header("🔍 Análise por Características")

# Notas por gênero
st.subheader("Notas por Gênero")
fig, ax = plt.subplots(figsize=(4, 3))
sns.boxplot(data=filtered_df, x='sex', y='G3', ax=ax, width=0.5)
ax.set_title("Notas Finais por Gênero", fontsize=9)
ax.set_ylabel("Nota Final (G3)", fontsize=8)
ax.set_xlabel("Gênero", fontsize=8)
st.pyplot(fig)

# Notas por idade
st.subheader("Notas por Idade")
fig, ax = plt.subplots(figsize=(6, 3))
sns.boxplot(data=filtered_df, x='age', y='G3', ax=ax, width=0.6)
ax.set_title("Notas Finais por Idade", fontsize=9)
ax.set_ylabel("Nota Final (G3)", fontsize=8)
ax.set_xlabel("Idade", fontsize=8)
st.pyplot(fig)

# Relação entre faltas e notas
st.subheader("Relação entre Faltas e Notas")
fig, ax = plt.subplots(figsize=(6, 3))
sns.scatterplot(data=filtered_df, x='absences', y='G3', hue='sex', ax=ax, s=30)
ax.set_title("Faltas vs Notas Finais", fontsize=9)
ax.set_ylabel("Nota Final (G3)", fontsize=8)
ax.set_xlabel("Número de Faltas", fontsize=8)
plt.legend(fontsize=8)
st.pyplot(fig)

# Análise de fatores influentes
st.header("📊 Fatores que Influenciam o Desempenho")

# Tempo de estudo vs notas
st.subheader("Tempo de Estudo vs Notas")
fig, ax = plt.subplots(figsize=(5, 3))
sns.boxplot(data=filtered_df, x='studytime', y='G3', ax=ax, width=0.6)
ax.set_title("Notas por Tempo de Estudo (1-4)", fontsize=9)
ax.set_ylabel("Nota Final (G3)", fontsize=8)
ax.set_xlabel("Tempo de Estudo", fontsize=8)
st.pyplot(fig)

# Suporte educacional vs notas
st.subheader("Suporte Educacional vs Notas")
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
sns.boxplot(data=filtered_df, x='schoolsup', y='G3', ax=axes[0], width=0.5)
sns.boxplot(data=filtered_df, x='famsup', y='G3', ax=axes[1], width=0.5)
axes[0].set_title("Suporte da Escola", fontsize=9)
axes[1].set_title("Suporte da Família", fontsize=9)
axes[0].set_ylabel("Nota Final (G3)", fontsize=8)
axes[1].set_ylabel("")
plt.tight_layout()
st.pyplot(fig)

# Correlações
st.subheader("Matriz de Correlação")
fig, ax = plt.subplots(figsize=(5, 4))
corr = filtered_df[['G1', 'G2', 'G3', 'studytime', 'failures', 'absences', 'age']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt=".2f", annot_kws={"size": 8})
ax.set_title("Correlação entre Variáveis", fontsize=9)
st.pyplot(fig)

# Análise de outliers
st.header("🔎 Análise de Casos Interessantes")

# Melhores alunos
st.subheader("Top 5 Melhores Alunos (G3)")
st.dataframe(filtered_df.nlargest(5, 'G3')[['sex', 'age', 'studytime', 'G1', 'G2', 'G3']], height=150)

# Alunos com maior melhoria
filtered_df['melhoria'] = filtered_df['G3'] - filtered_df['G1']
st.subheader("Top 5 Maiores Melhorias")
st.dataframe(filtered_df.nlargest(5, 'melhoria')[['sex', 'age', 'G1', 'G3', 'melhoria']], height=150)

# Alunos com pior desempenho
st.subheader("Top 5 Piores Desempenhos")
st.dataframe(filtered_df.nsmallest(5, 'G3')[['sex', 'age', 'studytime', 'G1', 'G2', 'G3']], height=210)