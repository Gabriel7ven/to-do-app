# Keep Notes App

Este é um aplicativo web simples de notas autoadesivas criado com Python e Flask.

## Visão geral

Este projeto permite que usuários se registrem, façam login e gerenciem notas/tarefas pessoais.

Principais recursos:
- Cadastro de usuário
- Autenticação com login e logout
- Criação, edição e exclusão de notas autoadesivas
- Interface de usuário com templates Jinja2
- Armazenamento de dados utilizando PostgreSQL no Neon

## Tecnologias usadas

- Python
- Flask
- PostgreSQL
- Jinja2
- Werkzeug (para hashing de senha)

## Estrutura do projeto

- `todolist/`
  - `__init__.py` - fábrica do app Flask e registro de blueprints
  - `auth.py` - rotas e lógica de autenticação
  - `notes.py` - rotas e lógica de criação/edição/exclusão de tarefas
  - `wsgi.py` - inicializa a aplicação Flask para execução em produção (Vercel/Gunicorn) 
  - `templates/` - templates HTML
    - `base.html` - template base comum
    - `auth/` - páginas de login e registro
    - `notes/` - páginas de lista, criação e edição de tarefas
  - `static/` - arquivos estáticos como CSS e imagens
  - `models/` - modelos de dados da aplicação (SQLAlchemy)
  - `migrations/` - histórico das migrações do banco de dados
  - `README.md` - documentação do projeto, contendo informações sobre instalação, uso e estrutura da aplicação.
  - `requirements.txt` - lista das dependências Python necessárias para executar o projeto.
  - `vercel.json` - configuração de deploy da aplicação na Vercel.

## Instalação

1. Clone o repositório em sua máquina local (o baixe os arquivos)

```powershell
git clone https://github.com/Gabriel7ven/keep-notes.git
cd keep-notes
```

2. Crie e ative um ambiente virtual

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências necessárias :

```powershell
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto contendo:

```env
DATABASE_URL=sua_url_do_neon
SECRET_KEY=sua_chave_secreta
```

5. Execute as migrações

```bash
cd todolist
flask --app . db upgrade
```

6. Execute a aplicação

```bash
flask --app . run
```

O aplicativo estará disponível em `http://127.0.0.1:5000/`.

## Uso

1. Acesse `http://127.0.0.1:5000/`.
2. Cadastre um novo usuário em `/auth/register`.
3. Faça login em `/auth/login`.
4. Crie, atualize e exclua notas na página principal.




## Rotas principais

- `/auth/register` - registro de novos usuários
- `/auth/login` - formulário de login
- `/auth/logout` - logout do usuário
- `/` - lista de tarefas do usuário autenticado
- `/create` - criar nova tarefa
- `/<id>/update` - editar tarefa existente
- `/<id>/delete` - excluir tarefa (POST)


## Licença

Sinta-se à vontade para adaptar o projeto para uso pessoal ou estudo.

