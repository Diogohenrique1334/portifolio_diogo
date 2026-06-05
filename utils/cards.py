"""Renderização de cards de currículo (formação e certificações).

O markdown do Streamlit trata linhas indentadas com 4+ espaços como bloco de
código e encerra um bloco HTML ao encontrar uma linha em branco. Por isso o
HTML aqui é montado em linha única, sem indentação à esquerda — caso contrário
cards concatenados vazam como texto cru na página.
"""

from __future__ import annotations


def edu_card(titulo: str, instituicao: str, periodo: str = "", url: str | None = None) -> str:
    """Monta o HTML de um card de formação ou certificação.

    Serve tanto para Formação quanto para Certificações, já que ambos usam a
    classe CSS ``.edu-card``.

    Args:
        titulo: título principal (grau acadêmico ou nome da certificação).
        instituicao: nome da instituição.
        periodo: período ou ano. Omitido do HTML quando vazio.
        url: link opcional do certificado. Quando presente, o card vira clicável.

    Returns:
        String HTML de um único ``.edu-card`` em linha única (sem quebras de
        linha à esquerda).
    """
    periodo_html = f'<p class="edu-period">{periodo}</p>' if periodo else ""
    corpo = (
        '<div class="edu-card">'
        f'<p class="edu-degree">{titulo}</p>'
        f'<p class="edu-school">{instituicao}</p>'
        f"{periodo_html}"
        "</div>"
    )
    if url:
        return f'<a href="{url}" target="_blank" class="edu-card-link">{corpo}</a>'
    return corpo


def edu_grid(cards: list[str]) -> str:
    """Envolve uma lista de cards em um grid ``.edu-grid``.

    Args:
        cards: HTML de cada card (tipicamente vindo de :func:`edu_card`).

    Returns:
        String HTML do grid completo em linha única.
    """
    return f'<div class="edu-grid">{"".join(cards)}</div>'
