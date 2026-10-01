import customtkinter as ctk
from tkinter import messagebox


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

saldo = 0.0


# =========================================================
# FUNÇÃO PARA CENTRALIZAR A JANELA
# =========================================================

def centralizar_janela(janela, largura, altura):

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    x = (largura_tela - largura) // 2
    y = (altura_tela - altura) // 2

    janela.geometry(f"{largura}x{altura}+{x}+{y}")


# =========================================================
# FUNÇÃO PARA FORMATAR DINHEIRO
# =========================================================

def formatar_reais(valor):

    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# =========================================================
# REGISTRAR OPERAÇÃO
# =========================================================

def registrar_operacao():

    global saldo

    descricao = entrada_descricao.get().strip()
    valor_texto = entrada_valor.get().strip()
    tipo = tipo_movimentacao.get()

    # -----------------------------------------------------
    # VALIDAÇÃO DA DESCRIÇÃO
    # -----------------------------------------------------

    if not descricao:

        messagebox.showwarning(
            "Campo obrigatório",
            "Preencha a descrição do lançamento."
        )

        auditoria.configure(
            text="Auditoria: Descrição não preenchida.",
            text_color="orange"
        )

        return

    # -----------------------------------------------------
    # VALIDAÇÃO DO VALOR
    # -----------------------------------------------------

    if not valor_texto:

        messagebox.showwarning(
            "Campo obrigatório",
            "Informe o valor da operação."
        )

        auditoria.configure(
            text="Auditoria: Valor não informado.",
            text_color="orange"
        )

        return

    try:

        valor = float(valor_texto.replace(",", "."))

    except ValueError:

        messagebox.showerror(
            "Valor inválido",
            "O valor deve ser numérico.\n\n"
            "Exemplo: 1500.50"
        )

        auditoria.configure(
            text="Auditoria: Valor informado não é numérico.",
            text_color="red"
        )

        return

    # -----------------------------------------------------
    # VALOR MAIOR QUE ZERO
    # -----------------------------------------------------

    if valor <= 0:

        messagebox.showwarning(
            "Valor inválido",
            "O valor deve ser maior que zero."
        )

        auditoria.configure(
            text="Auditoria: O valor deve ser maior que zero.",
            text_color="red"
        )

        return

    # -----------------------------------------------------
    # TIPO DE MOVIMENTAÇÃO
    # -----------------------------------------------------

    if not tipo:

        messagebox.showwarning(
            "Tipo de movimentação",
            "Selecione Entrada / Receita ou Saída / Despesa."
        )

        auditoria.configure(
            text="Auditoria: Tipo de movimentação não selecionado.",
            text_color="orange"
        )

        return

    # -----------------------------------------------------
    # ATUALIZAÇÃO DO SALDO
    # -----------------------------------------------------

    if tipo == "Entrada / Receita":

        saldo += valor

    else:

        saldo -= valor

    # -----------------------------------------------------
    # ATUALIZAR SALDO NA TELA
    # -----------------------------------------------------

    label_saldo_valor.configure(
        text=formatar_reais(saldo)
    )

    # -----------------------------------------------------
    # AUDITORIA
    # -----------------------------------------------------

    auditoria.configure(
        text=f"Auditoria: {tipo} registrada — "
             f"{descricao} | {formatar_reais(valor)}",
        text_color="lightgreen"
    )

    messagebox.showinfo(
        "Operação registrada",
        f"Operação registrada com sucesso!\n\n"
        f"Descrição: {descricao}\n"
        f"Valor: {formatar_reais(valor)}\n"
        f"Tipo: {tipo}\n\n"
        f"Saldo atual: {formatar_reais(saldo)}"
    )


# =========================================================
# LIMPAR FORMULÁRIO
# =========================================================

def limpar_formulario():

    confirmar = messagebox.askyesno(
        "Limpar formulário",
        "Deseja realmente limpar os campos?"
    )

    if not confirmar:
        return

    entrada_descricao.delete(0, "end")
    entrada_valor.delete(0, "end")

    tipo_movimentacao.set("")

    auditoria.configure(
        text="Auditoria: Formulário limpo. Saldo mantido.",
        text_color="gray"
    )


# =========================================================
# JANELA PRINCIPAL
# =========================================================

app = ctk.CTk()

app.title(
    "Controle Financeiro Empresarial - Fluxo de Caixa"
)

app.resizable(False, False)

centralizar_janela(app, 550, 450)


# =========================================================
# TÍTULO
# =========================================================

titulo = ctk.CTkLabel(
    app,
    text="Controle Financeiro Empresarial",
    font=ctk.CTkFont(
        size=22,
        weight="bold"
    )
)

titulo.pack(pady=(20, 0))


subtitulo = ctk.CTkLabel(
    app,
    text="Módulo de Lançamento e Controle de Fluxo de Caixa",
    font=ctk.CTkFont(size=12)
)

subtitulo.pack(pady=(3, 15))


# =========================================================
# SALDO
# =========================================================

frame_saldo = ctk.CTkFrame(
    app,
    width=490,
    height=70
)

frame_saldo.pack(
    padx=30,
    fill="x"
)

frame_saldo.pack_propagate(False)


label_saldo = ctk.CTkLabel(
    frame_saldo,
    text="SALDO OPERACIONAL",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    )
)

label_saldo.pack(
    pady=(8, 0)
)


label_saldo_valor = ctk.CTkLabel(
    frame_saldo,
    text="R$ 0,00",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
)

label_saldo_valor.pack()


# =========================================================
# FORMULÁRIO
# =========================================================

frame_formulario = ctk.CTkFrame(
    app,
    width=490,
    height=210
)

frame_formulario.pack(
    padx=30,
    pady=10,
    fill="x"
)

frame_formulario.pack_propagate(False)


# =========================================================
# DESCRIÇÃO
# =========================================================

label_descricao = ctk.CTkLabel(
    frame_formulario,
    text="Descrição:"
)

label_descricao.grid(
    row=0,
    column=0,
    padx=15,
    pady=(15, 5),
    sticky="w"
)


entrada_descricao = ctk.CTkEntry(
    frame_formulario,
    placeholder_text="Ex: Venda de produto",
    width=300
)

entrada_descricao.grid(
    row=0,
    column=1,
    padx=15,
    pady=(15, 5)
)


# =========================================================
# VALOR
# =========================================================

label_valor = ctk.CTkLabel(
    frame_formulario,
    text="Valor (R$):"
)

label_valor.grid(
    row=1,
    column=0,
    padx=15,
    pady=5,
    sticky="w"
)


entrada_valor = ctk.CTkEntry(
    frame_formulario,
    placeholder_text="Ex: 1500,00",
    width=300
)

entrada_valor.grid(
    row=1,
    column=1,
    padx=15,
    pady=5
)


# =========================================================
# TIPO DE MOVIMENTAÇÃO
# =========================================================

label_tipo = ctk.CTkLabel(
    frame_formulario,
    text="Movimentação:"
)

label_tipo.grid(
    row=2,
    column=0,
    padx=15,
    pady=5,
    sticky="w"
)


tipo_movimentacao = ctk.StringVar(value="")


radio_entrada = ctk.CTkRadioButton(
    frame_formulario,
    text="Entrada / Receita",
    variable=tipo_movimentacao,
    value="Entrada / Receita"
)

radio_entrada.grid(
    row=2,
    column=1,
    padx=15,
    pady=5,
    sticky="w"
)


radio_saida = ctk.CTkRadioButton(
    frame_formulario,
    text="Saída / Despesa",
    variable=tipo_movimentacao,
    value="Saída / Despesa"
)

radio_saida.grid(
    row=3,
    column=1,
    padx=15,
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

frame_botoes.pack(
    pady=5
)


botao_registrar = ctk.CTkButton(
    frame_botoes,
    text="Registrar Operação",
    width=200,
    height=35,
    command=registrar_operacao
)

botao_registrar.grid(
    row=0,
    column=0,
    padx=5
)


botao_limpar = ctk.CTkButton(
    frame_botoes,
    text="Limpar Formulário",
    width=200,
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