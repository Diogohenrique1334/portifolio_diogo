"""Proteções do agente público: validação de input, rate limit e perguntas guiadas.

Como o agente é exposto num portfólio público e cada pergunta gera uma chamada
paga à OpenAI, limitamos tamanho de input e número de perguntas por sessão, e
oferecemos perguntas sugeridas para guiar o uso (reduz chamadas aleatórias).
"""

from __future__ import annotations

# Perguntas que aparecem como botões — guiam o visitante e reduzem chamadas soltas.
PERGUNTAS_SUGERIDAS = [
    "Qual a experiência do Diogo com visão computacional?",
    "Que projetos ele tem envolvendo LLMs?",
    "Qual a formação acadêmica e certificações dele?",
    "Que tipo de impacto ele gerou na Claro?",
    "Ele tem experiência com engenharia de dados e deploy?",
]


def validar_pergunta(texto: str, max_chars: int) -> tuple[bool, str]:
    """Valida a pergunta do usuário. Retorna (ok, mensagem_de_erro)."""
    if not texto or not texto.strip():
        return False, "Digite uma pergunta."
    if len(texto) > max_chars:
        return False, f"Pergunta muito longa (máx. {max_chars} caracteres)."
    return True, ""


class RateLimiterSessao:
    """Limita o número de perguntas por sessão Streamlit (estado em session_state)."""

    _CHAVE = "_agente_perguntas_contador"

    def __init__(self, maximo: int):
        self._maximo = maximo

    def _contador(self) -> int:
        import streamlit as st

        return st.session_state.get(self._CHAVE, 0)

    def permitido(self) -> bool:
        """True se ainda há perguntas disponíveis nesta sessão."""
        return self._contador() < self._maximo

    def registrar(self) -> None:
        """Contabiliza uma pergunta consumida."""
        import streamlit as st

        st.session_state[self._CHAVE] = self._contador() + 1

    def restantes(self) -> int:
        return max(0, self._maximo - self._contador())
