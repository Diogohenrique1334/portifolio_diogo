"""Integração opcional com o banco do projeto Diagnóstico (Neon).

Enriquece o corpus do agente com a trajetória de execução do Diogo (50+ projetos).
A segurança é por **allowlist**: só projetos cuja empresa estiver explicitamente
liberada (`DIAGNOSTICO_EMPRESAS_DETALHE`) são expostos em detalhe; todo o resto —
inclusive empresa desconhecida ou nova — entra **apenas em forma agregada** (sem
nomes, e-mails, clientes ou texto livre). Assim, dado profissional/confidencial nunca
vaza por omissão.

Os enums do Diagnóstico são gravados como o *nome* do membro (native_enum=False),
então no banco aparecem como ``VISAO_COMPUTACIONAL``, ``FINALIZADO`` etc.
"""

from __future__ import annotations

from collections import Counter
from contextlib import closing

import psycopg2

from agente.config import AgenteConfig
from agente.corpus import Documento

_STATUS_FINALIZADO = "FINALIZADO"


def _humanizar(nome: str | None) -> str:
    """'VISAO_COMPUTACIONAL' → 'Visao Computacional'. None → 'Não informado'."""
    if not nome:
        return "Não informado"
    return nome.replace("_", " ").strip().title()


def _conectar(url: str):
    return psycopg2.connect(url)


def _carregar(url: str) -> dict:
    """Lê projetos (+ empresa), frequência de skills e durações do Diagnóstico."""
    with closing(_conectar(url)) as conn, conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id, p.nome_projeto, p.objetivo,
                       p.tipo_projeto, p.status_projeto, c.empresa
                FROM projetos p
                LEFT JOIN clientes c ON c.id = p.id_cliente;
                """
            )
            projetos = [
                {
                    "id": r[0],
                    "nome": r[1],
                    "objetivo": r[2],
                    "tipo": r[3],
                    "status": r[4],
                    "empresa": r[5],
                }
                for r in cur.fetchall()
            ]

            cur.execute(
                "SELECT skill, COUNT(*) FROM projeto_skill GROUP BY skill ORDER BY COUNT(*) DESC;"
            )
            skills_freq = cur.fetchall()

            cur.execute(
                """
                SELECT id_projeto,
                       MIN(data_mudanca) AS inicio,
                       MAX(CASE WHEN status_novo = %s THEN data_mudanca END) AS fim
                FROM historico_status_projeto
                GROUP BY id_projeto;
                """,
                (_STATUS_FINALIZADO,),
            )
            duracoes = {}
            for id_proj, inicio, fim in cur.fetchall():
                if inicio and fim:
                    duracoes[id_proj] = max((fim - inicio).days, 0)

            # skills por projeto (só usado nos documentos detalhados)
            cur.execute("SELECT id_projeto, skill FROM projeto_skill;")
            skills_por_projeto: dict[int, list[str]] = {}
            for id_proj, skill in cur.fetchall():
                skills_por_projeto.setdefault(id_proj, []).append(skill)

    return {
        "projetos": projetos,
        "skills_freq": skills_freq,
        "duracoes": duracoes,
        "skills_por_projeto": skills_por_projeto,
    }


def _docs_agregados(dados: dict) -> list[Documento]:
    """Fatos agregados sobre TODOS os projetos — sem nomes/PII. Sempre seguros."""
    projetos = dados["projetos"]
    duracoes = dados["duracoes"]
    total = len(projetos)
    finalizados = sum(1 for p in projetos if p["status"] == _STATUS_FINALIZADO)
    por_tipo = Counter(_humanizar(p["tipo"]) for p in projetos)

    resumo = (
        "Trajetória de execução de projetos (visão agregada, sem identificação).\n"
        f"Total de projetos trabalhados: {total}\n"
        f"Projetos finalizados: {finalizados}\n"
        f"Projetos em andamento ou outros status: {total - finalizados}\n"
        "Distribuição por tipo:\n"
        + "".join(f"- {tipo}: {qtd}\n" for tipo, qtd in por_tipo.most_common())
    )
    docs = [
        Documento(
            id="diag-resumo",
            tipo="diagnostico-agregado",
            titulo="Resumo da trajetória de projetos",
            texto=resumo,
        )
    ]

    if dados["skills_freq"]:
        texto_skills = "Skills mais usadas nos projetos (frequência):\n" + "".join(
            f"- {skill}: {qtd} projeto(s)\n" for skill, qtd in dados["skills_freq"]
        )
        docs.append(
            Documento(
                id="diag-skills",
                tipo="diagnostico-agregado",
                titulo="Skills mais aplicadas",
                texto=texto_skills,
            )
        )

    if duracoes:
        valores = sorted(duracoes.values())
        media = sum(valores) / len(valores)
        mediana = valores[len(valores) // 2]
        texto_tempo = (
            "Tempo de execução dos projetos finalizados (em dias, da abertura ao "
            "status Finalizado):\n"
            f"- Projetos finalizados com duração medida: {len(valores)}\n"
            f"- Tempo médio: {media:.0f} dias\n"
            f"- Tempo mediano: {mediana} dias\n"
            f"- Mais rápido: {valores[0]} dias · Mais longo: {valores[-1]} dias\n"
        )
        docs.append(
            Documento(
                id="diag-tempo",
                tipo="diagnostico-agregado",
                titulo="Tempo médio de execução",
                texto=texto_tempo,
            )
        )

    return docs


def _docs_detalhados(dados: dict, empresas_detalhe: set[str]) -> list[Documento]:
    """Documentos por projeto — SÓ para empresas na allowlist (acadêmico/hobby)."""
    if not empresas_detalhe:
        return []
    docs = []
    for p in dados["projetos"]:
        empresa = (p["empresa"] or "").strip().lower()
        if empresa not in empresas_detalhe:
            continue  # fail-safe: fora da allowlist → não detalha
        skills = ", ".join(dados["skills_por_projeto"].get(p["id"], []))
        texto = (
            "Projeto da trajetória (acadêmico/pessoal).\n"
            f"Nome: {p['nome']}\n"
            f"Tipo: {_humanizar(p['tipo'])}\n"
            f"Status: {_humanizar(p['status'])}\n"
        )
        if p["objetivo"]:
            texto += f"Objetivo: {p['objetivo']}\n"
        if skills:
            texto += f"Skills: {skills}\n"
        docs.append(
            Documento(
                id=f"diag-proj-{p['id']}",
                tipo="diagnostico-projeto",
                titulo=p["nome"],
                texto=texto,
            )
        )
    return docs


def construir_documentos_diagnostico(cfg: AgenteConfig) -> list[Documento]:
    """Documentos do Diagnóstico para o índice. Vazio se o banco não estiver configurado."""
    url = cfg.diagnostico_url_libpq()
    if not url:
        return []
    dados = _carregar(url)
    return _docs_agregados(dados) + _docs_detalhados(dados, cfg.empresas_detalhe())


def auditar(cfg: AgenteConfig) -> str:
    """Relatório legível do que será exposto — rode ANTES de indexar.

    Mostra as empresas presentes (e quantos projetos cada uma tem), quais entram em
    DETALHE (allowlist) e confirma que o restante é só agregado.
    """
    url = cfg.diagnostico_url_libpq()
    if not url:
        return "DIAGNOSTICO_DATABASE_URL não configurado — integração desligada."

    dados = _carregar(url)
    allowlist = cfg.empresas_detalhe()
    por_empresa = Counter((p["empresa"] or "—(sem empresa)").strip() for p in dados["projetos"])

    linhas = ["=== Auditoria de exposição do Diagnóstico ===", ""]
    linhas.append(f"Total de projetos: {len(dados['projetos'])}")
    linhas.append(f"Allowlist (detalhe) configurada: {sorted(allowlist) or '— vazia (tudo agregado)'}")
    linhas.append("")
    linhas.append("Empresas encontradas (nº de projetos) → modo:")
    for empresa, qtd in por_empresa.most_common():
        modo = "DETALHE" if empresa.strip().lower() in allowlist else "agregado"
        linhas.append(f"  - {empresa}: {qtd} → {modo}")

    detalhados = [
        p["nome"]
        for p in dados["projetos"]
        if (p["empresa"] or "").strip().lower() in allowlist
    ]
    linhas.append("")
    linhas.append(f"Projetos que seriam expostos EM DETALHE ({len(detalhados)}):")
    linhas += [f"  - {nome}" for nome in detalhados] or ["  (nenhum)"]
    linhas.append("")
    linhas.append("Todo o restante entra apenas em forma agregada (sem nomes/PII).")
    return "\n".join(linhas)


def main() -> None:
    """CLI de auditoria: ``python -m agente.diagnostico``."""
    from dotenv import load_dotenv

    load_dotenv()
    print(auditar(AgenteConfig()))


if __name__ == "__main__":
    main()
