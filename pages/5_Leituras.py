import base64
import json
import streamlit as st
from pathlib import Path
from utils.sidebar import render_sidebar
from utils.styles import inject_css

st.set_page_config(
    page_title="Leituras - Diogo Oliveira",
    page_icon="📚",
    layout="wide",
)

inject_css()
render_sidebar()

st.markdown('<p class="sec-heading">📚 Leituras & Acervo Técnico</p>', unsafe_allow_html=True)

ASSETS_LIVROS = Path(__file__).parent.parent / "assets" / "livros"

# Cor da faixa/badge por status da leitura.
COR_STATUS = {
    "Lido": "#18990b",
    "Lendo": "#D4AF37",
    "Quero ler": "#6b7280",
}


@st.cache_data
def carregar_livros() -> list[dict]:
    path = Path(__file__).parent.parent / "data" / "livros.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


livros = carregar_livros()

if not livros:
    st.info("Nenhum livro cadastrado ainda. Acesse o painel Admin para adicionar.")
    st.stop()


# ================================================================
# FILTROS (no topo da seção)
# ================================================================
categorias = ["Todas"] + sorted({l.get("categoria", "") for l in livros if l.get("categoria")})

col_cat, col_status = st.columns([1, 2])
with col_cat:
    cat_sel = st.selectbox("Categoria", categorias, index=0)
with col_status:
    status_sel = st.segmented_control(
        "Status",
        ["Todos", "Lido", "Lendo", "Quero ler"],
        default="Todos",
    )


def _passa_filtro(livro: dict) -> bool:
    if cat_sel != "Todas" and livro.get("categoria") != cat_sel:
        return False
    if status_sel and status_sel != "Todos" and livro.get("status") != status_sel:
        return False
    return True


filtrados = [l for l in livros if _passa_filtro(l)]


# ================================================================
# KPIs (visão geral — sobre o acervo inteiro, não o filtro)
# ================================================================
def _conta(status: str) -> int:
    return sum(1 for l in livros if l.get("status") == status)


n_categorias = len({l.get("categoria") for l in livros if l.get("categoria")})
st.markdown(
    f"""
    <div class="metrics-row">
        <div class="metric-box"><div class="val">{_conta('Lido')}</div><div class="lbl">Lidos</div></div>
        <div class="metric-box"><div class="val">{_conta('Lendo')}</div><div class="lbl">Lendo</div></div>
        <div class="metric-box"><div class="val">{_conta('Quero ler')}</div><div class="lbl">Quero ler</div></div>
        <div class="metric-box"><div class="val">{n_categorias}</div><div class="lbl">Categorias</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("")


# ================================================================
# CARDS
# ================================================================
def _capa_html(capa: str, titulo: str) -> str:
    """Retorna a capa do livro (imagem local em base64) ou um fallback estilizado."""
    if capa:
        caminho = ASSETS_LIVROS / capa
        if caminho.exists():
            b64 = base64.b64encode(caminho.read_bytes()).decode()
            return (
                f'<div class="proj-thumb" style="padding:0;overflow:hidden;">'
                f'<img src="data:image/png;base64,{b64}" '
                f'style="width:100%;height:100%;object-fit:cover;border-radius:8px;"></div>'
            )
    return '<div class="proj-thumb">📖</div>'


def _estrelas(nota) -> str:
    try:
        n = int(nota)
    except (TypeError, ValueError):
        return ""
    n = max(0, min(5, n))
    return "★" * n + "☆" * (5 - n)


def _render_livro(livro: dict):
    with st.container(border=True):
        st.markdown(_capa_html(livro.get("capa", ""), livro["titulo"]), unsafe_allow_html=True)

        categoria = livro.get("categoria", "")
        status = livro.get("status", "")
        cor = COR_STATUS.get(status, "#6b7280")
        badges = f'<span class="proj-cat">{categoria}</span>'
        if status:
            badges += (
                f'<span class="proj-cat" style="margin-left:8px;'
                f'background:{cor}22;color:{cor};">{status}</span>'
            )
        st.markdown(badges, unsafe_allow_html=True)

        st.markdown(f'<p class="proj-title">{livro["titulo"]}</p>', unsafe_allow_html=True)
        st.markdown(
            f'<p class="proj-desc" style="margin-top:-4px;">{livro.get("autor", "")}</p>',
            unsafe_allow_html=True,
        )

        estrelas = _estrelas(livro.get("nota"))
        if estrelas:
            ano = livro.get("ano_leitura")
            sufixo = f'  ·  {ano}' if ano else ""
            st.markdown(
                f'<p style="color:#D4AF37;font-size:1rem;margin:0;">{estrelas}'
                f'<span style="color:#6b7280;font-size:0.8rem;">{sufixo}</span></p>',
                unsafe_allow_html=True,
            )

        if livro.get("aprendizado"):
            st.markdown(
                f'<p class="proj-desc">{livro["aprendizado"]}</p>',
                unsafe_allow_html=True,
            )

        if livro.get("projeto_relacionado"):
            st.caption(f"🔗 Apliquei em: {livro['projeto_relacionado']}")


st.caption(f"{len(filtrados)} de {len(livros)} livro(s)")
st.markdown("")

for i in range(0, len(filtrados), 2):
    cols = st.columns(2, gap="medium")
    for j in range(2):
        if i + j >= len(filtrados):
            break
        with cols[j]:
            _render_livro(filtrados[i + j])
    st.markdown("")
