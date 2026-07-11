"""Testes de integridade dos dados dinâmicos do portfólio.

O painel Admin grava `data/*.json` em tempo de execução; um JSON quebrado ou
com schema incompleto derruba a página inteira do Streamlit. Estes testes
travam o pipeline (CI) antes que isso chegue ao deploy, reusando os mesmos
validadores que o Admin usa.
"""
import pytest

from utils.admin_helpers import (
    carregar_projetos,
    carregar_experiencias,
    carregar_perfil,
    carregar_artigos,
    carregar_livros,
    validar_projeto,
    validar_experiencia,
    validar_formacao,
    validar_artigo,
    validar_livro,
)

# Campos mínimos que o cabeçalho/sidebar do portfólio sempre lê.
CAMPOS_PERFIL = ("nome", "cargo", "linkedin", "github")


def test_projetos_carregam_e_sao_lista():
    projetos = carregar_projetos()
    assert isinstance(projetos, list)
    assert projetos, "data/projetos.json não pode estar vazio"


@pytest.mark.parametrize("projeto", carregar_projetos(), ids=lambda p: p.get("titulo", "?"))
def test_cada_projeto_tem_schema_minimo(projeto):
    assert validar_projeto(projeto), f"projeto inválido: {projeto.get('titulo')}"


def test_experiencias_tem_chaves_de_topo():
    dados = carregar_experiencias()
    assert {"experiencias", "formacao", "certificacoes"} <= set(dados)


@pytest.mark.parametrize("exp", carregar_experiencias()["experiencias"], ids=lambda e: e.get("cargo", "?"))
def test_cada_experiencia_tem_schema_minimo(exp):
    assert validar_experiencia(exp), f"experiência inválida: {exp.get('cargo')}"


@pytest.mark.parametrize("form", carregar_experiencias()["formacao"], ids=lambda f: f.get("grau", "?"))
def test_cada_formacao_tem_schema_minimo(form):
    assert validar_formacao(form), f"formação inválida: {form.get('grau')}"


def test_perfil_tem_campos_essenciais():
    perfil = carregar_perfil()
    faltando = [c for c in CAMPOS_PERFIL if not perfil.get(c)]
    assert not faltando, f"perfil sem campos: {faltando}"


@pytest.mark.parametrize("artigo", carregar_artigos(), ids=lambda a: a.get("titulo", "?"))
def test_cada_artigo_tem_schema_minimo(artigo):
    assert validar_artigo(artigo), f"artigo inválido: {artigo.get('titulo')}"


@pytest.mark.parametrize("livro", carregar_livros(), ids=lambda l: l.get("titulo", "?"))
def test_cada_livro_tem_schema_minimo(livro):
    assert validar_livro(livro), f"livro inválido: {livro.get('titulo')}"
