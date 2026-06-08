"""Recuperação: pergunta → trechos mais relevantes do índice.

Junta o cliente de embeddings e o vector store numa única fachada usada pelo agente.
"""

from __future__ import annotations

from agente.config import AgenteConfig
from agente.embeddings import EmbeddingClient
from agente.vector_store import PgVectorStore, Trecho


class Recuperador:
    """Embedda a pergunta e busca os trechos mais próximos no pgvector."""

    def __init__(self, cfg: AgenteConfig):
        self._cfg = cfg
        self._embeddings = EmbeddingClient(
            api_key=cfg.openai_api_key,
            modelo=cfg.modelo_embedding,
            dimensao=cfg.dimensao_embedding,
        )
        self._store = PgVectorStore(
            db_url=cfg.db_url_libpq(), dimensao=cfg.dimensao_embedding
        )

    def recuperar(self, pergunta: str, k: int | None = None) -> list[Trecho]:
        """Retorna os ``k`` trechos mais relevantes para a pergunta."""
        k = k or self._cfg.top_k
        vetor = self._embeddings.embed_consulta(pergunta)
        return self._store.buscar(vetor, k)

    def indice_vazio(self) -> bool:
        """True se o índice ainda não foi construído (nenhum documento)."""
        return self._store.contar() == 0
