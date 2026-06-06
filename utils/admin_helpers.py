import json
import os
from pathlib import Path
from datetime import datetime


DATA_DIR = Path(__file__).parent.parent / "data"


def _get_data_file(filename: str) -> Path:
    """Retorna caminho do arquivo de dados."""
    return DATA_DIR / filename


def _fazer_backup(filepath: Path):
    """Faz backup do arquivo antes de sobrescrever."""
    if filepath.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = filepath.with_stem(f"{filepath.stem}_bkp_{timestamp}")
        backup_path.write_text(filepath.read_text(encoding="utf-8"), encoding="utf-8")


def carregar_projetos() -> list[dict]:
    """Carrega lista de projetos do JSON."""
    try:
        path = _get_data_file("projetos.json")
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Erro ao carregar projetos: {e}")


def salvar_projetos(projetos: list[dict]):
    """Salva lista de projetos no JSON com backup automático."""
    path = _get_data_file("projetos.json")
    _fazer_backup(path)
    path.write_text(
        json.dumps(projetos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def carregar_experiencias() -> dict:
    """Carrega experiências do JSON."""
    try:
        path = _get_data_file("experiencias.json")
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Erro ao carregar experiências: {e}")


def salvar_experiencias(dados: dict):
    """Salva experiências no JSON com backup automático."""
    path = _get_data_file("experiencias.json")
    _fazer_backup(path)
    path.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def carregar_perfil() -> dict:
    """Carrega perfil do JSON."""
    try:
        path = _get_data_file("perfil.json")
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Erro ao carregar perfil: {e}")


def salvar_perfil(perfil: dict):
    """Salva perfil no JSON com backup automático."""
    path = _get_data_file("perfil.json")
    _fazer_backup(path)
    path.write_text(
        json.dumps(perfil, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def carregar_artigos() -> list[dict]:
    """Carrega lista de artigos/publicações do JSON."""
    try:
        path = _get_data_file("artigos.json")
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Erro ao carregar artigos: {e}")


def salvar_artigos(artigos: list[dict]):
    """Salva lista de artigos no JSON com backup automático."""
    path = _get_data_file("artigos.json")
    _fazer_backup(path)
    path.write_text(
        json.dumps(artigos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def validar_artigo(a: dict) -> bool:
    """Valida estrutura mínima de um artigo."""
    return bool(a.get("titulo") and a.get("url"))


def validar_projeto(p: dict) -> bool:
    """Valida estrutura mínima de um projeto."""
    campos_obrigatorios = ["titulo", "categoria", "descricao", "stack", "destaque"]
    return all(campo in p for campo in campos_obrigatorios)


def validar_experiencia(exp: dict) -> bool:
    """Valida estrutura mínima de uma experiência."""
    campos_obrigatorios = ["periodo", "cargo", "empresa", "local"]
    return all(campo in exp for campo in campos_obrigatorios)


def validar_formacao(form: dict) -> bool:
    """Valida estrutura mínima de formação."""
    campos_obrigatorios = ["grau", "instituicao", "local", "status"]
    return all(campo in form for campo in campos_obrigatorios)
