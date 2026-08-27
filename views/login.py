import tkinter as tk
from cardapio import Cardapio
# em outro arquivo, ex: main.py ou menu principal
root = tk.Tk()
# ... outros widgets do menu principal ...

def abrir_cardapio():
    Cardapio(root)

btn = tk.Button(root, text="Abrir Cardápio", command=abrir_cardapio)
btn.pack()

root.mainloop()