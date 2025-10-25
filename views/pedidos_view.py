import tkinter as tk
from tkinter import ttk, filedialog
from datetime import date
import csv
from models import listar_clientes, inserir_pedido, listar_pedidos
from utils import erro, info
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class PedidosFrame(ttk.Frame):
    """Lista e filtra pedidos"""
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        self.carregar_pedidos()

    def criar_widgets(self):
        filtro_frame = ttk.Frame(self)
        filtro_frame.pack(fill="x", pady=5)

        ttk.Label(filtro_frame, text="De:").pack(side="left")
        self.var_ini = tk.StringVar()
        ttk.Entry(filtro_frame, textvariable=self.var_ini, width=10).pack(side="left", padx=2)
        ttk.Label(filtro_frame, text="Até:").pack(side="left")
        self.var_fim = tk.StringVar()
        ttk.Entry(filtro_frame, textvariable=self.var_fim, width=10).pack(side="left", padx=2)
        ttk.Button(filtro_frame, text="Filtrar", command=self.carregar_pedidos).pack(side="left", padx=5)

        botoes = ttk.Frame(self)
        botoes.pack(fill="x", pady=5)
        ttk.Button(botoes, text="Novo Pedido", command=self.novo_pedido).pack(side="left", padx=2)
        ttk.Button(botoes, text="Exportar CSV", command=lambda: self.exportar("csv")).pack(side="left", padx=2)
        ttk.Button(botoes, text="Exportar PDF", command=lambda: self.exportar("pdf")).pack(side="left", padx=2)

        self.tree = ttk.Treeview(self, columns=("id", "cliente", "data", "total"), show="headings")
        for c in ("id", "cliente", "data", "total"):
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True)

    def carregar_pedidos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        ini, fim = self.var_ini.get().strip(), self.var_fim.get().strip()
        pedidos = listar_pedidos(ini if ini else None, fim if fim else None)
        if pedidos:
            for p in pedidos:
                self.tree.insert("", "end", values=p)

    def novo_pedido(self):
        PedidoForm(self)

    def exportar(self, tipo):
        sel = self.tree.selection()
        if not sel:
            erro("Selecione um pedido para exportar.")
            return
        pedido = self.tree.item(sel[0])["values"]
        pedido_id, cliente, data, total = pedido

        if tipo == "csv":
            file = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV", "*.csv")])
            if not file:
                return
            with open(file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Pedido ID", "Cliente", "Data", "Total"])
                writer.writerow(pedido)
            info(f"Pedido exportado para {file}")

        elif tipo == "pdf":
            file = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF", "*.pdf")])
            if not file:
                return
            c = canvas.Canvas(file, pagesize=A4)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 800, "Resumo de Pedido")
            c.setFont("Helvetica", 12)
            c.drawString(100, 770, f"Pedido: {pedido_id}")
            c.drawString(100, 750, f"Cliente: {cliente}")
            c.drawString(100, 730, f"Data: {data}")
            c.drawString(100, 710, f"Total: R$ {total:.2f}")
            c.save()
            info(f"PDF salvo em {file}")
