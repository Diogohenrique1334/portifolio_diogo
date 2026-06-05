import streamlit as st


PORTFOLIO_CSS = """
<style>
/* ======================================================
   PORTFOLIO — GLOBAL STYLES
   ====================================================== */

.main .block-container {
    max-width: 1080px;
    padding-top: 1.5rem;
}

/* ---- HERO ---- */
.hero-wrap {
    text-align: center;
    padding: 52px 24px 36px;
}

.hero-avatar {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: linear-gradient(135deg, #18990b 0%, #65B581 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 58px;
    font-weight: 800;
    color: white;
    margin: 0 auto 24px;
    border: 4px solid rgba(24, 153, 11, 0.45);
    box-shadow: 0 0 48px rgba(24, 153, 11, 0.22);
}

.hero-avatar img {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    object-fit: cover;
}

.hero-name {
    font-size: 2.6rem;
    font-weight: 800;
    color: #f0f0f0;
    margin: 0 0 8px;
    letter-spacing: -0.5px;
    line-height: 1.1;
}

.hero-role {
    font-size: 1.1rem;
    color: #65B581;
    font-weight: 600;
    margin: 0 0 6px;
}

.hero-tagline {
    font-size: 1rem;
    color: #d1d5db;
    line-height: 1.6;
    font-style: italic;
    max-width: 520px;
    /* !important para vencer a regra do Streamlit em `.st-emotion-cache-* p`
       que zera as margens e impedia o auto de centralizar a caixa. */
    margin: 0 auto 10px !important;
    text-align: center;
}

.hero-loc {
    color: #6b7280;
    font-size: 0.88rem;
    margin: 0 0 28px;
}

.hero-social {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
}

.hero-social a {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #1a1a2e;
    color: #65B581;
    border: 1px solid rgba(24, 153, 11, 0.4);
    border-radius: 8px;
    padding: 8px 20px;
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.hero-social a:hover {
    background: #18990b;
    color: white;
    border-color: #18990b;
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(24, 153, 11, 0.25);
}

/* ---- SECTION HEADING ---- */
.sec-heading {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f0f0f0;
    padding-left: 14px;
    border-left: 4px solid #18990b;
    margin: 0 0 20px;
    line-height: 1.3;
}

/* ---- ABOUT ---- */
.about-text {
    color: #d1d5db;
    font-size: 1rem;
    line-height: 1.85;
}

/* ---- METRICS ---- */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 8px;
}

.metric-box {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 12px;
    padding: 22px 16px;
    text-align: center;
}

.metric-box .val {
    font-size: 2rem;
    font-weight: 800;
    color: #18990b;
    line-height: 1;
}

.metric-box .lbl {
    color: #6b7280;
    font-size: 0.82rem;
    margin-top: 6px;
    font-weight: 500;
}

/* ---- SKILL PILLS ---- */
.skills-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 8px;
}

.skill-pill {
    background: rgba(24, 153, 11, 0.1);
    color: #65B581;
    border: 1px solid rgba(24, 153, 11, 0.3);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.85rem;
    font-weight: 500;
    display: inline-block;
    transition: all 0.2s;
}

.skill-pill:hover {
    background: rgba(24, 153, 11, 0.22);
    border-color: #18990b;
}

/* ---- TECH BADGES (com ícones) ---- */
.tech-badge {
    display: inline-block;
    background: rgba(24, 153, 11, 0.1);
    color: #65B581;
    border: 1px solid rgba(24, 153, 11, 0.3);
    border-radius: 16px;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 500;
    margin-right: 6px;
    margin-bottom: 4px;
    transition: all 0.2s;
}

.tech-badge:hover {
    background: rgba(24, 153, 11, 0.22);
    border-color: #18990b;
}

/* ---- PROJECT GRID ---- */
.proj-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
    gap: 18px;
    margin-bottom: 8px;
}

.proj-card {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 14px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: all 0.25s ease;
}

.proj-card:hover {
    border-color: #18990b;
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(24, 153, 11, 0.12);
}

.proj-thumb {
    width: 100%;
    height: 140px;
    background: linear-gradient(135deg, #0d3320 0%, #1a1a2e 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
}

.proj-body {
    padding: 20px 22px 22px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex-grow: 1;
}

.proj-cat {
    display: inline-block;
    background: rgba(24, 153, 11, 0.15);
    color: #65B581;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.2px;
    width: fit-content;
}

.proj-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f0f0f0;
    margin: 0;
    line-height: 1.4;
}

.proj-desc {
    color: #9ca3af;
    font-size: 0.87rem;
    line-height: 1.65;
    margin: 0;
    flex-grow: 1;
}

.proj-techs {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.proj-tech {
    background: #0e1117;
    color: #65B581;
    border: 1px solid #2a2a4e;
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 0.76rem;
    font-weight: 500;
}

.proj-metrics {
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 10px 13px;
    font-size: 0.81rem;
    color: #9ca3af;
    line-height: 1.65;
}

.proj-metrics strong { color: #18990b; }

.proj-links {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: auto;
}

.proj-btn {
    display: inline-block;
    background: #18990b;
    color: white !important;
    border-radius: 8px;
    padding: 7px 18px;
    text-decoration: none !important;
    font-size: 0.83rem;
    font-weight: 600;
    transition: background 0.2s;
}

.proj-btn:hover { background: #14840a; }

.proj-btn.outline {
    background: transparent;
    color: #65B581 !important;
    border: 1px solid #65B581;
}

.proj-btn.outline:hover { background: rgba(101, 181, 129, 0.1); }

/* ---- EXPERIENCE ITEMS ---- */
.exp-item {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-left: 4px solid #18990b;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 14px;
}

.exp-period {
    color: #65B581;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 4px;
}

.exp-role {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f0f0f0;
    margin: 0 0 2px;
}

.exp-company {
    color: #9ca3af;
    font-size: 0.88rem;
    margin-bottom: 12px;
}

.exp-bullets {
    color: #d1d5db;
    font-size: 0.87rem;
    line-height: 1.75;
    padding-left: 18px;
    margin: 0;
}

/* ---- EDUCATION CARDS ---- */
.edu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
    margin-bottom: 8px;
}

.edu-card {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 12px;
    padding: 22px;
    height: 100%;
    transition: border-color 0.18s ease, transform 0.18s ease;
}

/* Card de certificação clicável (quando há URL) */
.edu-card-link {
    text-decoration: none;
    display: block;
    height: 100%;
}

.edu-card-link:hover .edu-card {
    border-color: #18990b;
    transform: translateY(-2px);
}

.edu-degree {
    font-size: 1rem;
    font-weight: 700;
    color: #f0f0f0;
    margin-bottom: 5px;
}

.edu-school {
    color: #65B581;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 4px;
}

.edu-period {
    color: #6b7280;
    font-size: 0.8rem;
}

/* ---- CARD INTERNALS (dentro de st.container) ---- */

/* Remove margem extra do markdown dentro dos cards */
.proj-techs { margin-top: 6px; margin-bottom: 6px; }

.proj-metrics {
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.82rem;
    color: #9ca3af;
    line-height: 1.65;
    margin-top: 6px;
    margin-bottom: 8px;
}

.proj-metrics strong { color: #18990b; }

/* Thumbnail dentro de container (não CSS grid) */
.proj-thumb {
    width: 100%;
    height: 260px;
    background: linear-gradient(135deg, #0d3320 0%, #1a1a2e 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 44px;
    border-radius: 8px;
    margin-bottom: 12px;
}

/* ---- PROJECT CARD UNIFORM HEIGHT ---- */
/* As colunas de uma mesma linha esticam até a altura da mais alta */
[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}

/* Cada coluna vira uma flex-column ocupando toda a altura da linha */
[data-testid="stColumn"] {
    display: flex;
    flex-direction: column;
}

/* Cadeia de wrappers (coluna → bloco → layout-wrapper → card com borda)
   cresce para que o card preencha 100% da altura da coluna. O combinador de
   filho direto (>) garante que só a cadeia externa estica — os wrappers
   internos dos botões e do expander não são afetados. */
[data-testid="stColumn"] > [data-testid="stVerticalBlock"],
[data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
}

[data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"] {
    flex: 1 1 auto;
}

/* ---- MISC ---- */
footer { visibility: hidden; }
</style>
"""


def inject_css():
    st.markdown(PORTFOLIO_CSS, unsafe_allow_html=True)
