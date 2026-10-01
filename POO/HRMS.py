import customtkinter as ctk
from tkinter import messagebox
import re


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# FUNÇÕES
# =========================================================

def centralizar_janela(janela, largura, altura):
    """Centraliza a janela na tela."""

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2

    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def validar_matricula(matricula):
    """
    Valida o formato:
    MAT-2026-01
    """

    padrao = r"^MAT-\d{4}-\d{2}$"

    return re.match(padrao, matricula) is not None


def salvar_colaborador():

    matricula = entrada_matricula.get().strip()
    nome = entrada_nome.get().strip()
    cargo = entrada_cargo.get().strip()
    departamento = combo_departamento.get()
    modalidade = modalidade_var.get()

    # ==========================================
    # VALIDAÇÃO DOS CAMPOS
    # ==========================================

    if not matricula or not nome or not cargo:
        messagebox.showwarning(
            "Campos obrigatórios",
            "Preencha todos os campos obrigatórios."
        )

        auditoria.configure(
            text="Auditoria: Existem campos obrigatórios não preenchidos.",
            text_color="orange"
        )

        return

    if not departamento or departamento == "Selecione o departamento":
        messagebox.showwarning(
            "Departamento",
            "Selecione um departamento."
        )

        auditoria.configure(
            text="Auditoria: Departamento não selecionado.",
            text_color="orange"
        )

        return

    if not modalidade:
        messagebox.showwarning(
            "Modalidade",
            "Selecione uma modalidade de trabalho."
        )

        auditoria.configure(
            text="Auditoria: Modalidade de trabalho não selecionada.",
            text_color="orange"
        )

        return

    # ==========================================
    # VALIDAÇÃO DA MATRÍCULA
    # ==========================================

    if not validar_matricula(matricula):
        messagebox.showerror(
            "Matrícula inválida",
            "A matrícula deve seguir o formato:\n\n"
            "MAT-2026-01"
        )

        auditoria.configure(
            text="Auditoria: Formato de matrícula inválido.",
            text_color="red"
        )

        return

    # ==========================================
    # CONFIRMAÇÃO
    # ==========================================

    confirmar = messagebox.askyesno(
        "Confirmar cadastro",
        f"Deseja salvar o colaborador?\n\n"
        f"Matrícula: {matricula}\n"
        f"Nome: {nome}\n"
        f"Cargo: {cargo}\n"
        f"Departamento: {departamento}\n"
        f"Modalidade: {modalidade}"
    )

    if not confirmar:
        return

    # ==========================================
    # CADASTRO REALIZADO
    # ==========================================

    auditoria.configure(
        text=f"Auditoria: Último registro salvo com sucesso: "
             f"{matricula} - {nome}",
        text_color="lightgreen"
    )

    messagebox.showinfo(
        "Cadastro realizado",
        "Colaborador cadastrado com sucesso!"
    )


def limpar_formulario():

    confirmar = messagebox.askyesno(
        "Limpar formulário",
        "Tem certeza que deseja limpar todos os campos?"
    )

    if not confirmar:
        return

    entrada_matricula.delete(0, "end")
    entrada_nome.delete(0, "end")
    entrada_cargo.delete(0, "end")

    combo_departamento.set("Selecione o departamento")

    modalidade_var.set("")

    auditoria.configure(
        text="Auditoria: Formulário limpo.",
        text_color="gray"
    )


# =========================================================
# JANELA PRINCIPAL
# =========================================================

app = ctk.CTk()

app.title(
    "HRMS - Sistema de Gestão de Colaboradores e Quadro Funcional"
)

# Janela fixa
app.resizable(False, False)

# Centralizar
centralizar_janela(app, 580, 460)


# =========================================================
# TÍTULO
# =========================================================

titulo = ctk.CTkLabel(
    app,
    text="HRMS - Sistema de Gestão de Colaboradores",
    font=ctk.CTkFont(size=20, weight="bold")
)

titulo.pack(pady=(20, 0))


subtitulo = ctk.CTkLabel(
    app,
    text="Módulo de Cadastro e Gestão do Quadro Funcional",
    font=ctk.CTkFont(size=12)
)

subtitulo.pack(pady=(2, 15))


# =========================================================
# FRAME DO FORMULÁRIO
# =========================================================

frame_formulario = ctk.CTkFrame(
    app,
    width=520,
    height=290,
    corner_radius=10
)

frame_formulario.pack(padx=30, fill="x")

frame_formulario.pack_propagate(False)


# =========================================================
# MATRÍCULA
# =========================================================

label_matricula = ctk.CTkLabel(
    frame_formulario,
    text="Matrícula Funcional:"
)

label_matricula.grid(
    row=0,
    column=0,
    padx=15,
    pady=(15, 5),
    sticky="w"
)

entrada_matricula = ctk.CTkEntry(
    frame_formulario,
    placeholder_text="Ex: MAT-2026-01",
    width=320
)

entrada_matricula.grid(
    row=0,
    column=1,
    padx=15,
    pady=(15, 5)
)


# =========================================================
# NOME
# =========================================================

label_nome = ctk.CTkLabel(
    frame_formulario,
    text="Nome Completo:"
)

label_nome.grid(
    row=1,
    column=0,
    padx=15,
    pady=5,
    sticky="w"
)

entrada_nome = ctk.CTkEntry(
    frame_formulario,
    placeholder_text="Nome do colaborador",
    width=320
)

entrada_nome.grid(
    row=1,
    column=1,
    padx=15,
    pady=5
)


# =========================================================
# CARGO
# =========================================================

label_cargo = ctk.CTkLabel(
    frame_formulario,
    text="Cargo / Função:"
)

label_cargo.grid(
    row=2,
    column=0,
    padx=15,
    pady=5,
    sticky="w"
)

entrada_cargo = ctk.CTkEntry(
    frame_formulario,
    placeholder_text="Ex: Desenvolvedor",
    width=320
)

entrada_cargo.grid(
    row=2,
    column=1,
    padx=15,
    pady=5
)


# =========================================================
# DEPARTAMENTO
# =========================================================

label_departamento = ctk.CTkLabel(
    frame_formulario,
    text="Departamento:"
)

label_departamento.grid(
    row=3,
    column=0,
    padx=15,
    pady=5,
    sticky="w"
)

departamentos = [
    "TI & Sistemas",
    "Recursos Humanos",
    "Operações & Logística",
    "Financeiro",
    "Marketing"
]

combo_departamento = ctk.CTkComboBox(
    frame_formulario,
    values=departamentos,
    width=320
)

combo_departamento.set("Selecione o departamento")

combo_departamento.grid(
    row=3,
    column=1,
    padx=15,
    pady=5
)


# =========================================================
# MODALIDADE
# =========================================================

label_modalidade = ctk.CTkLabel(
    frame_formulario,
    text="Modalidade:"
)

label_modalidade.grid(
    row=4,
    column=0,
    padx=15,
    pady=5,
    sticky="w"
)

modalidade_var = ctk.StringVar(value="")


radio_presencial = ctk.CTkRadioButton(
    frame_formulario,
    text="Presencial",
    variable=modalidade_var,
    value="Presencial"
)

radio_presencial.grid(
    row=4,
    column=1,
    padx=(15, 0),
    pady=5,
    sticky="w"
)


radio_hibrido = ctk.CTkRadioButton(
    frame_formulario,
    text="Híbrido",
    variable=modalidade_var,
    value="Híbrido"
)

radio_hibrido.grid(
    row=4,
    column=1,
    padx=(120, 0),
    pady=5,
    sticky="w"
)


radio_remoto = ctk.CTkRadioButton(
    frame_formulario,
    text="Remote/Home Office",
    variable=modalidade_var,
    value="Remote/Home Office"
)

radio_remoto.grid(
    row=4,
    column=1,
    padx=(220, 0),
    pady=5,
    sticky="w"
)


# =========================================================
# BOTÕES
# =========================================================

frame_botoes = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

frame_botoes.pack(pady=12)


botao_salvar = ctk.CTkButton(
    frame_botoes,
    text="Salvar Colaborador",
    width=190,
    height=35,
    command=salvar_colaborador
)

botao_salvar.grid(
    row=0,
    column=0,
    padx=5
)


botao_limpar = ctk.CTkButton(
    frame_botoes,
    text="Limpar Formulário",
    width=190,
    height=35,
    fg_color="gray",
    hover_color="darkgray",
    command=limpar_formulario
)

botao_limpar.grid(
    row=0,
    column=1,
    padx=5
)


# =========================================================
# AUDITORIA
# =========================================================

auditoria = ctk.CTkLabel(
    app,
    text="Auditoria: Aguardando operação...",
    font=ctk.CTkFont(size=11)
)

auditoria.pack(
    side="bottom",
    pady=10
)


# =========================================================
# EXECUTAR
# =========================================================

app.mainloop()