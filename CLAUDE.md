# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

Portfolio project by Diogo Oliveira (Data Scientist at Claro SA). This repo is new and may start empty — use the conventions below when building out the project.

Diogo's published portfolio: https://www.datascienceportfol.io/diogohenrique1334

---

## Standard Stack

All of Diogo's projects share a common stack. Default to these unless the task requires otherwise:

**Backend:** FastAPI + Uvicorn, SQLAlchemy 2.0 (async), Alembic, Pydantic 2.x, PostgreSQL (Neon Cloud)  
**Frontend:** Streamlit, streamlit-echarts, Plotly  
**Data/ML:** pandas, numpy, scikit-learn, statsmodels  
**Config:** python-dotenv with `.env` file (never hardcode secrets)  
**Deployment:** Render (backend), Streamlit Community Cloud (frontend)

---

## Architecture Pattern

All projects use a layered backend structure:

```
backend/
  main.py          # entry point / ingestion pipelines
  app.py           # Streamlit dashboard OR FastAPI app
  config.py        # settings loaded from .env
  database.py      # SQLAlchemy async engine and session
  models/          # SQLAlchemy ORM models
  repository/      # DB queries (no business logic)
  services/        # business logic (calls repository)
  agents/          # LLM or external API integrations
frontend/
  Page.py          # main Streamlit page
  pages/           # additional Streamlit pages
```

Keep responsibilities separated: routes call services, services call repositories, repositories call the DB.

---

## Baltazar Library

Diogo's personal utility library is installed in all projects. Import from it instead of reinventing utilities.

**Path:** `c:\Users\User\OneDrive - Claro SA\Área de Trabalho\notebook Dell\Diogo Coisas pessoais\Projetos\baltazar`  
**Install:** `pip install -e <path_to_baltazar>`

Key modules:
- `baltazar.funcoes_data_frames` — DataFrame reading and transformations
- `baltazar.ML` — data prep, regression, clustering, time series
- `baltazar.graficos.graficos_streamlit` — ECharts wrappers for Streamlit
- `baltazar.CX_PME` — Telecom/CX domain logic

---

## Running Projects (Typical Commands)

```bash
# Streamlit frontend
streamlit run Home.py

# Access admin panel (with password)
# First, set PORTFOLIO_ADMIN_PASSWORD environment variable or add to .env
# http://localhost:8501/Admin
```

---

## Admin Panel

**Pages:** `pages/3_Admin.py` — painel protegido por senha para editar projetos, experiências e perfil.

**Configuração local:**
1. Copie `.env.example` para `.env`
2. Defina `PORTFOLIO_ADMIN_PASSWORD=sua_senha` no `.env`
3. Abra `http://localhost:8501/Admin` após iniciar o Streamlit

**Configuração Streamlit Cloud:**
1. No dashboard Streamlit Cloud, vá a Settings → Secrets
2. Adicione:
```toml
portfolio_admin_password = "sua_senha_secreta"
```
3. A página Admin ficará acessível apenas com a senha

**Dados dinâmicos:**
- `data/perfil.json` — nome, cargo, tagline, links
- `data/projetos.json` — lista de projetos (4 projetos padrão)
- `data/experiencias.json` — experiências profissionais, formação, certificações
- Todos os dados podem ser editados via painel admin (com backup automático)

---

## Code Style

- **Modular architecture:** extract logic into separate modules/functions; never collapse responsibilities into a single large file.
- **snake_case** for all Python identifiers.
- **Docstrings** on all public functions.
- No hardcoded paths — use parameters or `config.py` variables loaded from `.env`.
- Async SQLAlchemy patterns (use `async with session` and `await` consistently).
