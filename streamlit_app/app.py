import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Cadastro de Pacientes",
    page_icon="🏥",
    layout="centered"
)

CSV_FILE = "pacientes.csv"

COLUNAS = [
    "Nome",
    "Idade",
    "Convênio",
    "Prioridade",
    "Motivo / Observações"
]

# Inicializa os dados da sessão
if "cadastros" not in st.session_state:
    if os.path.exists(CSV_FILE):
        try:
            st.session_state.cadastros = pd.read_csv(CSV_FILE)
        except Exception:
            st.session_state.cadastros = pd.DataFrame(columns=COLUNAS)
    else:
        st.session_state.cadastros = pd.DataFrame(columns=COLUNAS)


st.title("🏥 Cadastro de Pacientes")
st.write("Preencha os dados do paciente abaixo.")


# Formulário
with st.form("form_cadastro"):

    nome = st.text_input("Nome do paciente")

    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        value=18,
        step=1
    )

    convenio = st.selectbox(
        "Convênio",
        [
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Amil",
            "Particular"
        ]
    )

    prioridade = st.slider(
        "Prioridade do atendimento",
        min_value=1,
        max_value=5,
        value=3
    )

    motivo = st.text_area(
        "Motivo da consulta / Observações"
    )

    cadastrar = st.form_submit_button("Cadastrar")


# Cadastro do paciente
if cadastrar:

    if not nome.strip():

        st.error("Informe o nome do paciente.")

    else:

        novo_cadastro = pd.DataFrame([{
            "Nome": nome.strip(),
            "Idade": int(idade),
            "Convênio": convenio,
            "Prioridade": int(prioridade),
            "Motivo / Observações": motivo.strip()
        }])

        st.session_state.cadastros = pd.concat(
            [st.session_state.cadastros, novo_cadastro],
            ignore_index=True
        )

        # Salva no arquivo CSV
        st.session_state.cadastros.to_csv(
            CSV_FILE,
            index=False,
            encoding="utf-8"
        )

        st.success("✅ Paciente cadastrado com sucesso!")


# Exibe os últimos cadastros
st.subheader("Últimos cadastros")

st.dataframe(
    st.session_state.cadastros.tail(10),
    width="stretch",
    hide_index=True,
    column_config={
        "Nome": st.column_config.TextColumn(
            "Nome",
            width="large"
        ),
        "Idade": st.column_config.NumberColumn(
            "Idade",
            width="small"
        ),
        "Convênio": st.column_config.TextColumn(
            "Convênio",
            width="medium"
        ),
        "Prioridade": st.column_config.NumberColumn(
            "Prioridade",
            width="small"
        ),
        "Motivo / Observações": st.column_config.TextColumn(
            "Motivo / Observações",
            width="large"
        )
    },
    height=300
)



# Botão para baixar o CSV
csv_data = st.session_state.cadastros.to_csv(
    index=False,
    encoding="utf-8"
)

st.download_button(
    label="⬇️ Baixar pacientes.csv",
    data=csv_data,
    file_name="pacientes.csv",
    mime="text/csv"
)
