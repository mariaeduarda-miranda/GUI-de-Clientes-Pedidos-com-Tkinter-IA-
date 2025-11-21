import tkinter as tk
from tkinter import ttk, scrolledtext  # Importante para rolagem
import threading
import models
import utils


class AnaliseIAView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        tk.Label(self, text="Análise de Inteligência Artificial (Local)", font=("Arial", 14, "bold")).pack(pady=10)

        # Instrução
        lbl_info = tk.Label(self, text="Certifique-se de que o Ollama está rodando no seu PC.", fg="gray")
        lbl_info.pack()

        # Botão
        self.btn_analisar = tk.Button(self, text="⚡ Analisar Pedidos com Ollama",
                                      command=self.iniciar_analise,
                                      bg="#42A5F5", fg="white", font=("Arial", 11))
        self.btn_analisar.pack(pady=10)

        # Área de Texto com Rolagem (ScrolledText)
        self.txt_resultado = scrolledtext.ScrolledText(self, width=70, height=20, font=("Consolas", 10))
        self.txt_resultado.pack(fill=tk.BOTH, expand=True, pady=10)

    def iniciar_analise(self):
        # Desabilita botão para evitar cliques duplos
        self.btn_analisar.config(state=tk.DISABLED, text="Processando... Aguarde...")
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END,
                                  "⏳ Coletando dados e enviando para o Ollama...\nIsso pode levar alguns segundos dependendo da sua GPU/CPU.\n")

        # Thread para não travar a janela
        threading.Thread(target=self.processar, daemon=True).start()

    def processar(self):
        # 1. Busca dados detalhados (com itens) no banco
        texto_dados = models.get_dados_para_analise_ia(limite=5)

        if not texto_dados:
            self.atualizar_gui("Nenhum pedido encontrado para analisar.")
            return

        # 2. Envia para o Ollama (utils.py)
        resultado = utils.analisar_pedidos_ia(texto_dados)

        # 3. Mostra resultado
        self.atualizar_gui(resultado)
        utils.log_acao("Análise de IA concluída")

    def atualizar_gui(self, texto):
        # Reabilita o botão e mostra o texto
        self.btn_analisar.config(state=tk.NORMAL, text="⚡ Analisar Pedidos com Ollama")
        self.txt_resultado.insert(tk.END, "\n" + "=" * 40 + "\n")
        self.txt_resultado.insert(tk.END, texto)
        self.txt_resultado.see(tk.END)  # Rola para o final