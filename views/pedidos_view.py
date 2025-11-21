import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import models


class PedidosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botão para criar novo pedido
        tk.Button(self, text="Novo Pedido", command=self.abrir_criacao_pedido).pack(pady=20)

        tk.Label(self, text="Para visualizar pedidos, implemente a listagem aqui").pack()

    def abrir_criacao_pedido(self):
        CriarPedidoWindow(self)


class CriarPedidoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title("Novo Pedido")
        self.geometry("500x400")

        # Seleção de Cliente
        frame_top = tk.Frame(self)
        frame_top.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_top, text="Cliente:").pack(side=tk.LEFT)

        # Carregar clientes para o Combobox
        self.clientes_map = {f"{c[1]} ({c[0]})": c[0] for c in models.listar_clientes()}
        self.cb_clientes = ttk.Combobox(frame_top, values=list(self.clientes_map.keys()))
        self.cb_clientes.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Label(frame_top, text="Data:").pack(side=tk.LEFT)
        self.entry_data = tk.Entry(frame_top, width=10)
        self.entry_data.insert(0, str(date.today()))
        self.entry_data.pack(side=tk.LEFT)

        # Adicionar Itens
        frame_item = tk.LabelFrame(self, text="Adicionar Produto")
        frame_item.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_item, text="Produto:").grid(row=0, column=0)
        self.entry_prod = tk.Entry(frame_item)
        self.entry_prod.grid(row=0, column=1)

        tk.Label(frame_item, text="Qtd:").grid(row=0, column=2)
        self.entry_qtd = tk.Entry(frame_item, width=5)
        self.entry_qtd.grid(row=0, column=3)

        tk.Label(frame_item, text="Preço:").grid(row=0, column=4)
        self.entry_preco = tk.Entry(frame_item, width=8)
        self.entry_preco.grid(row=0, column=5)

        tk.Button(frame_item, text="+", command=self.add_item).grid(row=0, column=6, padx=5)

        # Lista de Itens (Treeview temporária)
        self.tree = ttk.Treeview(self, columns=("Produto", "Qtd", "Preco", "Subtotal"), show="headings", height=5)
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Qtd", text="Qtd")
        self.tree.heading("Preco", text="Preço Unit.")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10)

        # Total
        self.lbl_total = tk.Label(self, text="Total: R$ 0.00", font=("Arial", 12, "bold"))
        self.lbl_total.pack(pady=5)

        # Ação Final
        tk.Button(self, text="Finalizar Pedido", command=self.salvar_pedido, bg="#dddddd").pack(pady=10)

        self.itens_temporarios = []

    def add_item(self):
        prod = self.entry_prod.get()
        try:
            qtd = int(self.entry_qtd.get())
            preco = float(self.entry_preco.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Preço devem ser números.")
            return

        if not prod:
            messagebox.showerror("Erro", "Nome do produto obrigatório.")
            return

        subtotal = qtd * preco
        self.itens_temporarios.append((prod, qtd, preco))
        self.tree.insert("", tk.END, values=(prod, qtd, f"{preco:.2f}", f"{subtotal:.2f}"))
        self.atualizar_total()

        # Limpar campos
        self.entry_prod.delete(0, tk.END)
        self.entry_qtd.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_prod.focus()

    def atualizar_total(self):
        total = sum(i[1] * i[2] for i in self.itens_temporarios)
        self.lbl_total.config(text=f"Total: R$ {total:.2f}")

    def salvar_pedido(self):
        cliente_str = self.cb_clientes.get()
        if cliente_str not in self.clientes_map:
            messagebox.showerror("Erro", "Selecione um cliente válido.")
            return
        if not self.itens_temporarios:
            messagebox.showerror("Erro", "O pedido precisa de pelo menos um item.")
            return

        cliente_id = self.clientes_map[cliente_str]
        data_ped = self.entry_data.get()
        total = sum(i[1] * i[2] for i in self.itens_temporarios)

        try:
            models.salvar_pedido_completo(cliente_id, data_ped, total, self.itens_temporarios)
            messagebox.showinfo("Sucesso", "Pedido salvo com sucesso!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")