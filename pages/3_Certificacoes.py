import json
import streamlit as st
from pathlib import Path
from utils.sidebar import render_sidebar
from utils.styles import inject_css

st.set_page_config(
    page_title="Certificações - Diogo Oliveira",
    page_icon="🏆",
    layout="wide",
)

inject_css()
render_sidebar()

st.markdown('<p class="sec-heading">Certificações & Cursos</p>', unsafe_allow_html=True)


@st.cache_data
def carregar_certificacoes() -> list[dict]:
    path = Path(__file__).parent.parent / "data" / "experiencias.json"
    dados = json.loads(path.read_text(encoding="utf-8"))
    return dados.get("certificacoes", [])


certificacoes = carregar_certificacoes()

if not certificacoes:
    st.info("Nenhuma certificação adicionada ainda. Acesse o painel Admin para adicionar.")
    st.stop()

st.caption(f"{len(certificacoes)} certificação(ões) obtida(s)")
st.markdown("")

# Organiza por ano (decrescente)
certs_por_ano = {}
for cert in certificacoes:
    ano = cert.get("ano", "Sem data")
    if ano not in certs_por_ano:
        certs_por_ano[ano] = []
    certs_por_ano[ano].append(cert)

# Renderiza por ano
for ano in sorted(certs_por_ano.keys(), reverse=True):
    with st.container():
        st.markdown(f"### 📅 {ano}")

        cols = st.columns(2, gap="medium")
        for i, cert in enumerate(certs_por_ano[ano]):
            with cols[i % 2]:
                with st.container(border=True):
                    st.markdown(f"### 🏆 {cert['nome']}")
                    st.markdown(f"**{cert['instituicao']}**")

                    # Detalhes adicionais (se existirem)
                    if cert.get("url"):
                        st.link_button(
                            "🔗 Ver certificado",
                            cert["url"],
                            use_container_width=True,
                        )

                    if cert.get("descricao"):
                        st.markdown(f"_{cert['descricao']}_")

        st.markdown("")
