import json
import urllib.parse
import streamlit as st
from pathlib import Path
from utils.sidebar import render_sidebar
from utils.styles import inject_css
from utils.tech_icons import render_tech_badge

st.set_page_config(
    page_title="Projetos — Diogo Oliveira",
    page_icon="🗂️",
    layout="wide",
)

inject_css()
render_sidebar()

st.markdown('<p class="sec-heading">Projetos</p>', unsafe_allow_html=True)


@st.cache_data
def carregar_projetos() -> list[dict]:
    path = Path(__file__).parent.parent / "data" / "projetos.json"
    return json.loads(path.read_text(encoding="utf-8"))


EMOJI_CATEGORIA = {
    "Computer Vision": "🔬",
    "Análise de Dados": "📊",
    "Machine Learning": "🤖",
    "NLP": "💬",
    "Engenharia de Dados": "⚙️",
    "Produto de Dados": "🛠️",
}

projetos = carregar_projetos()
categorias_disponiveis = sorted({p["categoria"] for p in projetos if p["destaque"]})

filtro = st.multiselect(
    "Filtrar por categoria",
    options=categorias_disponiveis,
    default=[],
    placeholder="Todas as categorias",
)

projetos_filtrados = [
    p for p in projetos
    if p["destaque"] and (not filtro or p["categoria"] in filtro)
]

if not projetos_filtrados:
    st.info("Nenhum projeto encontrado com os filtros selecionados.")
    st.stop()

st.caption(f"{len(projetos_filtrados)} projeto(s) encontrado(s)")
st.markdown("")


def _render_card(p: dict):
    """Renderiza um card de projeto com imagem, badges, ações e 'saber mais'."""
    assets_dir = Path(__file__).parent.parent / "assets" / "projetos"
    emoji = EMOJI_CATEGORIA.get(p["categoria"], "📁")

    with st.container(border=True):
        # ---- Thumbnail ----
        imagem_path = assets_dir / p["imagem"] if p.get("imagem") else None
        if imagem_path and imagem_path.exists():
            import base64
            img_bytes = imagem_path.read_bytes()
            img_b64 = base64.b64encode(img_bytes).decode()
            st.markdown(
                f'<img src="data:image/png;base64,{img_b64}" style="width:100%;height:260px;object-fit:cover;border-radius:8px;margin-bottom:12px;">',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="proj-thumb">{emoji}</div>',
                unsafe_allow_html=True,
            )

        # ---- Categoria + Título + Descrição curta ----
        techs_html = "".join(render_tech_badge(t) for t in p["stack"])
        st.markdown(
            f"""
            <span class="proj-cat">{p['categoria']}</span>
            <p class="proj-title">{p['titulo']}</p>
            <p class="proj-desc">{p['descricao']}</p>
            <div class="proj-techs">{techs_html}</div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Métricas (se existirem) ----
        if p.get("metricas"):
            metricas_linhas = "  ·  ".join(
                f"**{k}:** {v}" for k, v in p["metricas"].items()
            )
            st.markdown(
                f'<div class="proj-metrics">{metricas_linhas}</div>',
                unsafe_allow_html=True,
            )

        # ---- Botões de ação ----
        subject = urllib.parse.quote(f"Interesse no projeto: {p['titulo']}")
        body = urllib.parse.quote(
            f"Olá Diogo,\n\nVi seu portfólio e fiquei interessado no projeto '{p['titulo']}'.\n"
            "Gostaria de saber mais sobre como você o desenvolveu e se poderíamos conversar.\n\n"
        )
        mailto = f"mailto:diogohenrique1334@gmail.com?subject={subject}&body={body}"

        if p.get("github"):
            col_gh, col_contact = st.columns(2)
            col_gh.link_button("🐙 GitHub", p["github"], use_container_width=True)
            col_contact.link_button("✉ Fale comigo", mailto, use_container_width=True)
        else:
            st.link_button("✉ Fale comigo sobre este projeto", mailto, use_container_width=True)

        # ---- Saber mais (para leitores não técnicos) ----
        if p.get("descricao_longa"):
            with st.expander("📖 Saber mais — explicação sem jargões"):
                st.markdown(p["descricao_longa"])
                if p.get("impacto"):
                    st.success(f"**Impacto:** {p['impacto']}")


# Renderiza em grade de 2 colunas
for i in range(0, len(projetos_filtrados), 2):
    cols = st.columns(2, gap="medium")
    for j in range(2):
        if i + j >= len(projetos_filtrados):
            break
        with cols[j]:
            _render_card(projetos_filtrados[i + j])

    st.markdown("")
