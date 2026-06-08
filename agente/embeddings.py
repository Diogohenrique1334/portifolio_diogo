"""Wrapper de embeddings da OpenAI.

Isola a chamada à API de embeddings para que o resto do código não dependa do SDK
diretamente. Usado tanto na indexação (lote de documentos) quanto na consulta.
"""

from __future__ import annotations

from openai import OpenAI


class EmbeddingClient:
    """Gera embeddings de texto via OpenAI."""

    def __init__(self, api_key: str, modelo: str, dimensao: int):
        self._client = OpenAI(api_key=api_key)
        self._modelo = modelo
        self._dimensao = dimensao

    def _embed(self, textos: list[str]) -> list[list[float]]:
        resposta = self._client.embeddings.create(
            model=self._modelo,
            input=textos,
            dimensions=self._dimensao,
        )
        return [item.embedding for item in resposta.data]

    def embed_documentos(self, textos: list[str]) -> list[list[float]]:
        """Embedda uma lista de documentos (indexação)."""
        if not textos:
            return []
        return self._embed(textos)

    def embed_consulta(self, texto: str) -> list[float]:
        """Embedda uma única pergunta (consulta)."""
        return self._embed([texto])[0]
