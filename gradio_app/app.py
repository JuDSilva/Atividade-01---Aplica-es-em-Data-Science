import gradio as gr
import csv
import os

ARQUIVO = "pacientes.csv"

COLUNAS = [
    "Nome",
    "Idade",
    "Convênio",
    "Prioridade",
    "Motivo / Observações"
]


def cadastrar(nome, idade, convenio, prioridade, motivo):
    novo_cadastro = [
        nome,
        idade,
        convenio,
        prioridade,
        motivo
    ]

    arquivo_existe = os.path.exists(ARQUIVO)

    with open(ARQUIVO, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        if not arquivo_existe:
            escritor.writerow(COLUNAS)

        escritor.writerow(novo_cadastro)

    with open(ARQUIVO, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        dados = list(leitor)

    ultimos = dados[-6:]

    return (
        "✅ Paciente cadastrado com sucesso!",
        ultimos
    )


with gr.Blocks(title="Cadastro de Pacientes") as app:

    gr.Markdown("# 🏥 Cadastro de Pacientes")
    gr.Markdown("Preencha os dados do paciente abaixo.")

    nome = gr.Textbox(
        label="Nome do paciente",
        placeholder="Digite o nome"
    )

    idade = gr.Number(
        label="Idade",
        minimum=0,
        maximum=120,
        precision=0
    )

    convenio = gr.Dropdown(
        choices=[
            "Particular",
            "Unimed",
            "Amil",
            "Bradesco Saúde",
            "SulAmérica"
        ],
        label="Convênio",
        value="Particular"
    )

    prioridade = gr.Slider(
        minimum=1,
        maximum=5,
        step=1,
        value=3,
        label="Prioridade do atendimento"
    )

    motivo = gr.Textbox(
        label="Motivo da consulta / Observações",
        placeholder="Digite o motivo da consulta ou outras observações",
        lines=4
    )

    botao = gr.Button("Cadastrar")

    mensagem = gr.Markdown()

    tabela = gr.Dataframe(
        headers=COLUNAS,
        label="Últimos cadastros",
        interactive=False
    )

    botao.click(
        fn=cadastrar,
        inputs=[
            nome,
            idade,
            convenio,
            prioridade,
            motivo
        ],
        outputs=[
            mensagem,
            tabela
        ]
    )


app.launch()
