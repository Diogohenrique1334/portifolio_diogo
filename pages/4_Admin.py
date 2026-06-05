import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

from utils.sidebar import render_sidebar
from utils.styles import inject_css
from utils.admin_helpers import (
    carregar_projetos,
    salvar_projetos,
    carregar_experiencias,
    salvar_experiencias,
    validar_projeto,
    validar_experiencia,
)

st.set_page_config(
    page_title="Admin — Portfólio",
    page_icon="⚙️",
    layout="wide",
)

inject_css()

# ================================================================
# AUTENTICAÇÃO
# ================================================================
SENHA_ADMIN = os.getenv("PORTFOLIO_ADMIN_PASSWORD")

# Tenta carregar de st.secrets se não estiver em .env
if not SENHA_ADMIN:
    try:
        SENHA_ADMIN = st.secrets.get("portfolio_admin_password")
    except (FileNotFoundError, Exception):
        SENHA_ADMIN = None

if not SENHA_ADMIN:
    st.error(
        "⚠️ Painel admin desabilitado. Configure `PORTFOLIO_ADMIN_PASSWORD` "
        "para habilitar (variável de ambiente ou Streamlit Secrets)."
    )
    st.stop()

if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False

if not st.session_state.admin_autenticado:
    render_sidebar()
    st.markdown('<p class="sec-heading">🔐 Admin — Acesso restrito</p>', unsafe_allow_html=True)

    senha = st.text_input("Senha do admin", type="password")
    if st.button("Entrar"):
        if senha == SENHA_ADMIN:
            st.session_state.admin_autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta")
    st.stop()

# ================================================================
# PAINEL ADMIN (autenticado)
# ================================================================
render_sidebar()

col_titulo, col_logout = st.columns([10, 1])
with col_titulo:
    st.markdown('<p class="sec-heading">⚙️ Painel de Administração</p>', unsafe_allow_html=True)
with col_logout:
    if st.button("🚪 Sair"):
        st.session_state.admin_autenticado = False
        st.rerun()

st.divider()

# Abas
tab_projetos, tab_experiencia, tab_perfil = st.tabs(
    ["📦 Projetos", "💼 Experiência", "👤 Perfil"]
)

# ================================================================
# ABA: PROJETOS
# ================================================================
with tab_projetos:
    st.markdown("### Gerenciar Projetos")
    projetos = carregar_projetos()

    # Listar projetos
    st.write(f"**Total: {len(projetos)} projeto(s)**")

    # Cria pasta de assets se não existir
    assets_dir = Path(__file__).parent.parent / "assets" / "projetos"
    assets_dir.mkdir(parents=True, exist_ok=True)

    for i, p in enumerate(projetos):
        with st.expander(f"📌 {p['titulo']}", expanded=False):
            col1, col2 = st.columns([5, 1])

            with col1:
                novo_titulo = st.text_input(
                    "Título", p.get("titulo", ""), key=f"p_titulo_{i}"
                )
                nova_categoria = st.selectbox(
                    "Categoria",
                    [
                        "Computer Vision",
                        "Análise de Dados",
                        "Machine Learning",
                        "NLP",
                        "Engenharia de Dados",
                        "Produto de Dados",
                    ],
                    index=0,
                    key=f"p_cat_{i}",
                )
                nova_descricao = st.text_area(
                    "Descrição (técnica)", p.get("descricao", ""), key=f"p_desc_{i}"
                )
                nova_desc_longa = st.text_area(
                    "Descrição longa (para leitor não técnico)",
                    p.get("descricao_longa", ""),
                    key=f"p_desclonga_{i}",
                )
                novo_impacto = st.text_area(
                    "Impacto (frase sobre o resultado)",
                    p.get("impacto", ""),
                    key=f"p_impact_{i}",
                )
                nova_stack = st.text_area(
                    "Stack (separado por vírgula)",
                    ", ".join(p.get("stack", [])),
                    key=f"p_stack_{i}",
                )
                novo_github = st.text_input(
                    "GitHub URL", p.get("github", ""), key=f"p_gh_{i}"
                )
                novo_destaque = st.checkbox(
                    "Destacar?", p.get("destaque", True), key=f"p_dest_{i}"
                )

                # Upload de foto
                st.markdown("**Foto do projeto**")
                foto_atual = p.get("imagem")
                if foto_atual:
                    st.caption(f"Foto atual: {foto_atual}")
                arquivo_foto = st.file_uploader(
                    "Fazer upload de nova foto (PNG/JPG)",
                    type=["png", "jpg", "jpeg"],
                    key=f"p_foto_{i}",
                )

                if st.button("💾 Salvar alterações", key=f"save_p_{i}"):
                    # Salva foto se foi feito upload
                    nome_foto = foto_atual
                    if arquivo_foto:
                        # Gera nome do arquivo: titulo_projeto.extensao
                        ext = arquivo_foto.name.split(".")[-1]
                        nome_foto = f"{novo_titulo.lower().replace(' ', '_').replace('—', '')[:30]}.{ext}"
                        foto_path = assets_dir / nome_foto
                        foto_path.write_bytes(arquivo_foto.getbuffer())

                    projetos[i].update(
                        {
                            "titulo": novo_titulo,
                            "categoria": nova_categoria,
                            "descricao": nova_descricao,
                            "descricao_longa": nova_desc_longa,
                            "impacto": novo_impacto,
                            "stack": [s.strip() for s in nova_stack.split(",") if s.strip()],
                            "github": novo_github or None,
                            "destaque": novo_destaque,
                            "imagem": nome_foto,
                        }
                    )
                    salvar_projetos(projetos)
                    st.success("✅ Projeto atualizado!")
                    st.rerun()

            with col2:
                if st.button("🗑️", key=f"del_p_{i}", help="Deletar projeto"):
                    projetos.pop(i)
                    salvar_projetos(projetos)
                    st.success("✅ Projeto removido!")
                    st.rerun()

    # Adicionar novo projeto
    st.markdown("### ➕ Novo Projeto")
    with st.form("novo_projeto"):
        novo_titulo = st.text_input("Título")
        nova_categoria = st.selectbox(
            "Categoria",
            [
                "Computer Vision",
                "Análise de Dados",
                "Machine Learning",
                "NLP",
                "Engenharia de Dados",
                "Produto de Dados",
            ],
        )
        nova_descricao = st.text_area("Descrição (técnica)")
        nova_descricao_longa = st.text_area("Descrição longa (opcional)")
        novo_impacto = st.text_area("Impacto (opcional)")
        nova_stack_str = st.text_input("Stack (separado por vírgula)")
        novo_github = st.text_input("GitHub URL (opcional)")
        novo_destaque = st.checkbox("Destacar?", True)
        arquivo_foto = st.file_uploader(
            "Foto do projeto (PNG/JPG - opcional)",
            type=["png", "jpg", "jpeg"],
            key="novo_proj_foto",
        )

        if st.form_submit_button("➕ Adicionar Projeto"):
            # Salva foto se foi feito upload
            nome_foto = None
            if arquivo_foto:
                ext = arquivo_foto.name.split(".")[-1]
                nome_foto = f"{novo_titulo.lower().replace(' ', '_').replace('—', '')[:30]}.{ext}"
                foto_path = assets_dir / nome_foto
                foto_path.write_bytes(arquivo_foto.getbuffer())

            novo_proj = {
                "titulo": novo_titulo,
                "categoria": nova_categoria,
                "descricao": nova_descricao,
                "descricao_longa": nova_descricao_longa,
                "impacto": novo_impacto,
                "stack": [s.strip() for s in nova_stack_str.split(",") if s.strip()],
                "metricas": {},
                "imagem": nome_foto,
                "github": novo_github or None,
                "demo": None,
                "destaque": novo_destaque,
            }
            if validar_projeto(novo_proj):
                projetos.append(novo_proj)
                salvar_projetos(projetos)
                st.success("✅ Projeto criado!")
                st.rerun()
            else:
                st.error("❌ Preencha todos os campos obrigatórios")

# ================================================================
# ABA: EXPERIÊNCIA
# ================================================================
with tab_experiencia:
    st.markdown("### Gerenciar Experiências")
    dados_exp = carregar_experiencias()
    experiencias = dados_exp.get("experiencias", [])

    st.write(f"**Experiências: {len(experiencias)}**")
    for i, exp in enumerate(experiencias):
        with st.expander(f"💼 {exp['cargo']} — {exp['empresa']}", expanded=False):
            novo_periodo = st.text_input(
                "Período", exp.get("periodo", ""), key=f"exp_periodo_{i}"
            )
            novo_cargo = st.text_input("Cargo", exp.get("cargo", ""), key=f"exp_cargo_{i}")
            nova_empresa = st.text_input(
                "Empresa", exp.get("empresa", ""), key=f"exp_emp_{i}"
            )
            novo_local = st.text_input("Local", exp.get("local", ""), key=f"exp_loc_{i}")
            novos_bullets = st.text_area(
                "Bullets (uma por linha)",
                "\n".join(exp.get("bullets", [])),
                key=f"exp_bull_{i}",
            )

            col_save, col_del = st.columns(2)
            with col_save:
                if st.button("💾 Salvar", key=f"save_exp_{i}"):
                    experiencias[i].update(
                        {
                            "periodo": novo_periodo,
                            "cargo": novo_cargo,
                            "empresa": nova_empresa,
                            "local": novo_local,
                            "bullets": [b.strip() for b in novos_bullets.split("\n") if b.strip()],
                        }
                    )
                    dados_exp["experiencias"] = experiencias
                    salvar_experiencias(dados_exp)
                    st.success("✅ Experiência atualizada!")
                    st.rerun()

            with col_del:
                if st.button("🗑️ Deletar", key=f"del_exp_{i}"):
                    experiencias.pop(i)
                    dados_exp["experiencias"] = experiencias
                    salvar_experiencias(dados_exp)
                    st.success("✅ Experiência removida!")
                    st.rerun()

    # Adicionar experiência
    st.markdown("### ➕ Nova Experiência")
    with st.form("nova_experiencia"):
        novo_periodo = st.text_input("Período (ex: 2022 – Presente)")
        novo_cargo = st.text_input("Cargo")
        nova_empresa = st.text_input("Empresa")
        novo_local = st.text_input("Local")
        novos_bullets = st.text_area("Bullets (uma por linha)")

        if st.form_submit_button("➕ Adicionar Experiência"):
            nova_exp = {
                "periodo": novo_periodo,
                "cargo": novo_cargo,
                "empresa": nova_empresa,
                "local": novo_local,
                "bullets": [b.strip() for b in novos_bullets.split("\n") if b.strip()],
            }
            if validar_experiencia(nova_exp):
                experiencias.append(nova_exp)
                dados_exp["experiencias"] = experiencias
                salvar_experiencias(dados_exp)
                st.success("✅ Experiência criada!")
                st.rerun()
            else:
                st.error("❌ Preencha todos os campos obrigatórios")

# ================================================================
# ABA: PERFIL
# ================================================================
with tab_perfil:
    st.markdown("### Editar Perfil")

    from utils.admin_helpers import carregar_perfil, salvar_perfil

    perfil = carregar_perfil()

    with st.form("editar_perfil"):
        novo_nome = st.text_input("Nome", perfil.get("nome", ""))
        novo_cargo = st.text_input("Cargo", perfil.get("cargo", ""))
        nova_empresa = st.text_input("Empresa", perfil.get("empresa", ""))
        nova_localizacao = st.text_input("Localização", perfil.get("localizacao", ""))
        nova_tagline = st.text_area("Tagline Sidebar", perfil.get("tagline_sidebar", ""))
        novo_anos = st.number_input("Anos de experiência", perfil.get("anos_experiencia", 8))
        novo_linkedin = st.text_input("LinkedIn URL", perfil.get("linkedin", ""))
        novo_github = st.text_input("GitHub URL", perfil.get("github", ""))
        novo_portfolio = st.text_input("Portfólio URL", perfil.get("portfolio", ""))
        novo_email = st.text_input("Email", perfil.get("email", ""))

        if st.form_submit_button("💾 Salvar Perfil"):
            perfil.update(
                {
                    "nome": novo_nome,
                    "cargo": novo_cargo,
                    "empresa": nova_empresa,
                    "localizacao": nova_localizacao,
                    "tagline_sidebar": nova_tagline,
                    "anos_experiencia": novo_anos,
                    "linkedin": novo_linkedin,
                    "github": novo_github,
                    "portfolio": novo_portfolio,
                    "email": novo_email,
                }
            )
            salvar_perfil(perfil)
            st.success("✅ Perfil atualizado!")
            st.rerun()

    # ---- Currículo tradicional (anexo para download) ----
    st.markdown("### Currículo tradicional (anexo)")
    assets_root = Path(__file__).parent.parent / "assets"
    assets_root.mkdir(parents=True, exist_ok=True)

    curriculos_existentes = [
        nome for nome in ("curriculo.pdf", "curriculo.docx")
        if (assets_root / nome).exists()
    ]
    if curriculos_existentes:
        st.caption(f"Currículo atual: {', '.join(curriculos_existentes)}")
    else:
        st.caption("Nenhum currículo enviado ainda.")

    arquivo_cv = st.file_uploader(
        "Enviar currículo (PDF ou DOCX)",
        type=["pdf", "docx"],
        key="cv_upload",
    )
    col_cv_save, col_cv_del = st.columns(2)
    with col_cv_save:
        if st.button("💾 Salvar currículo", key="save_cv"):
            if arquivo_cv:
                ext = arquivo_cv.name.split(".")[-1].lower()
                destino = assets_root / f"curriculo.{ext}"
                destino.write_bytes(arquivo_cv.getbuffer())
                st.success(f"✅ Currículo salvo como curriculo.{ext}")
                st.rerun()
            else:
                st.error("❌ Selecione um arquivo PDF ou DOCX primeiro")
    with col_cv_del:
        if st.button("🗑️ Remover currículo", key="del_cv"):
            removidos = 0
            for nome in ("curriculo.pdf", "curriculo.docx"):
                caminho = assets_root / nome
                if caminho.exists():
                    caminho.unlink()
                    removidos += 1
            if removidos:
                st.success("✅ Currículo removido")
                st.rerun()
            else:
                st.info("Nenhum currículo para remover")

    # ---- Certificações ----
    st.markdown("### Gerenciar Certificações")
    certificacoes = dados_exp.get("certificacoes", [])

    st.write(f"**Certificações: {len(certificacoes)}**")
    for i, cert in enumerate(certificacoes):
        with st.expander(f"🏆 {cert['nome']}", expanded=False):
            novo_nome = st.text_input(
                "Nome", cert.get("nome", ""), key=f"cert_nome_{i}"
            )
            nova_inst = st.text_input(
                "Instituição", cert.get("instituicao", ""), key=f"cert_inst_{i}"
            )
            novo_ano = st.text_input("Ano", cert.get("ano", ""), key=f"cert_ano_{i}")
            nova_desc = st.text_area(
                "Descrição (opcional)",
                cert.get("descricao", ""),
                key=f"cert_desc_{i}",
            )
            nova_url = st.text_input(
                "URL do certificado (opcional)",
                cert.get("url", ""),
                key=f"cert_url_{i}",
            )

            col_save, col_del = st.columns(2)
            with col_save:
                if st.button("💾 Salvar", key=f"save_cert_{i}"):
                    certificacoes[i].update(
                        {
                            "nome": novo_nome,
                            "instituicao": nova_inst,
                            "ano": novo_ano,
                            "descricao": nova_desc,
                            "url": nova_url or None,
                        }
                    )
                    dados_exp["certificacoes"] = certificacoes
                    salvar_experiencias(dados_exp)
                    st.success("✅ Certificação atualizada!")
                    st.rerun()

            with col_del:
                if st.button("🗑️ Deletar", key=f"del_cert_{i}"):
                    certificacoes.pop(i)
                    dados_exp["certificacoes"] = certificacoes
                    salvar_experiencias(dados_exp)
                    st.success("✅ Certificação removida!")
                    st.rerun()

    # Adicionar certificação
    st.markdown("### ➕ Nova Certificação")
    with st.form("nova_certificacao"):
        novo_nome = st.text_input("Nome")
        nova_inst = st.text_input("Instituição")
        novo_ano = st.text_input("Ano")
        nova_desc = st.text_area("Descrição (opcional)")
        nova_url = st.text_input("URL do certificado (opcional)")

        if st.form_submit_button("➕ Adicionar Certificação"):
            nova_cert = {
                "nome": novo_nome,
                "instituicao": nova_inst,
                "ano": novo_ano,
                "descricao": nova_desc,
                "url": nova_url or None,
            }
            if novo_nome and nova_inst and novo_ano:
                certificacoes.append(nova_cert)
                dados_exp["certificacoes"] = certificacoes
                salvar_experiencias(dados_exp)
                st.success("✅ Certificação criada!")
                st.rerun()
            else:
                st.error("❌ Preencha nome, instituição e ano")

    st.divider()
    st.info(
        "💡 **Dica:** Configure a senha do admin nas Streamlit Secrets "
        "(Streamlit Cloud) ou variável de ambiente `PORTFOLIO_ADMIN_PASSWORD`"
    )
