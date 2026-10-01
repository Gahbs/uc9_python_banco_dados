import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# MODEL - BANCO DE DADOS E OPERAÇÕES SQL
# ============================================================

class FuncionarioModel:

    def __init__(self, banco="hrms.db"):
        self.banco = banco
        self.criar_tabela()

    def conectar(self):
        return sqlite3.connect(self.banco)

    def criar_tabela(self):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                cargo TEXT NOT NULL,
                departamento TEXT NOT NULL,
                trabalho TEXT NOT NULL
            )
        """)

        conexao.commit()
        conexao.close()

    def inserir(
        self,
        matricula,
        nome,
        cargo,
        departamento,
        trabalho
    ):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO funcionarios
            (matricula, nome, cargo, departamento, trabalho)
            VALUES (?, ?, ?, ?, ?)
        """, (
            matricula,
            nome,
            cargo,
            departamento,
            trabalho
        ))

        conexao.commit()
        conexao.close()

    def listar(self, filtro=""):
        conexao = self.conectar()
        cursor = conexao.cursor()

        if filtro:
            cursor.execute("""
                SELECT
                    id,
                    matricula,
                    nome,
                    cargo,
                    departamento,
                    trabalho
                FROM funcionarios
                WHERE matricula LIKE ?
                   OR nome LIKE ?
                   OR cargo LIKE ?
                   OR departamento LIKE ?
                ORDER BY id DESC
            """, (
                f"%{filtro}%",
                f"%{filtro}%",
                f"%{filtro}%",
                f"%{filtro}%"
            ))

        else:
            cursor.execute("""
                SELECT
                    id,
                    matricula,
                    nome,
                    cargo,
                    departamento,
                    trabalho
                FROM funcionarios
                ORDER BY id DESC
            """)

        dados = cursor.fetchall()

        conexao.close()

        return dados

    def atualizar(
        self,
        id_funcionario,
        matricula,
        nome,
        cargo,
        departamento,
        trabalho
    ):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE funcionarios
            SET matricula = ?,
                nome = ?,
                cargo = ?,
                departamento = ?,
                trabalho = ?
            WHERE id = ?
        """, (
            matricula,
            nome,
            cargo,
            departamento,
            trabalho,
            id_funcionario
        ))

        conexao.commit()
        conexao.close()

    def excluir(self, id_funcionario):
        conexao = self.conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            DELETE FROM funcionarios
            WHERE id = ?
        """, (id_funcionario,))

        conexao.commit()
        conexao.close()


# ============================================================
# CONTROLLER - REGRAS E VALIDAÇÕES
# ============================================================

class FuncionarioController:

    def __init__(self):
        self.model = FuncionarioModel()

    def validar(
        self,
        matricula,
        nome,
        cargo,
        departamento,
        trabalho
    ):
        matricula = matricula.strip()
        nome = nome.strip()
        cargo = cargo.strip()

        if not matricula:
            return False, "Informe a matrícula."

        if not nome:
            return False, "Informe o nome completo."

        if not cargo:
            return False, "Informe o cargo/função."

        if not departamento:
            return False, "Selecione o departamento."

        if not trabalho:
            return False, "Selecione o tipo de trabalho."

        if len(matricula) < 3:
            return False, "A matrícula deve possuir pelo menos 3 caracteres."

        return True, "Dados válidos."

    def cadastrar(
        self,
        matricula,
        nome,
        cargo,
        departamento,
        trabalho
    ):
        valido, mensagem = self.validar(
            matricula,
            nome,
            cargo,
            departamento,
            trabalho
        )

        if not valido:
            return False, mensagem

        try:
            self.model.inserir(
                matricula.strip(),
                nome.strip(),
                cargo.strip(),
                departamento,
                trabalho
            )

            return True, "Funcionário cadastrado com sucesso."

        except sqlite3.IntegrityError:
            return False, "Essa matrícula já está cadastrada."

        except Exception as erro:
            return False, f"Erro ao cadastrar: {erro}"

    def listar(self, filtro=""):
        return self.model.listar(filtro)

    def atualizar(
        self,
        id_funcionario,
        matricula,
        nome,
        cargo,
        departamento,
        trabalho
    ):
        valido, mensagem = self.validar(
            matricula,
            nome,
            cargo,
            departamento,
            trabalho
        )

        if not valido:
            return False, mensagem

        try:
            self.model.atualizar(
                id_funcionario,
                matricula.strip(),
                nome.strip(),
                cargo.strip(),
                departamento,
                trabalho
            )

            return True, "Funcionário atualizado com sucesso."

        except sqlite3.IntegrityError:
            return False, "Essa matrícula já pertence a outro funcionário."

        except Exception as erro:
            return False, f"Erro ao atualizar: {erro}"

    def excluir(self, id_funcionario):
        try:
            self.model.excluir(id_funcionario)

            return True, "Funcionário excluído com sucesso."

        except Exception as erro:
            return False, f"Erro ao excluir: {erro}"


# ============================================================
# VIEW - JANELA PRINCIPAL
# ============================================================

class JanelaPrincipal:

    def __init__(self, janela, controller):

        self.janela = janela
        self.controller = controller

        self.janela.title(
            "HRMS - Gestão de Funcionários"
        )

        self.janela.geometry(
            "700x450"
        )

        self.janela.resizable(
            False,
            False
        )

        self.janela.configure(
            bg="#0f172a"
        )

        self.centralizar()
        self.configurar_estilo()
        self.criar_interface()

    def centralizar(self):

        largura = 700
        altura = 450

        tela_largura = self.janela.winfo_screenwidth()
        tela_altura = self.janela.winfo_screenheight()

        x = (tela_largura - largura) // 2
        y = (tela_altura - altura) // 2

        self.janela.geometry(
            f"{largura}x{altura}+{x}+{y}"
        )

    def configurar_estilo(self):

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background="#1e293b",
            foreground="white",
            fieldbackground="#1e293b",
            rowheight=30,
            borderwidth=0
        )

        estilo.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", "#2563eb")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

    def criar_interface(self):

        titulo = tk.Label(
            self.janela,
            text="HRMS",
            font=("Arial", 28, "bold"),
            bg="#0f172a",
            fg="white"
        )

        titulo.pack(
            pady=(55, 5)
        )

        subtitulo = tk.Label(
            self.janela,
            text="Sistema de Gestão de Funcionários",
            font=("Arial", 12),
            bg="#0f172a",
            fg="#94a3b8"
        )

        subtitulo.pack(
            pady=(0, 35)
        )

        frame_menu = tk.Frame(
            self.janela,
            bg="#1e293b",
            padx=30,
            pady=30
        )

        frame_menu.pack(
            padx=100,
            fill="x"
        )

        titulo_menu = tk.Label(
            frame_menu,
            text="Gestão de Funcionários",
            font=("Arial", 15, "bold"),
            bg="#1e293b",
            fg="white"
        )

        titulo_menu.pack(
            pady=(0, 20)
        )

        botao_gestao = tk.Button(
            frame_menu,
            text="Abrir Gestão Completa",
            command=self.abrir_gestao,
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            height=2
        )

        botao_gestao.pack(
            fill="x",
            pady=5
        )

        botao_sair = tk.Button(
            frame_menu,
            text="Fechar Sistema",
            command=self.janela.destroy,
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            height=2
        )

        botao_sair.pack(
            fill="x",
            pady=5
        )

    def abrir_gestao(self):

        JanelaGestaoDB(
            self.janela,
            self.controller
        )


# ============================================================
# VIEW - GESTÃO COMPLETA / CRUD
# ============================================================

class JanelaGestaoDB:

    def __init__(self, principal, controller):

        self.controller = controller
        self.id_selecionado = None

        self.janela = tk.Toplevel(principal)

        self.janela.title(
            "Gestão Completa - Funcionários"
        )

        self.janela.geometry(
            "1100x650"
        )

        self.janela.resizable(
            False,
            False
        )

        self.janela.configure(
            bg="#0f172a"
        )

        self.centralizar()
        self.criar_interface()
        self.carregar_tabela()

    def centralizar(self):

        largura = 1100
        altura = 650

        tela_largura = self.janela.winfo_screenwidth()
        tela_altura = self.janela.winfo_screenheight()

        x = (tela_largura - largura) // 2
        y = (tela_altura - altura) // 2

        self.janela.geometry(
            f"{largura}x{altura}+{x}+{y}"
        )

    def criar_interface(self):

        titulo = tk.Label(
            self.janela,
            text="Gestão Completa de Funcionários",
            font=("Arial", 21, "bold"),
            bg="#0f172a",
            fg="white"
        )

        titulo.pack(
            pady=(20, 3)
        )

        subtitulo = tk.Label(
            self.janela,
            text="Cadastro, edição, exclusão e consulta",
            font=("Arial", 10),
            bg="#0f172a",
            fg="#94a3b8"
        )

        subtitulo.pack(
            pady=(0, 15)
        )

        frame_form = tk.Frame(
            self.janela,
            bg="#1e293b",
            padx=20,
            pady=15
        )

        frame_form.pack(
            padx=25,
            fill="x"
        )

        self.criar_campo(
            frame_form,
            "Matrícula",
            0,
            0
        )

        self.criar_campo(
            frame_form,
            "Nome",
            0,
            2
        )

        self.criar_campo(
            frame_form,
            "Cargo",
            1,
            0
        )

        tk.Label(
            frame_form,
            text="Departamento",
            font=("Arial", 9, "bold"),
            bg="#1e293b",
            fg="white"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=5
        )

        self.departamento = ttk.Combobox(
            frame_form,
            values=[
                "TI & Sistemas",
                "Recursos Humanos",
                "Operações & Logística",
                "Financeiro",
                "Marketing"
            ],
            state="readonly",
            width=23
        )

        self.departamento.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        tk.Label(
            frame_form,
            text="Trabalho",
            font=("Arial", 9, "bold"),
            bg="#1e293b",
            fg="white"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        self.trabalho = ttk.Combobox(
            frame_form,
            values=[
                "Presencial",
                "Híbrido",
                "Remoto"
            ],
            state="readonly",
            width=23
        )

        self.trabalho.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        botoes = tk.Frame(
            frame_form,
            bg="#1e293b"
        )

        botoes.grid(
            row=2,
            column=2,
            columnspan=2,
            pady=8
        )

        tk.Button(
            botoes,
            text="Novo / Limpar",
            command=self.limpar_formulario,
            bg="#475569",
            fg="white",
            relief="flat",
            width=14,
            height=2
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            botoes,
            text="Salvar",
            command=self.salvar,
            bg="#2563eb",
            fg="white",
            relief="flat",
            width=14,
            height=2
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            botoes,
            text="Excluir",
            command=self.excluir,
            bg="#dc2626",
            fg="white",
            relief="flat",
            width=14,
            height=2
        ).pack(
            side="left",
            padx=3
        )

        frame_filtro = tk.Frame(
            self.janela,
            bg="#0f172a"
        )

        frame_filtro.pack(
            padx=25,
            pady=15,
            fill="x"
        )

        tk.Label(
            frame_filtro,
            text="Pesquisar:",
            font=("Arial", 10, "bold"),
            bg="#0f172a",
            fg="white"
        ).pack(
            side="left"
        )

        self.filtro = tk.Entry(
            frame_filtro,
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=45
        )

        self.filtro.pack(
            side="left",
            padx=10,
            ipady=5
        )

        self.filtro.bind(
            "<KeyRelease>",
            self.filtrar
        )

        tk.Button(
            frame_filtro,
            text="Atualizar",
            command=self.carregar_tabela,
            bg="#16a34a",
            fg="white",
            relief="flat",
            width=14,
            height=2
        ).pack(
            side="left",
            padx=5
        )

        frame_tabela = tk.Frame(
            self.janela,
            bg="#0f172a"
        )

        frame_tabela.pack(
            padx=25,
            fill="both",
            expand=True
        )

        colunas = (
            "id",
            "matricula",
            "nome",
            "cargo",
            "departamento",
            "trabalho"
        )

        self.tabela = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        self.tabela.heading(
            "id",
            text="ID"
        )

        self.tabela.heading(
            "matricula",
            text="Matrícula"
        )

        self.tabela.heading(
            "nome",
            text="Nome"
        )

        self.tabela.heading(
            "cargo",
            text="Cargo"
        )

        self.tabela.heading(
            "departamento",
            text="Departamento"
        )

        self.tabela.heading(
            "trabalho",
            text="Trabalho"
        )

        self.tabela.column(
            "id",
            width=50,
            anchor="center"
        )

        self.tabela.column(
            "matricula",
            width=110,
            anchor="center"
        )

        self.tabela.column(
            "nome",
            width=220
        )

        self.tabela.column(
            "cargo",
            width=170
        )

        self.tabela.column(
            "departamento",
            width=200
        )

        self.tabela.column(
            "trabalho",
            width=110,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            frame_tabela,
            orient="vertical",
            command=self.tabela.yview
        )

        self.tabela.configure(
            yscrollcommand=scrollbar.set
        )

        self.tabela.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_funcionario
        )

    def criar_campo(
        self,
        frame,
        texto,
        linha,
        coluna
    ):

        tk.Label(
            frame,
            text=texto,
            font=("Arial", 9, "bold"),
            bg="#1e293b",
            fg="white"
        ).grid(
            row=linha,
            column=coluna,
            sticky="w",
            padx=5,
            pady=5
        )

        entrada = tk.Entry(
            frame,
            bg="#334155",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=25
        )

        entrada.grid(
            row=linha,
            column=coluna + 1,
            padx=5,
            pady=5,
            ipady=4
        )

        if texto == "Matrícula":
            self.matricula = entrada

        elif texto == "Nome":
            self.nome = entrada

        elif texto == "Cargo":
            self.cargo = entrada

    def carregar_tabela(self):

        filtro = self.filtro.get()

        dados = self.controller.listar(
            filtro
        )

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for funcionario in dados:

            self.tabela.insert(
                "",
                tk.END,
                values=funcionario
            )

    def filtrar(self, evento=None):

        self.carregar_tabela()

    def selecionar_funcionario(self, evento=None):

        selecionado = self.tabela.selection()

        if not selecionado:
            return

        valores = self.tabela.item(
            selecionado[0],
            "values"
        )

        if not valores:
            return

        self.id_selecionado = valores[0]

        self.matricula.delete(
            0,
            tk.END
        )

        self.matricula.insert(
            0,
            valores[1]
        )

        self.nome.delete(
            0,
            tk.END
        )

        self.nome.insert(
            0,
            valores[2]
        )

        self.cargo.delete(
            0,
            tk.END
        )

        self.cargo.insert(
            0,
            valores[3]
        )

        self.departamento.set(
            valores[4]
        )

        self.trabalho.set(
            valores[5]
        )

    def salvar(self):

        if self.id_selecionado is None:

            sucesso, mensagem = self.controller.cadastrar(
                self.matricula.get(),
                self.nome.get(),
                self.cargo.get(),
                self.departamento.get(),
                self.trabalho.get()
            )

        else:

            sucesso, mensagem = self.controller.atualizar(
                self.id_selecionado,
                self.matricula.get(),
                self.nome.get(),
                self.cargo.get(),
                self.departamento.get(),
                self.trabalho.get()
            )

        if sucesso:

            messagebox.showinfo(
                "Sucesso",
                mensagem,
                parent=self.janela
            )

            self.limpar_formulario()
            self.carregar_tabela()

        else:

            messagebox.showerror(
                "Erro",
                mensagem,
                parent=self.janela
            )

    def excluir(self):

        if self.id_selecionado is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um funcionário para excluir.",
                parent=self.janela
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este funcionário?",
            parent=self.janela
        )

        if not confirmar:
            return

        sucesso, mensagem = self.controller.excluir(
            self.id_selecionado
        )

        if sucesso:

            messagebox.showinfo(
                "Sucesso",
                mensagem,
                parent=self.janela
            )

            self.limpar_formulario()
            self.carregar_tabela()

        else:

            messagebox.showerror(
                "Erro",
                mensagem,
                parent=self.janela
            )

    def limpar_formulario(self):

        self.id_selecionado = None

        self.matricula.delete(
            0,
            tk.END
        )

        self.nome.delete(
            0,
            tk.END
        )

        self.cargo.delete(
            0,
            tk.END
        )

        self.departamento.set("")
        self.trabalho.set("")

        self.tabela.selection_remove(
            self.tabela.selection()
        )


# ============================================================
# EXECUÇÃO DO PROGRAMA
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    controller = FuncionarioController()

    app = JanelaPrincipal(
        root,
        controller
    )

    root.mainloop()