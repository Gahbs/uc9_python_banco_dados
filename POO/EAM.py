import tkinter as tk


def criar_kpi(pai, titulo, valor):

    card = tk.Frame(
        pai,
        bg="#1e293b"
    )

    tk.Label(
        card,
        text=titulo,
        bg="#1e293b",
        fg="#94a3b8",
        font=("Arial", 8, "bold")
    ).pack(pady=(8, 0))

    tk.Label(
        card,
        text=valor,
        bg="#1e293b",
        fg="white",
        font=("Arial", 18, "bold")
    ).pack()

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=3
    )


# =========================
# JANELA
# =========================

janela = tk.Tk()

janela.title(
    "Painel de Controle - Gestão de Ativos Corporativos (EAM)"
)

largura = 500
altura = 350

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela - largura) // 2
pos_y = (altura_tela - altura) // 2

janela.geometry(
    f"{largura}x{altura}+{pos_x}+{pos_y}"
)

janela.resizable(False, False)

janela.configure(
    bg="#0f172a"
)


# =========================
# CABEÇALHO
# =========================

cabecalho = tk.Frame(
    janela,
    bg="#1e293b",
    height=70
)

cabecalho.pack(
    fill="x"
)

tk.Label(
    cabecalho,
    text="PAINEL DE CONTROLE",
    bg="#1e293b",
    fg="white",
    font=("Arial", 16, "bold")
).pack(pady=(10, 0))

tk.Label(
    cabecalho,
    text="Gestão de Ativos Corporativos (EAM)",
    bg="#1e293b",
    fg="#94a3b8",
    font=("Arial", 9)
).pack()


# =========================
# KPIs
# =========================

kpis = tk.Frame(
    janela,
    bg="#0f172a"
)

kpis.pack(
    fill="x",
    padx=15,
    pady=15
)

criar_kpi(kpis, "TOTAL", "120")
criar_kpi(kpis, "OPERAÇÃO", "98")
criar_kpi(kpis, "MANUTENÇÃO", "15")
criar_kpi(kpis, "CRÍTICOS", "7")


# =========================
# SAÚDE OPERACIONAL
# =========================

saude = tk.Frame(
    janela,
    bg="#0f172a"
)

saude.pack(
    fill="both",
    expand=True
)

tk.Label(
    saude,
    text="SAÚDE OPERACIONAL",
    bg="#0f172a",
    fg="#94a3b8",
    font=("Arial", 10, "bold")
).pack(pady=(5, 0))

tk.Label(
    saude,
    text="92%",
    bg="#0f172a",
    fg="#22c55e",
    font=("Arial", 32, "bold")
).pack()

tk.Label(
    saude,
    text="INFRAESTRUTURA SAUDÁVEL",
    bg="#0f172a",
    fg="white",
    font=("Arial", 10, "bold")
).pack()


janela.mainloop()