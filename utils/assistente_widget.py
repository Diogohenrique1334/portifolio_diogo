"""Componente de UI do assistente da trajetória (RAG), embutido no Home.

Mantém o pacote ``agente/`` como lógica pura; aqui mora só a renderização Streamlit:
checagem de pré-requisitos, carregamento cacheado do agente, perguntas sugeridas,
formulário de pergunta e histórico da conversa com as fontes usadas.
"""

import streamlit as st

from agente.config import AgenteConfig
from agente.seguranca import (
    PERGUNTAS_SUGERIDAS,
    RateLimiterSessao,
    validar_pergunta,
)


@st.cache_resource(show_spinner=False)
def _carregar_agente():
    """Instancia o agente uma vez por processo (cacheado entre reruns)."""
    from agente.agente import AgenteTrajetoria

    return AgenteTrajetoria(AgenteConfig())


def _processar(agente, cfg: AgenteConfig, limiter: RateLimiterSessao, pergunta: str) -> None:
    """Valida, aplica rate limit, consulta o agente e guarda no histórico."""
    ok, msg = validar_pergunta(pergunta, cfg.max_chars_pergunta)
    if not ok:
        st.toast(msg, icon="⚠️")
        return
    if not limiter.permitido():
        st.toast("Limite de perguntas desta sessão atingido.", icon="🚦")
        return
    with st.spinner("Consultando o portfólio…"):
        resposta = agente.responder(pergunta.strip())
    limiter.registrar()
    st.session_state.agente_historico.append((pergunta.strip(), resposta))


def render_assistente() -> None:
    """Renderiza a seção do assistente. Degrada com elegância se não configurado."""
    cfg = AgenteConfig()

    if not cfg.configurado:
        st.info(
            "🔧 Assistente em configuração. (Requer `OPENAI_API_KEY` e `DATABASE_URL`; "
            "índice via `python -m agente.indexador`.)"
        )
        return

    try:
        agente = _carregar_agente()
    except Exception as erro:
        st.error(f"Não foi possível iniciar o assistente: {erro}")
        return

    if agente.indice_vazio():
        st.warning(
            "📭 Índice ainda não construído. Rode `python -m agente.indexador`."
        )
        return

    limiter = RateLimiterSessao(cfg.max_perguntas_sessao)
    if "agente_historico" not in st.session_state:
        st.session_state.agente_historico = []

    # Perguntas sugeridas
    st.markdown("**Sugestões:**")
    colunas = st.columns(len(PERGUNTAS_SUGERIDAS))
    for coluna, sugestao in zip(colunas, PERGUNTAS_SUGERIDAS):
        if coluna.button(sugestao, use_container_width=True, key=f"sug_{sugestao}"):
            _processar(agente, cfg, limiter, sugestao)

    # Formulário inline (não fixa no rodapé, ao contrário de st.chat_input)
    with st.form("form_assistente", clear_on_submit=True):
        pergunta = st.text_input(
            "Sua pergunta",
            placeholder="Pergunte algo sobre a trajetória do Diogo…",
            label_visibility="collapsed",
        )
        enviado = st.form_submit_button("Perguntar", use_container_width=True)
    if enviado and pergunta:
        _processar(agente, cfg, limiter, pergunta)

    # Histórico (mais recente primeiro)
    for pergunta_usuario, resposta in reversed(st.session_state.agente_historico):
        with st.chat_message("user"):
            st.write(pergunta_usuario)
        with st.chat_message("assistant"):
            st.write(resposta.texto)
            if resposta.fontes:
                with st.expander("Fontes usadas nesta resposta"):
                    for fonte in resposta.fontes:
                        st.markdown(f"- {fonte}")
            st.caption(
                f"{resposta.tokens} tokens · {resposta.latencia_ms} ms · "
                f"{limiter.restantes()} perguntas restantes nesta sessão"
            )
