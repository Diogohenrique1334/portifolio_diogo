# Portfólio · Diogo Oliveira

Portfólio pessoal em **Streamlit** de Diogo Oliveira — Cientista de Dados. Uma aplicação web multipágina que apresenta projetos, currículo, certificações e artigos, com um **painel administrativo protegido por senha** para edição dinâmica de todo o conteúdo (sem precisar mexer no código).

🌐 **Portfólio online:** [datascienceportfol.io/diogohenrique1334](https://www.datascienceportfol.io/diogohenrique1334)
💼 [LinkedIn](https://www.linkedin.com/in/diogooliveira1334/) · 🐙 [GitHub](https://github.com/Diogohenrique1334)

---

## ✨ Funcionalidades

- **Home** — apresentação, métricas agregadas (projetos, tecnologias, anos de experiência) e badges de habilidades técnicas.
- **Projetos** — cards interativos com descrição, stack, métricas de impacto e links para GitHub.
- **Currículo** — experiências profissionais, formação e download do CV em PDF.
- **Certificações** — certificados e cursos concluídos.
- **Artigos** — publicações e conteúdos técnicos.
- **Admin** — painel protegido por senha para editar projetos, experiências, perfil e artigos, com **backup automático** dos dados a cada alteração.

Todo o conteúdo é servido a partir de arquivos JSON em [`data/`](data/), editáveis pela interface admin.

---

## 🧱 Stack

| Camada | Tecnologias |
|---|---|
| **App** | Streamlit (multipágina), HTML/CSS customizado |
| **Dados** | Arquivos JSON versionados em `data/` |
| **Config** | `python-dotenv` (`.env`) |
| **Imagens** | Pillow |
| **Containerização** | Docker + Docker Compose |
| **Deploy** | Streamlit Community Cloud |

---

## 📁 Estrutura

```
portifolio_diogo/
├── Home.py               # Página inicial (entry point)
├── pages/                # Páginas do app (multipágina nativa do Streamlit)
│   ├── 1_Projetos.py
│   ├── 2_Curriculo.py
│   ├── 3_Certificacoes.py
│   ├── 4_Artigos.py
│   └── 5_Admin.py        # Painel protegido por senha
├── utils/                # Componentes e helpers
│   ├── sidebar.py        # Sidebar compartilhada
│   ├── styles.py         # Injeção de CSS
│   ├── cards.py          # Cards de projeto
│   ├── tech_icons.py     # Badges de tecnologia
│   └── admin_helpers.py  # Lógica do painel admin (backup, persistência)
├── data/                 # Conteúdo dinâmico (JSON)
│   ├── perfil.json
│   ├── projetos.json
│   ├── experiencias.json
│   └── artigos.json
├── assets/               # Foto, CV e imagens dos projetos
├── .streamlit/           # Tema do Streamlit
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🚀 Como rodar localmente

**Pré-requisitos:** Python 3.12+

```bash
# 1. Clone o repositório
git clone https://github.com/Diogohenrique1334/portifolio_diogo.git
cd portifolio_diogo

# 2. (Opcional) crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o ambiente
cp .env.example .env           # e defina PORTFOLIO_ADMIN_PASSWORD

# 5. Rode o app
streamlit run Home.py
```

O app fica disponível em **http://localhost:8501**.

---

## 🐳 Como rodar com Docker

A imagem usa `python:3.12-slim`, roda como **usuário não-root** e tem **healthcheck** no endpoint nativo do Streamlit.

```bash
# Suba a aplicação (build + run)
docker compose up --build

# Em background
docker compose up -d --build

# Derrube
docker compose down
```

Acesse **http://localhost:8501**.

> O `PORTFOLIO_ADMIN_PASSWORD` é lido em runtime via `env_file: .env` — nunca é embutido na imagem. Copie `.env.example` para `.env` antes de subir.

Sem Compose, manualmente:

```bash
docker build -t portfolio-diogo .
docker run -p 8501:8501 --env-file .env portfolio-diogo
```

---

## 🔐 Painel Admin

O painel em `pages/5_Admin.py` permite editar todo o conteúdo do portfólio pela interface, com backup automático a cada alteração.

**Local:** defina `PORTFOLIO_ADMIN_PASSWORD` no `.env` e acesse **http://localhost:8501/Admin**.

**Streamlit Cloud:** em *Settings → Secrets*, adicione:

```toml
portfolio_admin_password = "sua_senha_secreta"
```

---

## 📦 Deploy

O portfólio é publicado no **Streamlit Community Cloud**, apontando para `Home.py` como entry point. A senha do admin é configurada via *Secrets* do dashboard do Streamlit Cloud.

---

## 📄 Licença

Projeto pessoal de portfólio. Sinta-se à vontade para se inspirar na estrutura. 🙂
