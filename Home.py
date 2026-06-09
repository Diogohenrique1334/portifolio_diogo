import streamlit as st
import json
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

from utils.sidebar import render_sidebar
from utils.styles import inject_css
from utils.tech_icons import render_tech_badge
from utils.assistente_widget import render_assistente

st.set_page_config(
    page_title="Diogo Oliveira - Cientista de Dados",
    page_icon="📊",
    layout="wide",
)

inject_css()
render_sidebar()

# ================================================================
# HERO
# ================================================================
foto_path = Path("assets/foto.png")

if foto_path.exists():
    import base64
    img_bytes = foto_path.read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode()
    avatar_html = f'<img src="data:image/png;base64,{img_b64}" style="width:160px;height:160px;border-radius:50%;object-fit:cover;">'
else:
    avatar_html = "DO"

st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-avatar">{avatar_html}</div>
        <p class="hero-name">Diogo Oliveira</p>
        <p class="hero-role">Cientista de Dados · Claro SA</p>
        <p class="hero-tagline">
            8 anos convertendo dados em decisões.<br>
            Da análise exploratória a sistemas em produção.
        </p>
        <p class="hero-loc">📍 São Paulo, Brasil</p>
        <div class="hero-social">
            <a href="https://www.linkedin.com/in/diogooliveira1334/" target="_blank">💼 LinkedIn</a>
            <a href="https://github.com/Diogohenrique1334" target="_blank">🐙 GitHub</a>
            <a href="https://www.datascienceportfol.io/diogohenrique1334" target="_blank">🌐 Portfólio</a>
            <a href="mailto:diogohenrique1334@gmail.com">✉ Email</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ================================================================
# SOBRE MIM
# ================================================================
st.markdown('<p class="sec-heading">Sobre mim</p>', unsafe_allow_html=True)
st.markdown(
    """
    <p class="about-text">
        Cientista de Dados com mais de 8 anos de experiência em análise, engenharia e modelagem de dados, atuando atualmente 
        no setor de telecomunicações na Claro, com passagens por Comgás e JBS. Graduado em Ciência de Dados pela 
        Universidade Anhembi Morumbi e pós-graduando em Engenharia de Machine Learning pela Data Science Academy.
        <br><br>
        Atuo no desenvolvimento de soluções de dados de ponta a ponta, desde a extração, transformação e modelagem das informações 
        até a construção de APIs REST, aplicações analíticas, modelos de Machine Learning e dashboards interativos 
        prontos para produção. Meu foco está na criação de soluções que gerem impacto mensurável para o negócio, 
        reduzam esforço operacional e apoiem a tomada de decisão baseada em dados.
        <br><br>
        Possuo experiência em projetos de automação inteligente, visão computacional com YOLOv8, integração de modelos de linguagem (LLMs), 
        desenvolvimento de aplicações orientadas a dados e construção de pipelines escaláveis. Também atuo na implementação de 
        arquiteturas modernas, com código modular, versionamento de banco de dados, integração contínua e deploy em ambientes de nuvem.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ================================================================
# MÉTRICAS
# ================================================================
projetos_path = Path("data/projetos.json")
projetos = json.loads(projetos_path.read_text(encoding="utf-8"))
projetos_destaque = [p for p in projetos if p["destaque"]]
todas_stacks = {tech for p in projetos_destaque for tech in p["stack"]}

st.markdown(
    f"""
    <div class="metrics-row">
        <div class="metric-box">
            <div class="val">{len(projetos_destaque)}</div>
            <div class="lbl">Projetos no portfólio</div>
        </div>
        <div class="metric-box">
            <div class="val">{len(todas_stacks)}+</div>
            <div class="lbl">Tecnologias dominadas</div>
        </div>
        <div class="metric-box">
            <div class="val">8</div>
            <div class="lbl">Anos de experiência</div>
        </div>
        <div class="metric-box">
            <div class="val">3</div>
            <div class="lbl">Empresas atendidas</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ================================================================
# HABILIDADES
# ================================================================
st.markdown('<p class="sec-heading">Habilidades técnicas</p>', unsafe_allow_html=True)

skills = [
    "Python", "R", "SQL", "DAX",
    "scikit-learn", "statsmodels", "YOLOv8", "PyTorch", "OpenCV",
    "pandas", "numpy", "scipy",
    "Streamlit", "ECharts", "Plotly", "Power BI",
    "FastAPI", "Docker", "PostgreSQL", "SQLite", "SQLAlchemy", "Alembic",
    "Git", "Render", "AWS", "OpenAI GPT-4",
    "Machine Learning", "Deep Learning", "Computer Vision",
]

badges_html = "".join(render_tech_badge(s) for s in skills)
st.markdown(f'<div class="skills-wrap">{badges_html}</div>', unsafe_allow_html=True)

st.divider()

# ================================================================
# ASSISTENTE DA TRAJETÓRIA (RAG)
# ================================================================
st.markdown(
    '<p class="sec-heading">Pergunte sobre minha trajetória</p>',
    unsafe_allow_html=True,
)
st.caption(
    "Assistente com IA que responde sobre experiência, projetos e formação, "
    "usando o conteúdo deste portfólio como fonte."
)
render_assistente()
