# Portfólio · Diogo Oliveira

[![CI](https://github.com/Diogohenrique1334/portifolio_diogo/actions/workflows/ci.yml/badge.svg)](https://github.com/Diogohenrique1334/portifolio_diogo/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)

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
- **Assistente** — chat com IA (**RAG**) que responde perguntas sobre a trajetória, projetos e formação do Diogo, usando apenas o conteúdo do portfólio como fonte.
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
├── agente/               # Assistente da trajetória (RAG) — chat embutido no Home
│   ├── config.py         # Credenciais e parâmetros (.env / st.secrets)
│   ├── corpus.py         # JSONs de data/ → documentos textuais
│   ├── diagnostico.py    # Integração curada com o banco do Diagnóstico (Neon)
│   ├── embeddings.py     # Wrapper de embeddings OpenAI
│   ├── vector_store.py   # Índice pgvector no Postgres Neon
│   ├── indexador.py      # (Re)constrói o índice (offline)
│   ├── retrieval.py      # Pergunta → trechos relevantes
│   ├── seguranca.py      # Validação, rate limit, perguntas sugeridas
│   └── agente.py         # Orquestra retrieval + LLM → resposta + fontes
├── utils/                # Componentes e helpers
│   ├── sidebar.py        # Sidebar compartilhada
│   ├── styles.py         # Injeção de CSS
│   ├── cards.py          # Cards de projeto
│   ├── tech_icons.py     # Badges de tecnologia
│   ├── assistente_widget.py # UI do chat RAG (renderizado no Home)
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

## 🤖 Assistente da Trajetória (RAG)

Chat embutido no **Home** (`Home.py` via `utils/assistente_widget.py`) que responde
perguntas sobre a carreira do Diogo. O
conteúdo dos JSONs de `data/` é transformado em documentos (`agente/corpus.py`),
embeddado (OpenAI) e indexado no **pgvector** (Postgres Neon). A cada pergunta, os
trechos mais relevantes são recuperados e enviados ao LLM, que responde **usando
apenas esse contexto** — e a interface mostra as fontes usadas.

> **Nota de design:** o corpus é pequeno (cabe inteiro em contexto). O RAG aqui é uma
> **demonstração da técnica** — não uma necessidade. A escolha é assumida de propósito.

**Padrão técnico:** retrieval semântico (RAG), correto para conteúdo textual. *(Para o
agente de gastos do projeto Finanças, dado estruturado, o padrão é outro: tool calling.)*

### Configuração

1. No `.env` (ou em *Secrets* do Streamlit Cloud), defina:
   - `OPENAI_API_KEY` — chave OpenAI (embeddings + chat)
   - `DATABASE_URL` — Postgres Neon (aceita URL libpq; sufixo `+asyncpg` é removido)
   - *(opcional)* `OPENAI_CHAT_MODEL`, `OPENAI_EMBEDDING_MODEL`, `EMBEDDING_DIM`
2. Construa o índice (uma vez, e sempre que editar o conteúdo):
   ```bash
   python -m agente.indexador
   ```
3. Abra a página **Assistente** no app.

Se as credenciais não estiverem configuradas ou o índice não existir, a página exibe
uma instrução amigável em vez de quebrar.

### Integração opcional com o Diagnóstico (curada)

O agente pode ser enriquecido com a trajetória de execução (50+ projetos) vinda do
banco do projeto **Diagnóstico** (Neon). A segurança é por **allowlist**
(`agente/diagnostico.py`):

- Projetos cuja `empresa` estiver em `DIAGNOSTICO_EMPRESAS_DETALHE` são expostos **em
  detalhe** (acadêmico/hobby). Todo o resto — inclusive empresa desconhecida/nova —
  entra **apenas em forma agregada** (contagens, tempo médio, frequência de skills),
  **sem** nomes, clientes, e-mails ou texto livre. Dado profissional/Claro nunca vaza
  por omissão (*fail-safe*).
- **Antes de indexar, audite** o que será exposto:
  ```bash
  python -m agente.diagnostico   # relatório: empresas → modo (detalhe/agregado)
  ```
- Configure `DIAGNOSTICO_DATABASE_URL` e `DIAGNOSTICO_EMPRESAS_DETALHE` no `.env`. Se a
  URL ficar vazia, a integração é simplesmente ignorada.

### Proteções (agente público)

- Limite de tamanho da pergunta e **rate limit por sessão** (`agente/seguranca.py`).
- **Perguntas sugeridas** para guiar o uso e reduzir chamadas aleatórias.
- O system prompt restringe o escopo e resiste a *prompt injection*.

---

## 📦 Deploy

O portfólio é publicado no **Streamlit Community Cloud**, apontando para `Home.py` como entry point. A senha do admin é configurada via *Secrets* do dashboard do Streamlit Cloud.

---

## 📄 Licença

Projeto pessoal de portfólio. Sinta-se à vontade para se inspirar na estrutura. 🙂
