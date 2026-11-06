from database.conexao import inicializar_banco

inicializar_banco()

if "__main__" == __name__:
    from views.main import JanelaPrincipal
    app = JanelaPrincipal()
    app.mainloop()