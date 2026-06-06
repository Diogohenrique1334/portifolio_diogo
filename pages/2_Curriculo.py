import json
import streamlit as st
from pathlib import Path
from utils.sidebar import render_sidebar
from utils.styles import inject_css
from utils.tech_icons import render_tech_badge
from utils.cards import edu_card, edu_grid

st.set_page_config(
    page_title="Currículo — Diogo Oliveira",
    page_icon="📄",
    layout="wide",
)

inject_css()
render_sidebar()

st.markdown('<p class="sec-heading">Currículo</p>', unsafe_allow_html=True)


@st.cache_data
def _carregar_experiencias() -> dict:
    path = Path(__file__).parent.parent / "data" / "experiencias.json"
    return json.loads(path.read_text(encoding="utf-8"))


dados = _carregar_experiencias()

# ---- Download do currículo tradicional (aparece apenas se o arquivo existir) ----
def _encontrar_curriculo(assets_dir: Path):
    """Procura o currículo tradicional em assets, preferindo PDF a DOCX.

    Returns:
        Tupla (caminho, mime, extensao) ou (None, None, None) se não houver.
    """
    candidatos = [
        ("curriculo.pdf", "application/pdf", "pdf"),
        (
            "curriculo.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "docx",
        ),
    ]
    for nome, mime, ext in candidatos:
        caminho = assets_dir / nome
        if caminho.exists():
            return caminho, mime, ext
    return None, None, None


assets_dir = Path(__file__).parent.parent / "assets"
curriculo_path, curriculo_mime, curriculo_ext = _encontrar_curriculo(assets_dir)
if curriculo_path:
    st.download_button(
        label="⬇ Baixar currículo (anexo)",
        data=curriculo_path.read_bytes(),
        file_name=f"curriculo_diogo_oliveira.{curriculo_ext}",
        mime=curriculo_mime,
    )
    st.markdown("")

# ================================================================
# EXPERIÊNCIAS
# ================================================================
st.markdown('<p class="sec-heading">Experiência Profissional</p>', unsafe_allow_html=True)

for exp in dados.get("experiencias", []):
    bullets_html = "".join(f"<li>{b}</li>" for b in exp.get("bullets", []))
    st.markdown(
        f"""
        <div class="exp-item">
            <p class="exp-period">{exp['periodo']}</p>
            <p class="exp-role">{exp['cargo']}</p>
            <p class="exp-company">{exp['empresa']} · {exp['local']}</p>
            {"<ul class='exp-bullets'>" + bullets_html + "</ul>" if bullets_html else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ================================================================
# FORMAÇÃO
# ================================================================
st.markdown('<p class="sec-heading">Formação</p>', unsafe_allow_html=True)

formacoes = dados.get("formacao", [])
if formacoes:
    cards = [
        edu_card(
            f["grau"],
            f["instituicao"],
            " · ".join(p for p in [f.get("periodo"), f.get("status")] if p),
        )
        for f in formacoes
    ]
    st.markdown(edu_grid(cards), unsafe_allow_html=True)

# ================================================================
# CERTIFICAÇÕES (renderiza apenas se houver entradas)
# ================================================================
certs = dados.get("certificacoes", [])
if certs:
    st.divider()
    st.markdown('<p class="sec-heading">Certificações</p>', unsafe_allow_html=True)

    def _ano_ordenacao(cert: dict) -> int:
        """Converte o ano em inteiro para ordenação; vai ao fim se inválido."""
        try:
            return int(str(cert.get("ano", "")).strip())
        except (TypeError, ValueError):
            return -1

    certs_ordenadas = sorted(certs, key=_ano_ordenacao, reverse=True)
    cards = [
        edu_card(c["nome"], c["instituicao"], c.get("ano", ""), c.get("url"))
        for c in certs_ordenadas
    ]
    st.markdown(edu_grid(cards), unsafe_allow_html=True)

st.divider()

# ================================================================
# STACK TÉCNICA (vem do perfil ou estática — pode mover para JSON futuramente)
# ================================================================
st.markdown('<p class="sec-heading">Stack técnica</p>', unsafe_allow_html=True)

skills_grupos = {
    "Linguagens & Dados": ["Python", "R", "SQL", "DAX", "M", "pandas", "numpy", "scipy"],
    "Machine Learning": ["scikit-learn", "statsmodels", "YOLOv8", "PyTorch", "Keras", "TensorFlow"],
    "Visualização & Frontend": ["Streamlit", "streamlit-echarts", "Plotly", "Power BI", "Tableau"],
    "Infraestrutura": ["FastAPI", "Uvicorn", "Docker", "PostgreSQL", "SQLite", "SQLAlchemy", "Alembic", "Render", "Neon"],
}

for grupo, skills in skills_grupos.items():
    badges = "".join(render_tech_badge(s) for s in skills)
    st.markdown(f"**{grupo}**")
    st.markdown(f'<div class="skills-wrap">{badges}</div>', unsafe_allow_html=True)
    st.markdown("")
