import re
from tkinter import messagebox

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_telefone(telefone):
    return re.match(r"^\d{8,15}$", telefone)

def erro(msg):
    messagebox.showerror("Erro", msg)

def info(msg):
    messagebox.showinfo("Informação", msg)

def confirmar(msg):
    from tkinter import messagebox
    return messagebox.askyesno("Confirmação", msg)
