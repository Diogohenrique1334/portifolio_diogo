"""(Re)constrói o índice vetorial da trajetória.

Lê o corpus dos JSONs, gera embeddings e grava no pgvector (Neon). Idempotente:
rode sempre que editar o perfil/projetos/experiências.

Uso (a partir da raiz do projeto):

    python -m agente.indexador
"""

from __future__ import annotations

from agente.config import AgenteConfig
from agente.corpus import construir_corpus
from agente.diagnostico import construir_documentos_diagnostico
from agente.embeddings import EmbeddingClient
from agente.vector_store import PgVectorStore


def reindexar(cfg: AgenteConfig | None = None) -> int:
    """Reconstrói o índice e retorna a quantidade de documentos indexados.

    Corpus = JSONs do portfólio + (opcional) documentos curados do Diagnóstico.
    """
    cfg = cfg or AgenteConfig()
    if not cfg.configurado:
        raise RuntimeError(
            "Configure OPENAI_API_KEY e DATABASE_URL (.env ou st.secrets) antes de indexar."
        )

    documentos = construir_corpus() + construir_documentos_diagnostico(cfg)
    embeddings_client = EmbeddingClient(
        api_key=cfg.openai_api_key,
        modelo=cfg.modelo_embedding,
        dimensao=cfg.dimensao_embedding,
    )
    store = PgVectorStore(db_url=cfg.db_url_libpq(), dimensao=cfg.dimensao_embedding)

    vetores = embeddings_client.embed_documentos([d.texto for d in documentos])
    store.criar_schema()
    store.indexar(documentos, vetores)
    return len(documentos)


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv()
    total = reindexar()
    print(f"Índice reconstruído com {total} documentos.")


if __name__ == "__main__":
    main()
