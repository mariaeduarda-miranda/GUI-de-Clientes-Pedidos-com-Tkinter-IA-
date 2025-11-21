import tkinter as tk
from tkinter import messagebox
import models


class DashboardView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        tk.Label(self, text="Dashboard Gerencial", font=("Arial", 18, "bold")).pack(pady=(0, 20))

        # Container dos Cartões
        frame_cards = tk.Frame(self)
        frame_cards.pack(fill=tk.X)

        # Variáveis (StringVar)
        self.var_clientes = tk.StringVar(value="Carregando...")
        self.var_pedidos = tk.StringVar(value="Carregando...")
        self.var_ticket = tk.StringVar(value="Carregando...")

        # --- CHAMADAS DA FUNÇÃO ---
        # Ordem dos argumentos: (parent, titulo, variavel, cor_bg)
        self.criar_card(frame_cards, "Total Clientes", self.var_clientes, "#E3F2FD")
        self.criar_card(frame_cards, "Pedidos (Mês)", self.var_pedidos, "#E0F7FA")
        self.criar_card(frame_cards, "Ticket Médio", self.var_ticket, "#FFF8E1")

        # Botão Atualizar
        btn = tk.Button(self, text="Atualizar Dados", command=self.atualizar_dados,
                        bg="#42A5F5", fg="white", font=("Arial", 11, "bold"))
        btn.pack(pady=30, ipadx=10)

        # Inicializa os dados
        self.atualizar_dados(mostrar_msg=False)

    # --- DEFINIÇÃO DA FUNÇÃO ---
    # AQUI ESTAVA O PROBLEMA PROVÁVEL: A ordem deve ser (variavel, cor_bg)
    def criar_card(self, parent, titulo, variavel, cor_bg):

        # Cria o frame do cartão usando 'cor_bg' para o fundo
        card = tk.Frame(parent, bg=cor_bg, bd=2, relief=tk.GROOVE)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, ipady=10)

        # Rótulo do Título
        lbl_titulo = tk.Label(card, text=titulo, bg=cor_bg, font=("Arial", 10, "bold"), fg="#555")
        lbl_titulo.pack(pady=(10, 5))

        # Rótulo do Valor (usa 'variavel' no textvariable)
        lbl_valor = tk.Label(card, textvariable=variavel, bg=cor_bg, font=("Arial", 20, "bold"), fg="#000")
        lbl_valor.pack(pady=(0, 10))

    def atualizar_dados(self, mostrar_msg=True):
        try:
            # Busca dados no banco (models.py)
            t_cli, t_ped, t_med = models.get_dashboard_stats()

            # Atualiza as variáveis da tela
            self.var_clientes.set(str(t_cli))
            self.var_pedidos.set(str(t_ped))
            self.var_ticket.set(f"R$ {t_med:.2f}")

            if mostrar_msg:
                messagebox.showinfo("Dashboard", "Dados atualizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")