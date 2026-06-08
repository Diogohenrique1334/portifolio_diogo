"""Índice vetorial em pgvector (Postgres Neon).

Cria a extensão e a tabela de embeddings, indexa os documentos e faz busca por
similaridade de cosseno. Mantém só o necessário — uma tabela única, chave textual
por documento, upsert idempotente.

As conexões são curtas e sempre fechadas (``contextlib.closing``): o app Streamlit
re-executa com frequência e o Neon limita conexões simultâneas.
"""

from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

import psycopg2
from pgvector.psycopg2 import register_vector

from agente.corpus import Documento

_TABELA = "trajetoria_embeddings"


@dataclass
class Trecho:
    """Resultado de uma busca: documento recuperado + distância (menor = mais perto)."""

    tipo: str
    titulo: str
    texto: str
    distancia: float


class PgVectorStore:
    """Acesso ao índice pgvector. Conexões são abertas por operação (curtas)."""

    def __init__(self, db_url: str, dimensao: int):
        self._db_url = db_url
        self._dimensao = dimensao

    def _conectar(self, registrar_vetor: bool = True):
        """Abre conexão. ``registrar_vetor`` registra o tipo vector do pgvector —
        deve ser False antes de a extensão existir (ex.: na criação do schema)."""
        conn = psycopg2.connect(self._db_url)
        if registrar_vetor:
            register_vector(conn)
        return conn

    def criar_schema(self) -> None:
        """Cria a extensão vector e a tabela de embeddings (idempotente).

        Conecta sem registrar o tipo vector, pois ele ainda pode não existir.
        """
        with closing(self._conectar(registrar_vetor=False)) as conn, conn:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                cur.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {_TABELA} (
                        id        TEXT PRIMARY KEY,
                        tipo      TEXT NOT NULL,
                        titulo    TEXT NOT NULL,
                        texto     TEXT NOT NULL,
                        embedding vector({self._dimensao}) NOT NULL
                    );
                    """
                )

    def indexar(self, documentos: list[Documento], embeddings: list[list[float]]) -> None:
        """Substitui o índice pelos documentos atuais (upsert por id + poda)."""
        with closing(self._conectar()) as conn, conn:
            with conn.cursor() as cur:
                for doc, emb in zip(documentos, embeddings):
                    cur.execute(
                        f"""
                        INSERT INTO {_TABELA} (id, tipo, titulo, texto, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                            tipo = EXCLUDED.tipo,
                            titulo = EXCLUDED.titulo,
                            texto = EXCLUDED.texto,
                            embedding = EXCLUDED.embedding;
                        """,
                        (doc.id, doc.tipo, doc.titulo, doc.texto, emb),
                    )
                # remove documentos que saíram do corpus
                ids_atuais = tuple(doc.id for doc in documentos) or ("",)
                cur.execute(f"DELETE FROM {_TABELA} WHERE id NOT IN %s;", (ids_atuais,))

    def buscar(self, embedding: list[float], k: int) -> list[Trecho]:
        """Retorna os ``k`` trechos mais próximos por distância de cosseno."""
        with closing(self._conectar()) as conn, conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT tipo, titulo, texto, embedding <=> %s::vector AS distancia
                    FROM {_TABELA}
                    ORDER BY distancia ASC
                    LIMIT %s;
                    """,
                    (embedding, k),
                )
                linhas = cur.fetchall()
        return [
            Trecho(tipo=t, titulo=ti, texto=tx, distancia=float(d))
            for (t, ti, tx, d) in linhas
        ]

    def contar(self) -> int:
        """Quantidade de documentos indexados (0 = índice/tabela ainda inexistente).

        Não registra o tipo vector (contagem não precisa) e engole qualquer erro —
        tabela ausente, extensão ausente etc. — devolvendo 0.
        """
        try:
            with closing(self._conectar(registrar_vetor=False)) as conn, conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT COUNT(*) FROM {_TABELA};")
                    return int(cur.fetchone()[0])
        except Exception:
            return 0
