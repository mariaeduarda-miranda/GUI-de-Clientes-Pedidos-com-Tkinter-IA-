import tkinter as tk
from tkinter import ttk, messagebox
import models  # Para interagir com o banco de dados
import utils  # Para validações e logs


# =================================================================
# 1. JANELA DE CADASTRO/EDIÇÃO (ClienteFormView) - Contém Salvar/Cancelar
# =================================================================

class ClienteFormView(tk.Toplevel):
    """Janela modal para cadastro e edição de clientes."""

    def __init__(self, parent, cliente_id=None, callback_recarregar=None):
        super().__init__(parent)
        self.transient(parent)  # Mantém a janela no topo
        self.grab_set()  # Torna a janela modal
        self.title("Cadastro de Cliente" if cliente_id is None else "Editar Cliente")
        self.geometry("400x250")

        self.cliente_id = cliente_id
        self.callback_recarregar = callback_recarregar

        if self.cliente_id:
            self.carregar_dados(self.cliente_id)

        # Adiciona protocolo para fechar a janela
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def create_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campos de Entrada (Nome, E-mail, Telefone)
        tk.Label(main_frame, text="Nome:").pack(fill=tk.X, pady=(5, 0))
        self.entry_nome = tk.Entry(main_frame)
        self.entry_nome.pack(fill=tk.X)

        tk.Label(main_frame, text="E-mail:").pack(fill=tk.X, pady=(5, 0))
        self.entry_email = tk.Entry(main_frame)
        self.entry_email.pack(fill=tk.X)

        tk.Label(main_frame, text="Telefone:").pack(fill=tk.X, pady=(5, 0))
        self.entry_telefone = tk.Entry(main_frame)
        self.entry_telefone.pack(fill=tk.X)

        # --- FRAME DOS BOTÕES ---
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)

        # Botão Salvar (com a cor de ação primária)
        btn_salvar = tk.Button(button_frame, text="Salvar", command=self.salvar_cliente,
                               bg="#42A5F5", fg="white", padx=10, font=("Arial", 10, "bold"))
        btn_salvar.pack(side=tk.RIGHT, padx=5)

        # Botão Cancelar
        btn_cancelar = tk.Button(button_frame, text="Cancelar", command=self.destroy, padx=10, font=("Arial", 10))
        btn_cancelar.pack(side=tk.RIGHT)

    def carregar_dados(self, cliente_id):
        try:
            cliente = models.get_cliente(cliente_id)
            if cliente:
                self.entry_nome.insert(0, cliente[1])
                self.entry_email.insert(0, cliente[2])
                self.entry_telefone.insert(0, cliente[3])
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados do cliente: {e}")
            utils.log_acao(f"Erro ao carregar dados do cliente ID {cliente_id}: {e}")

    def salvar_cliente(self):
        """Método que valida os campos e salva ou atualiza no banco de dados."""
        # 1. Obtenção e Limpeza dos Dados
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()

        # 2. VALIDAÇÃO

        # Nome (Obrigatório e válido)
        nome_valido, nome_erro = utils.validar_nome(nome)
        if not nome_valido:
            messagebox.showerror("Erro de Validação", nome_erro)
            return

        # E-mail (Formato correto se preenchido)
        email_valido, email_erro = utils.validar_email(email)
        if not email_valido:
            messagebox.showerror("Erro de Validação", email_erro)
            return

        # Telefone (8-15 dígitos se preenchido)
        telefone_valido, telefone_erro = utils.validar_telefone(telefone)
        if not telefone_valido:
            messagebox.showerror("Erro de Validação", telefone_erro)
            return

        # 3. SALVAR/ATUALIZAR (Lógica de Banco de Dados)
        try:
            if self.cliente_id:
                # Edição
                models.atualizar_cliente(self.cliente_id, nome, email, telefone)
                utils.log_acao(f"Cliente ID {self.cliente_id} editado: {nome}")
                messagebox.showinfo("Sucesso", "Cliente atualizado!")
            else:
                # Novo Cadastro
                models.inserir_cliente(nome, email, telefone)
                utils.log_acao(f"Cliente novo cadastrado: {nome}")
                messagebox.showinfo("Sucesso", "Cliente cadastrado!")

            if self.callback_recarregar:
                self.callback_recarregar()

            self.destroy()

        except Exception as e:
            utils.log_acao(f"ERRO ao salvar cliente: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o cliente: {e}")


# =================================================================
# 2. FRAME PRINCIPAL DE LISTAGEM (ClientesView) - Contém a Treeview e Botões CRUD
# =================================================================

class ClientesView(tk.Frame):
    """Frame principal da aba Clientes, com busca e Treeview."""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_widgets()  # Chamada para criar os widgets desta classe (Busca e Treeview)
        self.carregar_clientes()  # Carrega os dados ao iniciar

    def create_widgets(self):
        # Variáveis e Widgets de Busca
        self.var_busca = tk.StringVar()

        frame_busca = tk.Frame(self)
        frame_busca.pack(fill=tk.X, pady=5)

        tk.Label(frame_busca, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        entry_busca = tk.Entry(frame_busca, textvariable=self.var_busca)
        entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        entry_busca.bind('<Return>', lambda event: self.carregar_clientes())

        btn_filtrar = tk.Button(frame_busca, text="Filtrar", command=self.carregar_clientes)
        btn_filtrar.pack(side=tk.LEFT)

        # Treeview para listar clientes
        colunas = ("ID", "Nome", "Email", "Telefone")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        for col in colunas:
            self.tree.heading(col, text=col)
            # Ajuste de Largura das Colunas
            if col == "ID":
                self.tree.column(col, width=50, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=150, anchor=tk.W)

        # Frame de Botões (Novo/Editar/Excluir)
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(frame_botoes, text="Novo Cliente", command=self.abrir_formulario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Editar Cliente", command=self.editar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Excluir Cliente", command=self.excluir_cliente).pack(side=tk.LEFT, padx=5)

    def carregar_clientes(self):
        # Limpa a Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        termo_busca = self.var_busca.get()
        # Assumindo que models.get_todos_clientes(termo) existe
        clientes = models.get_todos_clientes(termo_busca)

        for cli in clientes:
            self.tree.insert("", tk.END, values=cli)

    def abrir_formulario(self):
        """Abre a janela ClienteFormView para um NOVO cliente."""
        ClienteFormView(self.master, callback_recarregar=self.carregar_clientes)

    def editar_cliente(self):
        """Abre a janela ClienteFormView para EDIÇÃO do cliente selecionado."""
        selecionado = self.tree.focus()
        if selecionado:
            cliente_id = self.tree.item(selecionado, 'values')[0]
            ClienteFormView(self.master, cliente_id=cliente_id, callback_recarregar=self.carregar_clientes)
        else:
            messagebox.showwarning("Seleção", "Selecione um cliente para editar.")

    def excluir_cliente(self):
        """Exclui o cliente selecionado após confirmação."""
        selecionado = self.tree.focus()
        if selecionado:
            valores = self.tree.item(selecionado, 'values')
            cliente_id = valores[0]
            nome_cliente = valores[1]

            if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o cliente '{nome_cliente}'?"):
                try:
                    models.excluir_cliente(cliente_id)
                    utils.log_acao(f"Cliente ID {cliente_id} excluído: {nome_cliente}")
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")
                    self.carregar_clientes()
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao excluir cliente: {e}")
                    utils.log_acao(f"Erro ao excluir cliente ID {cliente_id}: {e}")
        else:
            messagebox.showwarning("Seleção", "Selecione um cliente para excluir.")

    def carregar_clientes(self):
        try:
            # Limpa a Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            termo_busca = self.var_busca.get()
            # ASSUMIMOS QUE models.get_todos_clientes(termo) está definido em models.py
            clientes = models.get_todos_clientes(termo_busca)

            for cli in clientes:
                self.tree.insert("", tk.END, values=cli)

        except Exception as e:
            # Garante que qualquer falha na busca (como um problema de DB)
            # não derrube a aplicação.
            messagebox.showerror("Erro ao Carregar Clientes", f"Ocorreu um erro ao buscar dados: {e}")
            utils.log_acao(f"ERRO CRÍTICO ao carregar clientes: {e}")