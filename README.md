
# Auth API - Django + JWT

API de autenticação construída com Django Rest Framework e JWT, com documentação automática via Swagger. Permite cadastro, login e consulta dos dados do usuário autenticado.

---

## 🚀 Deploy

A API está disponível publicamente em:

- https://auth-api-django-snowy-violet-9818.fly.dev/swagger/

---

## 📌 Endpoints

### 🔐 POST `/signup/`  
Cria um novo usuário.

#### Requisição
```json
{
  "email": "usuario@email.com",
  "nome": "Nome do Usuário",
  "password": "Senha123!",
  "password2": "Senha123!"
}
```

#### Resposta (201)
```json
{
  "email": "usuario@email.com",
  "nome": "Nome do Usuário"
}
```

---

### 🔑 POST `/login/`  
Autentica um usuário e retorna tokens JWT.

#### Requisição
```json
{
  "email": "usuario@email.com",
  "password": "Senha123!"
}
```

#### Resposta (200)
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh...",
  "access": "eyJ0eXAiOiJKV1QiLCJhb..."
}
```

---

### 👤 GET `/me/`  
Retorna os dados do usuário autenticado.

#### Cabeçalhos
```
Authorization: Bearer <access_token>
```

#### Resposta (200)
```json
{
  "email": "usuario@email.com",
  "nome": "Nome do Usuário"
}
```

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11
- Django 5.x
- Django REST Framework
- Simple JWT (JSON Web Token)
- drf-yasg (Swagger)
- Fly.io (Deploy)

---

## ⚙️ Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Rode o servidor de desenvolvimento
python manage.py runserver
```

---

## 🧪 Testes

Para rodar os testes automatizados da API, use o seguinte comando:

```bash
python manage.py test
```

