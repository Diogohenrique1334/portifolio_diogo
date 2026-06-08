"""Configuração do agente de trajetória.

Lê credenciais e parâmetros de variáveis de ambiente (`.env`) com fallback para
`st.secrets` (Streamlit Cloud). Nenhum segredo é hardcoded.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


def _get(chave: str, default: str | None = None) -> str | None:
    """Lê uma configuração de env var; cai para st.secrets quando no Streamlit.

    Procura tanto a chave em MAIÚSCULAS (env) quanto em minúsculas (convenção do
    secrets.toml do Streamlit Cloud).
    """
    valor = os.getenv(chave)
    if valor:
        return valor
    try:  # st.secrets só existe dentro do runtime do Streamlit
        import streamlit as st

        if chave in st.secrets:
            return st.secrets[chave]
        if chave.lower() in st.secrets:
            return st.secrets[chave.lower()]
    except Exception:
        pass
    return default


@dataclass
class AgenteConfig:
    """Parâmetros do agente. Instancie com ``AgenteConfig()`` para ler do ambiente."""

    openai_api_key: str | None = field(default_factory=lambda: _get("OPENAI_API_KEY"))
    database_url: str | None = field(default_factory=lambda: _get("DATABASE_URL"))
    # Integração opcional com o banco do projeto Diagnóstico (Neon).
    diagnostico_db_url: str | None = field(
        default_factory=lambda: _get("DIAGNOSTICO_DATABASE_URL")
    )
    # Allowlist de empresas seguras para expor EM DETALHE (acadêmico/hobby).
    # Tudo que não estiver aqui — inclusive empresa desconhecida — vira só agregado.
    diagnostico_empresas_detalhe: str = field(
        default_factory=lambda: _get("DIAGNOSTICO_EMPRESAS_DETALHE", "") or ""
    )
    modelo_chat: str = field(
        default_factory=lambda: _get("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    )
    modelo_embedding: str = field(
        default_factory=lambda: _get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )
    dimensao_embedding: int = field(
        default_factory=lambda: int(_get("EMBEDDING_DIM", "1536"))
    )
    top_k: int = 4
    max_chars_pergunta: int = 300
    temperatura: float = 0.2
    max_perguntas_sessao: int = 15

    @property
    def configurado(self) -> bool:
        """True quando há chave OpenAI e URL do banco — pré-requisito para rodar."""
        return bool(self.openai_api_key and self.database_url)

    @staticmethod
    def _libpq(url: str | None) -> str | None:
        """Normaliza uma URL Postgres para libpq (psycopg2).

        Remove o sufixo de driver async (``+asyncpg``) e traduz o parâmetro de SSL do
        estilo asyncpg (``ssl=require``/``ssl=true``) para o do libpq (``sslmode=...``).
        """
        if not url:
            return None
        from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

        for driver in ("+asyncpg", "+psycopg2", "+psycopg"):
            url = url.replace(driver, "")

        partes = urlsplit(url)
        if partes.query:
            params = dict(parse_qsl(partes.query, keep_blank_values=True))
            if "ssl" in params and "sslmode" not in params:
                valor = params.pop("ssl").lower()
                params["sslmode"] = (
                    "require" if valor in ("true", "require", "1", "yes") else valor
                )
            partes = partes._replace(query=urlencode(params))
        return urlunsplit(partes)

    def db_url_libpq(self) -> str | None:
        """URL libpq do banco de embeddings (pgvector)."""
        return self._libpq(self.database_url)

    def diagnostico_url_libpq(self) -> str | None:
        """URL libpq do banco do Diagnóstico (ou None se não configurado)."""
        return self._libpq(self.diagnostico_db_url)

    def empresas_detalhe(self) -> set[str]:
        """Conjunto (lowercase) de empresas liberadas para exposição detalhada."""
        return {
            e.strip().lower()
            for e in self.diagnostico_empresas_detalhe.split(",")
            if e.strip()
        }
