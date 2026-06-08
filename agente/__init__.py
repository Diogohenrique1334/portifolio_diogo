"""Agente de trajetória — RAG sobre o perfil, projetos e experiências do Diogo.

Responde perguntas em linguagem natural sobre a carreira (ex.: "qual experiência
ele tem com visão computacional?"), recuperando trechos relevantes do corpus
(JSONs em ``data/``) via embeddings + pgvector (Neon) e redigindo a resposta com
um LLM (OpenAI).

Camadas:
- ``config``      — credenciais e parâmetros (.env / st.secrets)
- ``corpus``      — JSONs → documentos textuais
- ``embeddings``  — wrapper de embeddings OpenAI
- ``vector_store``— índice pgvector no Postgres Neon
- ``indexador``   — (re)constrói o índice (offline)
- ``retrieval``   — pergunta → documentos relevantes
- ``seguranca``   — validação de input, rate limit, perguntas sugeridas
- ``agente``      — orquestra retrieval + LLM → resposta + fontes
"""
