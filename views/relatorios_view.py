import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date
import models
import utils

# Tenta importar reportlab, avisa se não tiver
try:
    from reportlab.pdfgen import canvas

    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class RelatoriosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Filtros
        frame_filtros = tk.LabelFrame(self, text="Filtros")
        frame_filtros.pack(fill=tk.X, pady=5)

        tk.Label(frame_filtros, text="Data Início (AAAA-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.entry_ini = tk.Entry(frame_filtros, width=12)
        self.entry_ini.insert(0, "2023-01-01")
        self.entry_ini.pack(side=tk.LEFT)

        tk.Label(frame_filtros, text="Data Fim:").pack(side=tk.LEFT, padx=5)
        self.entry_fim = tk.Entry(frame_filtros, width=12)
        self.entry_fim.insert(0, str(date.today()))
        self.entry_fim.pack(side=tk.LEFT)

        tk.Button(frame_filtros, text="Filtrar", command=self.buscar).pack(side=tk.LEFT, padx=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Data", "Total"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Total", text="Total")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botões de Exportação
        frame_export = tk.Frame(self)
        frame_export.pack(pady=10)
        tk.Button(frame_export, text="Exportar CSV", command=self.exportar_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_export, text="Exportar PDF", command=self.exportar_pdf).pack(side=tk.LEFT, padx=5)

    def buscar(self):
        ini = self.entry_ini.get()
        fim = self.entry_fim.get()
        self.dados_atuais = models.filtrar_pedidos(ini, fim)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in self.dados_atuais:
            self.tree.insert("", tk.END, values=p)

    def exportar_csv(self):
        if not hasattr(self, 'dados_atuais') or not self.dados_atuais:
            messagebox.showwarning("Aviso", "Sem dados para exportar.")
            return
        try:
            filename = "relatorio_pedidos.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Cliente", "Data", "Total"])
                writer.writerows(self.dados_atuais)
            utils.log_acao("Exportou CSV")
            messagebox.showinfo("Sucesso", f"CSV gerado: {filename}")
            os.startfile(filename) if os.name == 'nt' else None
        except Exception as e:
            utils.log_acao(f"Erro CSV: {e}")

    def exportar_pdf(self):
        if not HAS_REPORTLAB:
            messagebox.showerror("Erro", "Biblioteca 'reportlab' não instalada.")
            return
        if not hasattr(self, 'dados_atuais') or not self.dados_atuais:
            return

        try:
            filename = "relatorio_pedidos.pdf"
            c = canvas.Canvas(filename)
            c.drawString(100, 800, "Relatório de Pedidos")
            y = 780
            for p in self.dados_atuais:
                linha = f"Pedido #{p[0]} - {p[1]} - {p[2]} - R$ {p[3]:.2f}"
                c.drawString(100, y, linha)
                y -= 20
            c.save()
            utils.log_acao("Exportou PDF")
            messagebox.showinfo("Sucesso", f"PDF gerado: {filename}")
            os.startfile(filename) if os.name == 'nt' else None
        except Exception as e:
            utils.log_acao(f"Erro PDF: {e}")