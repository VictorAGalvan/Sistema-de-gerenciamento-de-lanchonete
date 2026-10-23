from controler.ingrediente_controler import Ingrediente_Controler
from database.conexao import inicializar_banco

try:
    inicializar_banco()
    controller = Ingrediente_Controler()
    ingredientes = controller.listar()
    print("id | ingrediente | nome | quantidade | unidade")
    for ingrediente in ingredientes:
        print(f"{ingrediente.id} | {ingrediente.nome} | {ingrediente.quantidade} | {ingrediente.unidade}")
except Exception as e:
    print(f"Error: {e}")


if "__main__" == __name__:
    from views.main import JanelaPrincipal
    app = JanelaPrincipal()
    app.mainloop()