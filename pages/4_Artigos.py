import json
import streamlit as st
from pathlib import Path
from utils.sidebar import render_sidebar
from utils.styles import inject_css

st.set_page_config(
    page_title="Artigos — Diogo Oliveira",
    page_icon="✍️",
    layout="wide",
)

inject_css()
render_sidebar()

st.markdown('<p class="sec-heading">Artigos & Publicações</p>', unsafe_allow_html=True)


@st.cache_data
def carregar_artigos() -> list[dict]:
    path = Path(__file__).parent.parent / "data" / "artigos.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


artigos = carregar_artigos()

if not artigos:
    st.info("Nenhum artigo publicado ainda. Acesse o painel Admin para adicionar.")
    st.stop()

st.caption(f"{len(artigos)} publicação(ões)")
st.markdown("")


def _render_artigo(a: dict):
    """Renderiza o card de um artigo com resumo, metadados, tags e link."""
    with st.container(border=True):
        plataforma = a.get("plataforma", "")
        data = a.get("data", "")
        meta = " · ".join(p for p in [plataforma, data] if p)
        if meta:
            st.markdown(f'<span class="proj-cat">{meta}</span>', unsafe_allow_html=True)

        st.markdown(f'<p class="proj-title">{a["titulo"]}</p>', unsafe_allow_html=True)

        if a.get("resumo"):
            st.markdown(f'<p class="proj-desc">{a["resumo"]}</p>', unsafe_allow_html=True)

        if a.get("tags"):
            tags = "  ".join(f"`{t}`" for t in a["tags"])
            st.markdown(tags)

        if a.get("projeto_relacionado"):
            st.caption(f"🔗 Projeto relacionado: {a['projeto_relacionado']}")

        st.link_button("📖 Ler artigo", a["url"], use_container_width=True)


# Renderiza em grade de 2 colunas
for i in range(0, len(artigos), 2):
    cols = st.columns(2, gap="medium")
    for j in range(2):
        if i + j >= len(artigos):
            break
        with cols[j]:
            _render_artigo(artigos[i + j])
    st.markdown("")
