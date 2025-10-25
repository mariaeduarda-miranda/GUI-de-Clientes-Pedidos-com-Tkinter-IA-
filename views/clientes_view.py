import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from models import listar_clientes, inserir_cliente, atualizar_cliente, excluir_cliente, obter_cliente
from utils import validar_email, validar_telefone, erro, info, confirmar

class ClientesFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        self.carregar_clientes()

    def criar_widgets(self):
        busca_frame = ttk.Frame(self)
        busca_frame.pack(fill="x", pady=5)

        ttk.Label(busca_frame, text="Buscar:").pack(side="left", padx=5)
        self.var_busca = tk.StringVar()
        self.entry_busca = ttk.Entry(busca_frame, textvariable=self.var_busca)
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(busca_frame, text="🔍", command=self.carregar_clientes).pack(side="left")

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=5)
        ttk.Button(botoes, text="Novo", command=self.novo_cliente).pack(side="left", padx=2)
        ttk.Button(botoes, text="Editar", command=self.editar_cliente).pack(side="left", padx=2)
        ttk.Button(botoes, text="Excluir", command=self.excluir_cliente).pack(side="left", padx=2)

        self.tree = ttk.Treeview(self, columns=("id", "nome", "email", "telefone"), show="headings")
        for col in ("id", "nome", "email", "telefone"):
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)

    def carregar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        filtro = self.var_busca.get()
        clientes = listar_clientes(filtro)
        if clientes:
            for c in clientes:
                self.tree.insert("", "end", values=c)

    def novo_cliente(self):
        ClienteForm(self, None, self.carregar_clientes)

    def editar_cliente(self):
        sel = self.tree.selection()
        if not sel:
            erro("Selecione um cliente.")
            return
        cid = self.tree.item(sel[0])["values"][0]
        ClienteForm(self, cid, self.carregar_clientes)

    def excluir_cliente(self):
        sel = self.tree.selection()
        if not sel:
            erro("Selecione um cliente.")
            return
        cid = self.tree.item(sel[0])["values"][0]
        if confirmar("Excluir cliente selecionado?"):
            excluir_cliente(cid)
            info("Cliente excluído.")
            self.carregar_clientes()


class ClienteForm(Toplevel):
    def __init__(self, master, cliente_id, callback):
        super().__init__(master)
        self.title("Cliente")
        self.cliente_id = cliente_id
        self.callback = callback
        self.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.criar_widgets()
        if cliente_id:
            self.carregar_dados()

    def criar_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Nome *").grid(row=0, column=0, sticky="w")
        self.nome = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nome).grid(row=0, column=1)

        ttk.Label(frame, text="Email").grid(row=1, column=0, sticky="w")
        self.email = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email).grid(row=1, column=1)

        ttk.Label(frame, text="Telefone").grid(row=2, column=0, sticky="w")
        self.telefone = tk.StringVar()
        ttk.Entry(frame, textvariable=self.telefone).grid(row=2, column=1)

        botoes = ttk.Frame(frame)
        botoes.grid(row=3, columnspan=2, pady=10)
        ttk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        ttk.Button(botoes, text="Cancelar", command=self.cancelar).pack(side="left")

    def carregar_dados(self):
        cliente = obter_cliente(self.cliente_id)
        if cliente:
            _, nome, email, telefone = cliente
            self.nome.set(nome)
            self.email.set(email)
            self.telefone.set(telefone)

    def salvar(self):
        nome, email, telefone = self.nome.get().strip(), self.email.get().strip(), self.telefone.get().strip()
        if not nome:
            erro("Nome é obrigatório.")
            return
        if email and not validar_email(email):
            erro("Email inválido.")
            return
        if telefone and not validar_telefone(telefone):
            erro("Telefone inválido (8–15 dígitos).")
            return
        if self.cliente_id:
            atualizar_cliente(self.cliente_id, nome, email, telefone)
        else:
            inserir_cliente(nome, email, telefone)
        info("Cliente salvo com sucesso!")
        self.callback()
        self.destroy()

    def cancelar(self):
        if messagebox.askokcancel("Cancelar", "Descartar alterações?"):
            self.destroy()
