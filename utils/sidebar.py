import json
import streamlit as st
from pathlib import Path


@st.cache_data
def _carregar_perfil() -> dict:
    path = Path(__file__).parent.parent / "data" / "perfil.json"
    return json.loads(path.read_text(encoding="utf-8"))


def render_sidebar():
    """Sidebar com foto, nome, tagline e links de contato — tudo lido do perfil.json."""
    perfil = _carregar_perfil()
    foto_path = Path(__file__).parent.parent / "assets" / "foto.png"

    with st.sidebar:
        # Foto ou avatar
        if foto_path.exists():
            import base64
            img_bytes = foto_path.read_bytes()
            img_b64 = base64.b64encode(img_bytes).decode()
            avatar_html = f'<img src="data:image/png;base64,{img_b64}" style="width:140px;height:140px;border-radius:50%;object-fit:cover;display:block;margin:0 auto 16px;border:4px solid rgba(24, 153, 11, 0.45);box-shadow:0 0 48px rgba(24, 153, 11, 0.22);">'
            st.markdown(avatar_html, unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div style="
                    width:100px; height:100px; border-radius:50%;
                    background:linear-gradient(135deg,#18990b,#65B581);
                    display:flex; align-items:center; justify-content:center;
                    font-size:36px; font-weight:800; color:white;
                    margin:0 auto 16px;
                    border: 4px solid rgba(24, 153, 11, 0.45);
                    box-shadow: 0 0 48px rgba(24, 153, 11, 0.22);">
                    DO
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(f"### {perfil['nome']}")
        st.caption(f"{perfil['cargo']} · {perfil['empresa']}")

        # Tagline — editável no perfil.json
        if perfil.get("tagline_sidebar"):
            st.markdown(
                f"""
                <p style="font-size:0.78rem; color:#9ca3af; line-height:1.5;
                           margin-top:2px; margin-bottom:0;">
                    {perfil['tagline_sidebar']}
                </p>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        st.markdown(
            f"""
            [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white&style=flat)]({perfil['linkedin']})
            [![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white&style=flat)]({perfil['github']})
            [![Email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white&style=flat)](mailto:{perfil['email']})
            """,
        )
