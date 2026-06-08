"""Utilitário de administração do banco do agente (uso pontual, fora do runtime).

Cria/rotaciona um papel **read-only** restrito à tabela ``trajetoria_embeddings`` —
a credencial que o app público (Streamlit Cloud) deve usar no ``DATABASE_URL``. Assim,
mesmo que a secret vaze, ela não alcança outras tabelas (ex.: dados do Diagnóstico) nem
escreve nada.

Uso (a partir da raiz do projeto, com a credencial DONA no .env):

    python -m agente.admin_db
"""

from __future__ import annotations

import re
import secrets
from urllib.parse import urlsplit, urlunsplit

import psycopg2

from agente.config import AgenteConfig

_ROLE = "portfolio_ro"
_TABELA = "trajetoria_embeddings"


def _validar_identificador(nome: str) -> str:
    """Garante que um identificador SQL (vindo da URL) é simples e seguro."""
    if not re.fullmatch(r"[A-Za-z0-9_-]+", nome):
        raise ValueError(f"Identificador inesperado/inseguro: {nome!r}")
    return nome


def _montar_url(base: str, usuario: str, senha: str) -> str:
    """Reconstrói a URL trocando apenas usuário/senha (mantém host, db e query)."""
    p = urlsplit(base)
    porta = f":{p.port}" if p.port else ""
    return urlunsplit(p._replace(netloc=f"{usuario}:{senha}@{p.hostname}{porta}"))


def criar_usuario_readonly(cfg: AgenteConfig | None = None, role: str = _ROLE) -> str:
    """Cria/atualiza o papel read-only e retorna a URL pronta para o app público."""
    cfg = cfg or AgenteConfig()
    owner = cfg.db_url_libpq()
    if not owner:
        raise RuntimeError("DATABASE_URL (dona) não configurada no .env.")

    dbname = _validar_identificador(urlsplit(owner).path.lstrip("/"))
    role = _validar_identificador(role)
    senha = secrets.token_urlsafe(24)

    conn = psycopg2.connect(owner)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (role,))
            existe = cur.fetchone()
            if existe:
                # Apenas rotaciona a senha — alterar atributos (NOSUPERUSER) exigiria
                # superusuário; os atributos já foram fixados na criação.
                cur.execute(f"ALTER ROLE {role} PASSWORD %s;", (senha,))
            else:
                opcoes = "LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT"
                cur.execute(f"CREATE ROLE {role} {opcoes} PASSWORD %s;", (senha,))

            cur.execute(f"GRANT CONNECT ON DATABASE {dbname} TO {role};")
            cur.execute(f"GRANT USAGE ON SCHEMA public TO {role};")
            cur.execute(f"REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {role};")
            cur.execute(f"GRANT SELECT ON public.{_TABELA} TO {role};")
    finally:
        conn.close()

    return _montar_url(owner, role, senha)


def verificar(url_readonly: str) -> None:
    """Prova a blindagem: lê os embeddings (ok) e é barrado em ``clientes`` (esperado)."""
    conn = psycopg2.connect(url_readonly)
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {_TABELA};")
            print(f"  ✅ leu {_TABELA}: {cur.fetchone()[0]} linhas")
        conn.rollback()
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM clientes;")
                print(f"  ❌ LEU clientes ({cur.fetchone()[0]}) — restrição FALHOU!")
            except psycopg2.Error as e:
                conn.rollback()
                print(f"  ✅ bloqueado em clientes (esperado): {str(e).splitlines()[0]}")
    finally:
        conn.close()


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv()
    url = criar_usuario_readonly()
    print(f"Papel '{_ROLE}' criado/atualizado e restrito a '{_TABELA}'.")
    print("\nVerificando blindagem:")
    verificar(url)
    print("\n=== DATABASE_URL para o app público (Streamlit Cloud Secrets) ===")
    print(url)
    print("\n⚠️  Guarde esta URL com segurança (contém a senha do papel read-only).")


if __name__ == "__main__":
    main()
