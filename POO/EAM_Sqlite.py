import tkinter as tk
import sqlite3

#=====
#MODEL
#=====

class AtivoModel:
    def __init__(self):
        self.banco = "eam_mvc_ativos.db"

        self.criar_banco()
        self.inserir_dados_iniciais()

    def criar_banco(self):
        conexao = sqlite3.connect(self.banco)
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ativos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (
                        status IN (
                            'EM_OPERACAO',
                            'MANUTENCAO',
                            'CRITICO'
                        )
                    )
            )
        """)

        conexao.commit()
        conexao.close()

    def inserir_dados_iniciais(self):

        conexao = sqlite3.connect(self.banco)
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT (*) FROM ativos")
        quantidade = cursor.fetchone()[0]

        if quantidade == 0:
            dados = [
                ("Computador Dell", "EM_OPERACAO"),
                ("Notebook Lenovo", "EM_OPERACAO"),
                ("Servidor Dell", "EM_OPERACAO"),
                ("Monitor Samsung", "EM_OPERACAO"),
                ("Impressora HP", "MANUTENCAO"),
                ("Projetor Epson", "MANUTENCAO"),
                ("Roteador Cisco", "CRITICO"),
                ("Scanner Epson", "EM_OPERACAO")
            ]

            cursor.executemany("""
                INSERT INTO ativos (nome, status)
                VALUES (?, ?)
            """, dados)

        conexao.commit()
        conexao.close()

    def contar_total(self):

        conexao = sqlite3.connect(self.banco)
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM ativos
        """)

        resultado = cursor.fetchone()[0]

        conexao.close()

        return resultado

    def contar_operacao(self):

        conexao = sqlite3.connect(self.banco)
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM ativos
            WHERE status = 'EM_OPERACAO'
        """)

        resultado = cursor.fetchone()[0]

        conexao.close()

        return resultado

    def contar_manutencao(self):

        conexao = sqlite3.connect(self.banco)
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM ativos
            WHERE status = 'MANUTENCAO'
        """)

        resultado = cursor.fetchone()[0]

        conexao.close()

        return resultado

    def contar_criticos(self):

        conexao = sqlite3.connect(self.banco)
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM ativos
            WHERE status = 'CRITICO'
        """)

        resultado = cursor.fetchone()[0]

        conexao.close()

        return resultado

#=====
#VIEW
#=====

class DashboardView:

    def __init__(self, janela):

        self.janela = janela

        # ----------------------------------------------------
        # Configurações da janela
        # ----------------------------------------------------

        self.janela.title(
            "Painel de Controle - Gestão de Ativos Corporativos (EAM)"
        )

        self.janela.geometry("500x350")

        self.janela.resizable(False, False)

        self.janela.configure(
            bg="#0f172a"
        )

        self.centralizar_janela()

        # Cria a interface
        self.criar_interface()

    def centralizar_janela(self):

        largura = 500
        altura = 350

        largura_tela = self.janela.winfo_screenwidth()
        altura_tela = self.janela.winfo_screenheight()

        pos_x = (largura_tela - largura) // 2
        pos_y = (altura_tela - altura) // 2

        self.janela.geometry(
            f"{largura}x{altura}+{pos_x}+{pos_y}"
        )

    def criar_interface(self):

        # ====================================================
        # TÍTULO
        # ====================================================

        titulo = tk.Label(
            self.janela,
            text="Painel de Controle - Gestão de Ativos Corporativos (EAM)",
            font=("Arial", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )

        titulo.pack(
            pady=(18, 12)
        )

        # ====================================================
        # ÁREA DOS KPIs
        # ====================================================

        frame_kpis = tk.Frame(
            self.janela,
            bg="#0f172a"
        )

        frame_kpis.pack(
            padx=20,
            pady=5
        )

        # ----------------------------------------------------
        # Cartão 1 - Total
        # ----------------------------------------------------

        self.criar_cartao(
            frame_kpis,
            "TOTAL DE EQUIPAMENTOS",
            0,
            0
        )

        # ----------------------------------------------------
        # Cartão 2 - Em operação
        # ----------------------------------------------------

        self.criar_cartao(
            frame_kpis,
            "EM OPERAÇÃO",
            0,
            1
        )

        # ----------------------------------------------------
        # Cartão 3 - Manutenção
        # ----------------------------------------------------

        self.criar_cartao(
            frame_kpis,
            "MANUTENÇÃO PREVENTIVA",
            1,
            0
        )

        # ----------------------------------------------------
        # Cartão 4 - Críticos
        # ----------------------------------------------------

        self.criar_cartao(
            frame_kpis,
            "EQUIPAMENTOS CRÍTICOS",
            1,
            1
        )

        # ====================================================
        # STATUS OPERACIONAL
        # ====================================================

        self.lbl_status = tk.Label(
            self.janela,
            text="Status operacional: aguardando dados...",
            font=("Arial", 10, "bold"),
            bg="#0f172a",
            fg="white"
        )

        self.lbl_status.pack(
            pady=(12, 5)
        )

        # ====================================================
        # RODAPÉ
        # ====================================================

        rodape = tk.Label(
            self.janela,
            text="Sistema EAM • Banco de dados SQLite • Arquitetura MVC",
            font=("Arial", 8),
            bg="#0f172a",
            fg="#94a3b8"
        )

        rodape.pack(
            pady=(5, 0)
        )

    # --------------------------------------------------------
    # Cria um cartão de KPI
    # --------------------------------------------------------

    def criar_cartao(
        self,
        pai,
        titulo,
        linha,
        coluna
    ):

        cartao = tk.Frame(
            pai,
            bg="#1e293b",
            height=100,
            highlightthickness=1,
            highlightbackground="#334155"
        )

        cartao.grid(
            row=linha,
            column=coluna,
            padx=6,
            pady=6,
            sticky="nsew"
        )

        pai.columnconfigure(0, weight=1)
        pai.columnconfigure(1, weight=1)

        # ----------------------------------------------------
        # Título do cartão
        # ----------------------------------------------------

        label_titulo = tk.Label(
            cartao,
            text=titulo,
            font=("Arial", 8, "bold"),
            bg="#1e293b",
            fg="#cbd5e1"
        )

        label_titulo.pack(
            pady=(10, 2)
        )

        # ----------------------------------------------------
        # Número do cartão
        # ----------------------------------------------------

        label_valor = tk.Label(
            cartao,
            text="0",
            font=("Arial", 25, "bold"),
            bg="#1e293b",
            fg="white"
        )

        label_valor.pack()

        # ----------------------------------------------------
        # Guarda a referência do Label
        # ----------------------------------------------------

        if "TOTAL" in titulo:
            self.lbl_total = label_valor

        elif "OPERAÇÃO" in titulo:
            self.lbl_operacao = label_valor

        elif "MANUTENÇÃO" in titulo:
            self.lbl_manutencao = label_valor

        elif "CRÍTICOS" in titulo:
            self.lbl_criticos = label_valor

    # --------------------------------------------------------
    # Atualiza os números dos KPIs
    # --------------------------------------------------------

    def atualizar_kpis(
        self,
        total,
        operacao,
        manutencao,
        criticos
    ):

        self.lbl_total.config(
            text=str(total)
        )

        self.lbl_operacao.config(
            text=str(operacao)
        )

        self.lbl_manutencao.config(
            text=str(manutencao)
        )

        self.lbl_criticos.config(
            text=str(criticos)
        )

        # Atualiza o status
        self.lbl_status.config(
            text="Status operacional: monitoramento ativo"
        )

#===========
#CONTROLLER
#===========

class DashboardController:

    def __init__(
        self,
        model,
        view
    ):

        self.model = model
        self.view = view

        # Atualiza o dashboard
        self.atualizar_dashboard()

    def atualizar_dashboard(self):

        # Busca os KPIs no banco
        total = self.model.contar_total()

        operacao = self.model.contar_operacao()

        manutencao = self.model.contar_manutencao()

        criticos = self.model.contar_criticos()

        # Envia os resultados para a View
        self.view.atualizar_kpis(
            total,
            operacao,
            manutencao,
            criticos
        )

if __name__ == "__main__":

    # --------------------------------------------------------
    # Cria a janela principal
    # --------------------------------------------------------

    janela = tk.Tk()

    # --------------------------------------------------------
    # Cria o Model
    # --------------------------------------------------------

    model = AtivoModel()

    # --------------------------------------------------------
    # Cria a View
    # --------------------------------------------------------

    view = DashboardView(
        janela
    )

    # --------------------------------------------------------
    # Cria o Controller
    # --------------------------------------------------------

    controller = DashboardController(
        model,
        view
    )

    # --------------------------------------------------------
    # Mantém a aplicação aberta
    # --------------------------------------------------------

    janela.mainloop()
