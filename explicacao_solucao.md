# Solução: Sistema de Tickets e Orders 🎟️🛒

Olá! Aqui é o seu professor para te guiar pela resolução deste exercício. Nosso objetivo principal aqui é transformar um sistema de sessões de cinema simples em um sistema comercial completo, que suporta **usuários**, **pedidos (orders)** e **ingressos (tickets)**. 

Vamos analisar a solução passo a passo, entendendo _o quê_ foi feito e _por que_ foi feito.

---

## 1. Evoluindo nosso Banco de Dados (`db/models.py`)

Em um sistema de verdade, a modelagem de dados é o coração de tudo. Precisamos garantir que todos os dados estejam conectados e que as regras de negócio sejam seguidas *antes* mesmo de salvar no banco!

### 1.1 O Modelo Customizado de User
O Django já tem um usuário padrão (`django.contrib.auth.models.User`), mas a documentação do Django sempre recomenda criar um modelo de usuário próprio (`AbstractUser`) para facilitar futuras expansões do sistema (por exemplo, se um dia você quiser adicionar campos como `telefone` ou `cpf`).
Para isso, foi criado a classe `User(AbstractUser): pass`. Depois, nós avisamos ao Django para usá-lo através da configuração `AUTH_USER_MODEL = "db.User"` no arquivo `settings.py`.

### 1.2 Otimizando a Busca em `Movie`
O exercício pediu para adicionarmos um index no título dos filmes. 
**Por quê?** Pense no banco de dados como um dicionário de papel. Sem um índice (index), procurar por um filme chamado "Matrix" exigiria ler o dicionário inteiro página por página. Com o índice, o banco vai direto para a letra "M" e acha muito mais rápido.
*   **Como?** Adicionando `class Meta: indexes = [models.Index(fields=["title"])]`.

### 1.3 O Pedido (`Order`)
Cada compra feita por um usuário vira um **Pedido**. 
*   Adicionamos o `created_at` usando `auto_now_add=True` (assim o Django coloca a data e hora atual automaticamente quando o pedido nasce, sem a gente precisar se preocupar).
*   Fizemos uma relação (`ForeignKey`) com o usuário.
*   Na classe `Meta`, usamos `ordering = ["-created_at"]` para garantir que, ao buscar os pedidos de um cliente, os mais recentes (sinal de menos `-`) apareçam primeiro.

### 1.4 O Ingresso (`Ticket`) e suas Validações
Aqui está a regra de negócio mais crítica: **ninguém quer comprar uma cadeira que não existe!**
O ingresso faz a ponte entre uma Sessão (`movie_session`) e um Pedido (`order`).

*   **Validação customizada (`clean()`)**: Sobrescrevemos o método `clean()` do Django. Nele, checamos:
    1. A linha (`row`) informada existe dentro da sala de cinema (`cinema_hall.rows`)? E é maior ou igual a 1?
    2. A cadeira (`seat`) existe naquela linha (`cinema_hall.seats_in_row`)? E é maior ou igual a 1?
    Se tentar comprar a cadeira 50 em uma sala que só tem 20, o Django vai dar um grito (o famigerado `ValidationError`).
*   O método `save()` precisou ser estendido. Naturalmente, o `.save()` do Django não chama o `.clean()` automaticamente, a não ser que você mande (usando o `self.full_clean()`).
*   **Garantindo que a cadeira não foi comprada duas vezes**: Usamos a `UniqueConstraint` para o trio (`row`, `seat`, `movie_session`). Isso diz ao banco de dados: _"É proibido existir dois ingressos para a mesma cadeira na mesma sessão"_!

---

## 2. A Camada de Serviços (`services/`)

A camada de serviços é onde a "Mágica" ou "Lógica de Negócios" invisível atua, processando dados antes de manipular o banco de dados propriamente.

### 2.1 Criando Pedidos (`services/order.py`) com Atomicidade (`transaction.atomic`)
No método `create_order`, nós recebemos uma lista de ingressos selecionados. É aqui que usamos o **`@transaction.atomic`**.
*   **O problema:** Imagina se um cliente tenta comprar 5 ingressos. O sistema salva 4 deles com sucesso, mas no 5º o código "quebra" porque a cadeira já estava ocupada ou ocorreu uma falha de conexão. O cliente ficaria com uma compra pela metade? Isso seria um desastre!
*   **A solução:** A transação atômica (`atomic`) garante que o lema _"Ou vai tudo, ou não vai nada"_ seja cumprido. Se *qualquer* erro ocorrer ao salvar os tickets, toda a compra (incluindo o próprio pedido em si e ingressos parciais) é cancelada e revertida. Além disso, fizemos o mesmo em `create_movie` para garantir a operação.

### 2.2 Gerenciamento de Usuários (`services/user.py`)
No mundo web, senhas NUNCA devem ser salvas como texto puro ("1qazcde3"). Se um hacker vazar o banco de dados do cinema, todas as senhas estariam expostas.
* Ao invés de usar o clássico `User.objects.create(...)`, nós fomos espertos e usamos `.create_user()`. Esse método aplica uma função matemática chamada "hash", embaralhando a senha toda (ex: `$pbkdf2_sha256$260000...`) de forma irreversível. 
* O mesmo raciocínio foi usado na função `update_user` acionando o método `.set_password()`.

### 2.3 Saber Quem Pegou as Cadeiras (`services/movie_session.py`)
Por último, para plotar na tela as cadeiras, criamos o método `get_taken_seats(movie_session_id)`. Usando isso, o front-end poderia ver o mapa e desabilitar as cadeiras que a nossa query responder que já estão vendidas, evitando o usuário tentar comprar o que já era para o momento.

---
E aí, ficou mais claro como as peças do sistema se conectam? Agora, mão na massa e vamos para o código! 🚀
