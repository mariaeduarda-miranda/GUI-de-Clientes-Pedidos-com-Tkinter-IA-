import tkinter as tk
from tkinter import messagebox
import os


class LogsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_top = tk.Frame(self)
        frame_top.pack(fill=tk.X)

        tk.Button(frame_top, text="Atualizar Logs", command=self.carregar_logs).pack(side=tk.LEFT)
        tk.Button(frame_top, text="Limpar Histórico", command=self.limpar_logs, fg="red").pack(side=tk.RIGHT)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        self.carregar_logs()

    def carregar_logs(self):
        self.listbox.delete(0, tk.END)
        if os.path.exists('logs/app.log'):
            with open('logs/app.log', 'r') as f:
                linhas = f.readlines()
                for l in reversed(linhas):  # Mostrar mais recentes primeiro
                    self.listbox.insert(tk.END, l.strip())

    def limpar_logs(self):
        if messagebox.askyesno("Confirmar", "Deseja apagar todo o histórico?"):
            with open('logs/app.log', 'w') as f:
                f.write("")
            self.carregar_logs()