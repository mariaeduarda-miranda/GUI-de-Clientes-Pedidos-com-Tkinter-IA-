import tkinter as tk
from db import init_db
from views.clientes_view import ClientesFrame
from views.pedidos_view import PedidosFrame

def main():
    init_db()
    root = tk.Tk()
    root.title("Gestão de Clientes e Pedidos")

    menu = tk.Menu(root)
    root.config(menu=menu)

    cad_menu = tk.Menu(menu, tearoff=0)
    cad_menu.add_command(label="Clientes", command=lambda: ClientesFrame(root))
    cad_menu.add_command(label="Pedidos", command=lambda: PedidosFrame(root))
    menu.add_cascade(label="Cadastros", menu=cad_menu)

    ClientesFrame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
