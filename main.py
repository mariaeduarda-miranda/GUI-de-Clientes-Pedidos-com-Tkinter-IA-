import tkinter as tk
from tkinter import ttk, messagebox
import db
from views.clientes_view import ClientesView
from views.pedidos_view import PedidosView
from views.dashboard_view import DashboardView
from views.relatorios_view import RelatoriosView
from views.ia_view import AnaliseIAView
from views.logs_view import LogsView
import utils


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Clientes e Pedidos")
        self.geometry("900x650")

        db.init_db()
        utils.log_acao("Sistema iniciado")

        self.criar_menu()

        # Notebook (Abas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Inicializar Views
        self.dash_view = DashboardView(self.notebook)
        self.cli_view = ClientesView(self.notebook)
        self.ped_view = PedidosView(self.notebook)
        self.rel_view = RelatoriosView(self.notebook)
        self.ia_view = AnaliseIAView(self.notebook)
        self.log_view = LogsView(self.notebook)

        # Adicionar Abas
        self.notebook.add(self.dash_view, text="Dashboard")
        self.notebook.add(self.cli_view, text="Clientes")
        self.notebook.add(self.ped_view, text="Pedidos")
        self.notebook.add(self.rel_view, text="Relatórios")
        self.notebook.add(self.ia_view, text="IA / Análise")
        self.notebook.add(self.log_view, text="Logs")

        # Protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_menu(self):
        menubar = tk.Menu(self)

        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menu_arquivo.add_command(label="Sair", command=self.ao_fechar)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Menu Navegação (atalhos para abas)
        menu_nav = tk.Menu(menubar, tearoff=0)
        menu_nav.add_command(label="Dashboard", command=lambda: self.notebook.select(0))
        menu_nav.add_command(label="Clientes", command=lambda: self.notebook.select(1))
        menu_nav.add_command(label="Pedidos", command=lambda: self.notebook.select(2))
        menubar.add_cascade(label="Navegação", menu=menu_nav)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=lambda: messagebox.showinfo("Sobre", "Sistema Fase 2"))
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=menubar)

    def ao_fechar(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            utils.log_acao("Sistema encerrado")
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()