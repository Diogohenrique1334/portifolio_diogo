"""Constrói o corpus textual da trajetória a partir dos JSONs em ``data/``.

Cada item relevante (perfil, projeto, experiência, formação, certificações e
artigo) vira um :class:`Documento` com texto legível e metadados — a unidade que
será embeddada e indexada. O corpus é pequeno por natureza; o RAG aqui é uma
demonstração da técnica (o conteúdo caberia inteiro em contexto).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class Documento:
    """Um trecho do corpus pronto para embedding."""

    id: str
    tipo: str  # perfil | projeto | experiencia | formacao | certificacoes | artigo
    titulo: str
    texto: str


def _ler_json(nome: str):
    """Lê um arquivo JSON de ``data/``; retorna ``None`` se não existir."""
    caminho = _DATA_DIR / nome
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def _linha(rotulo: str, valor) -> str:
    """Formata 'rótulo: valor', ignorando valores vazios."""
    if valor is None or valor == "" or valor == []:
        return ""
    if isinstance(valor, (list, tuple)):
        valor = ", ".join(str(v) for v in valor)
    if isinstance(valor, dict):
        valor = "; ".join(f"{k}: {v}" for k, v in valor.items())
    return f"{rotulo}: {valor}\n"


def _doc_perfil(perfil: dict) -> Documento:
    texto = "Perfil profissional.\n"
    for rotulo, chave in [
        ("Nome", "nome"),
        ("Cargo atual", "cargo"),
        ("Empresa", "empresa"),
        ("Localização", "localizacao"),
        ("Anos de experiência", "anos_experiencia"),
        ("Resumo", "tagline_sidebar"),
    ]:
        texto += _linha(rotulo, perfil.get(chave))
    return Documento(id="perfil", tipo="perfil", titulo="Perfil", texto=texto)


def _doc_projeto(proj: dict, indice: int) -> Documento:
    titulo = proj.get("titulo", f"Projeto {indice}")
    texto = "Projeto do portfólio.\n"
    for rotulo, chave in [
        ("Título", "titulo"),
        ("Categoria", "categoria"),
        ("Descrição", "descricao"),
        ("Descrição detalhada", "descricao_longa"),
        ("Impacto", "impacto"),
        ("Stack", "stack"),
        ("Métricas", "metricas"),
        ("GitHub", "github"),
        ("Demo", "demo"),
    ]:
        texto += _linha(rotulo, proj.get(chave))
    return Documento(id=f"projeto-{indice}", tipo="projeto", titulo=titulo, texto=texto)


def _doc_experiencia(exp: dict, indice: int) -> Documento:
    titulo = f"{exp.get('cargo', '')} — {exp.get('empresa', '')}".strip(" —")
    texto = "Experiência profissional.\n"
    texto += _linha("Cargo", exp.get("cargo"))
    texto += _linha("Empresa", exp.get("empresa"))
    texto += _linha("Período", exp.get("periodo"))
    texto += _linha("Local", exp.get("local"))
    for bullet in exp.get("bullets", []):
        texto += f"- {bullet}\n"
    return Documento(
        id=f"experiencia-{indice}", tipo="experiencia", titulo=titulo, texto=texto
    )


def _doc_formacao(formacoes: list) -> Documento:
    texto = "Formação acadêmica.\n"
    for f in formacoes:
        texto += (
            f"- {f.get('grau', '')} — {f.get('instituicao', '')} "
            f"({f.get('periodo', '')}, {f.get('status', '')})\n"
        )
    return Documento(id="formacao", tipo="formacao", titulo="Formação", texto=texto)


def _doc_certificacoes(certs: list) -> Documento:
    texto = "Certificações.\n"
    for c in certs:
        texto += f"- {c.get('nome', '')} — {c.get('instituicao', '')} ({c.get('ano', '')})\n"
    return Documento(
        id="certificacoes", tipo="certificacoes", titulo="Certificações", texto=texto
    )


def _doc_artigo(art: dict, indice: int) -> Documento:
    titulo = art.get("titulo") or art.get("resumo", "")[:60] or f"Artigo {indice}"
    texto = "Artigo / publicação.\n"
    for rotulo, chave in [
        ("Título", "titulo"),
        ("Resumo", "resumo"),
        ("Plataforma", "plataforma"),
        ("Data", "data"),
        ("Tags", "tags"),
        ("Projeto relacionado", "projeto_relacionado"),
        ("URL", "url"),
    ]:
        texto += _linha(rotulo, art.get(chave))
    return Documento(id=f"artigo-{indice}", tipo="artigo", titulo=titulo, texto=texto)


def construir_corpus() -> list[Documento]:
    """Lê todos os JSONs de ``data/`` e devolve a lista de documentos do corpus."""
    docs: list[Documento] = []

    perfil = _ler_json("perfil.json")
    if perfil:
        docs.append(_doc_perfil(perfil))

    projetos = _ler_json("projetos.json") or []
    if isinstance(projetos, dict):
        projetos = projetos.get("projetos", [])
    for i, proj in enumerate(projetos, start=1):
        docs.append(_doc_projeto(proj, i))

    experiencias = _ler_json("experiencias.json") or {}
    for i, exp in enumerate(experiencias.get("experiencias", []), start=1):
        docs.append(_doc_experiencia(exp, i))
    if experiencias.get("formacao"):
        docs.append(_doc_formacao(experiencias["formacao"]))
    if experiencias.get("certificacoes"):
        docs.append(_doc_certificacoes(experiencias["certificacoes"]))

    artigos = _ler_json("artigos.json") or []
    if isinstance(artigos, dict):
        artigos = artigos.get("artigos", [])
    for i, art in enumerate(artigos, start=1):
        docs.append(_doc_artigo(art, i))

    return docs
