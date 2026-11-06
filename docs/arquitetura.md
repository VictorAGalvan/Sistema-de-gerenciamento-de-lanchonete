### 2.1. Arquitetura em camadas inspirada em MVC
 
O projeto tenta replicar as ideias do MVC (Model-View-Controller) dentro de uma arquitetura em camadas. A escolha faz sentido para o tamanho do projeto: o sistema não é extremamente complexo, mas tem volume de dados e de classes suficiente para exigir mais organização do que um único arquivo monolítico.
 
As camadas são:
 
- **Views** (`views/`): telas Tkinter. Criam os widgets, coletam entradas, exibem erros e resultados e encaminham eventos aos controllers de fluxo. Não acessam o banco nem aplicam regras de negócio diretamente.
- **Controllers** (`controler/`): fazem a ponte entre View, Model e DAO. Os controllers de fluxo (`login_controller.py`, `cardapio_view_controller.py`, `pedidos_view_controller.py`, `ingredientes_view_controller.py`, `cardapio_admin_controller.py` e `app_controller.py`) concentram validações, regras de negócio, navegação de sessão e operações do caso de uso; os controllers existentes por entidade encaminham as operações aos DAOs.
- **Models** (`models/`): classes de domínio puras (Pedido, ItensCardapio, Cliente, etc.), sem lógica de acesso a dados.
- **DAOs** (`dao/`): responsáveis pela leitura e escrita, seja em banco SQL, seja em memória (mock).
Essa divisão não é o MVC "de livro" (não há notificação automática de eventos entre Model e View, por exemplo). É uma arquitetura em camadas que reaproveita a separação de responsabilidades do MVC: Model guarda o estado do domínio, View mostra e recebe entrada do usuário, Controller decide o que fazer.
 
### 2.2. Padrão DAO (Data Access Object)
 
Cada entidade do domínio tem um DAO próprio (`ClienteDAO`, `PedidoDAO`, `ItensCardapioDAO`, etc.), com uma interface fixa: `select`, `selectID`, `insert`, `update`, `delete`, além de métodos específicos (`select_por_cardapio`, `select_nao_finalizados`, etc.).
 
O projeto tem duas implementações completas dessa interface:
 
- **Versão SQL** (branch `main`): usa SQLAlchemy sobre PostgreSQL.
- **Versão mock** (branch `add/interface`): guarda os dados em listas Python, em memória.
As duas implementações expõem os mesmos métodos. Isso permite trocar de uma para outra sem alterar Controller nem View — só o `import` do DAO muda. Essa é a vantagem central do padrão DAO/Repository: isolar o resto do sistema de como e onde os dados são guardados.
