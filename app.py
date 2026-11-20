import json, os
from pathlib import Path
import pandas as pd
import streamlit as st
from src.core import CASES, AGES, explain, retrieve, evidence, rules
from src.storage import save_feedback
from src.generation import generate
from src.session import generate_result
from src.charts import contribution_spec

ROOT = Path(__file__).parent
st.set_page_config(
    page_title="Fundamento | Demonstração", page_icon="🔎", layout="wide"
)
# Segredos só são lidos no servidor, nunca colocados na interface.
for name in ["DATABASE_URL", "OLLAMA_URL", "OLLAMA_MODEL"]:
    try:
        if name in st.secrets:
            os.environ[name] = str(st.secrets[name])
    except FileNotFoundError:
        pass


def choose_appearance(value):
    st.session_state["appearance"] = value


def choose_page(value):
    st.session_state["navigation"] = value


st.session_state.setdefault("appearance", "Claro")
st.session_state.setdefault("navigation", "Análise")
appearance = st.session_state["appearance"]
dark = appearance == "Escuro"
colors = (
    {
        "bg": "#09272b",
        "surface": "#10373c",
        "raised": "#16454a",
        "text": "#eff9f7",
        "muted": "#b4cfce",
        "line": "#356064",
        "accent": "#7ee5bd",
        "button": "#008655",
        "onbutton": "#ffffff",
        "warning": "#463615",
        "warntext": "#ffe8ad",
        "info": "#163e43",
        "infotext": "#d2ece8",
        "side": "#062125",
    }
    if dark
    else {
        "bg": "#f6f8f7",
        "surface": "#ffffff",
        "raised": "#eef5f1",
        "text": "#123a2c",
        "muted": "#4f6a60",
        "line": "#d6e3dd",
        "accent": "#00794d",
        "button": "#00794d",
        "onbutton": "#ffffff",
        "warning": "#fff0cf",
        "warntext": "#654207",
        "info": "#eaf4ef",
        "infotext": "#244d3a",
        "side": "#005238",
    }
)
with st.container(key="topbar"):
    heading, theme_control = st.columns([3, 2])
    with heading:
        st.markdown(
            '<span class="f-badge">PROTÓTIPO ACADÊMICO</span>', unsafe_allow_html=True
        )
    with theme_control:
        with st.container(key="theme_buttons"):
            light_button, dark_button = st.columns(2, gap="small")
            light_button.button(
                "Claro",
                key="theme_light",
                type="primary" if not dark else "secondary",
                on_click=choose_appearance,
                args=("Claro",),
                width="stretch",
            )
            dark_button.button(
                "Escuro",
                key="theme_dark",
                type="primary" if dark else "secondary",
                on_click=choose_appearance,
                args=("Escuro",),
                width="stretch",
            )
css = (ROOT / "assets/theme.css").read_text(encoding="utf-8")
css = (
    css.replace(
        "__VARS__", ";".join("--" + k + ":" + v for k, v in colors.items()) + ";"
    )
    .replace("__SCHEME__", "dark" if dark else "light")
)
st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)
metrics = json.loads((ROOT / "assets/metrics.json").read_text(encoding="utf-8"))
with st.sidebar:
    st.markdown(
        '<div class="f-brand"><span class="f-symbol" aria-hidden="true"></span> Fundamento</div>',
        unsafe_allow_html=True,
    )
    with st.container(key="side_navigation"):
        for page, icon in [
            ("Análise", ":material/bar_chart:"),
            ("Evidências", ":material/menu_book:"),
            ("Método", ":material/science:"),
        ]:
            st.button(
                page,
                key="nav_" + page,
                icon=icon,
                width="stretch",
                type="primary"
                if st.session_state["navigation"] == page
                else "secondary",
                on_click=choose_page,
                args=(page,),
            )
    navigation = st.session_state["navigation"]
    st.divider()
    case = st.radio(
        "Perfil demonstrativo",
        list(CASES),
        index=1,
        format_func=lambda name: name.split(" —")[0],
        horizontal=True,
        key="profile_choice",
    )
    v = CASES[case]
    st.markdown(
        f"""<div class="f-profile">
    <div class="f-row"><span>Faixa etária</span><strong>{AGES[v["Age"] - 1]} anos</strong></div>
    <div class="f-row"><span>IMC</span><strong>{v["BMI"]} kg/m²</strong></div>
    <div class="f-row"><span>Atividade física¹</span><strong>{"Sim" if v["PhysActivity"] else "Não"}</strong></div>
    <div class="f-row"><span>Hipertensão relatada</span><strong>{"Sim" if v["HighBP"] else "Não"}</strong></div>
    </div>""",
        unsafe_allow_html=True,
    )
    st.caption("¹ Nos últimos 30 dias, fora do trabalho.")
    st.caption("Perfis fictícios. Não representam pacientes da Unimed.")
    analyze = st.button(
        "Analisar caso",
        type="primary",
        width="stretch",
        on_click=choose_page,
        args=("Análise",),
    )
    st.divider()
    st.caption(
        "Geração: "
        + (
            "conector configurado"
            if os.environ.get("OLLAMA_MODEL")
            else "modelo não configurado"
        )
    )
    st.caption("Expertise clínica: revisão especializada pendente.")
if st.session_state.get("case") != case:
    for k in ["result", "feedback_id", "generated", "generation_error"]:
        st.session_state.pop(k, None)
    st.session_state["case"] = case
if analyze or "result" not in st.session_state:
    for stale in ["generated", "generation_error", "feedback_id"]:
        st.session_state.pop(stale, None)
    st.session_state["feedback_revision"] = st.session_state.get("feedback_revision", 0) + 1
    with st.spinner("Calculando as contribuições e buscando evidências…"):
        result = explain(v)
        result["case"] = case
        result["inputs"] = v
        result["retrieved"] = {
            f["feature"]: retrieve(f["feature"]) for f in result["factors"]
        }
        result["rules_version"] = "0.1"
        st.session_state["result"] = result
if navigation == "Análise":
    if "result" not in st.session_state:
        st.markdown(
            """<div class="f-empty"><div class="f-eyebrow" >UMA EXPLICAÇÃO QUE VOCÊ PODE CONFERIR</div>
        <h3>Do resultado à evidência.</h3><p>Escolha um perfil fictício no painel lateral e clique em <strong>Analisar caso</strong> para explorar o resultado.</p>
        <div class="f-steps"><div class="f-step"><b>01 · Entenda</b>Veja quais fatores contribuíram para a saída do modelo.</div><div class="f-step"><b>02 · Confira</b>Consulte os trechos e as fontes de cada fator.</div><div class="f-step"><b>03 · Avalie</b>Identifique os limites e avalie a clareza da explicação.</div></div></div>""",
            unsafe_allow_html=True,
        )
    else:
        r = st.session_state["result"]
        st.title(f"{case.split(' —')[0]} · Resultado do modelo")
        threshold = metrics["threshold"]
        positive = r["score"] >= threshold
        label = "Classe 1" if positive else "Classe 0"
        comparison = "atingiu ou superou" if positive else "ficou abaixo de"
        cutoff = f"{threshold:.0%}"
        score_label = f"{r['score']:.1%}".replace(".", ",")
        st.markdown(
            f'<section class="prediction"><span>Classificação experimental do perfil fictício</span>'
            f'<h2>{label}</h2><p>O escore de <strong>{score_label}</strong> {comparison} o corte '
            f'de {cutoff} usado na avaliação do modelo.</p></section>',
            unsafe_allow_html=True,
        )
        st.caption("O modelo tenta reproduzir o rótulo histórico de diabetes da base. "
                   "Esta classificação não confirma nem exclui doença e não estima risco futuro.")
        activity = "com" if v["PhysActivity"] else "sem"
        pressure = "com" if v["HighBP"] else "sem"
        st.write(
            f"Perfil fictício de {AGES[v['Age'] - 1]} anos, com IMC de {v['BMI']} kg/m², "
            f"{activity} atividade física fora do trabalho nos últimos 30 dias e "
            f"{pressure} relato de hipertensão."
        )
        c1, c2 = st.columns(2)
        score_label = f"{r['score']:.1%}".replace(".", ",")
        base_label = f"{r['base']:.1%}".replace(".", ",")
        c1.metric("Registros positivos no grupo deste perfil", score_label)
        c2.metric("Registros positivos no treino completo", base_label)
        st.write(
            f"A árvore reuniu este perfil com registros históricos que seguiram as mesmas regras. "
            f"Nesse grupo, **{score_label}** dos registros de treino tinham o rótulo positivo "
            "da base de diabetes."
        )
        st.subheader("O que pesou no resultado?")
        strongest = r["factors"][0]
        direction = "acima" if strongest["contribution"] >= 0 else "abaixo"
        magnitude = f"{abs(strongest['contribution']) * 100:.2f}".replace(".", ",")
        st.write(
            f"**{strongest['label']}** teve o maior peso neste caso: sua contribuição foi de "
            f"**{magnitude} pontos percentuais {direction} da referência** de {base_label}. "
            "Os demais fatores também entram na soma."
        )
        supported = sum(bool(d) for d in r["retrieved"].values())
        st.caption(
            f"Abra um fator para consultar o contexto documental. Há fontes cadastradas para "
            f"{supported} dos {len(r['factors'])} fatores. Os valores em pontos percentuais vêm do modelo."
        )
        for f in r["factors"]:
            docs = r["retrieved"][f["feature"]]
            with st.expander(
                f"{f['label']} · {f['contribution'] * 100:+.2f} p.p. · "
                + ("contexto encontrado" if docs else "sem evidência na base"),
                expanded=False,
            ):
                if not docs:
                    st.warning(
                        "Não foi encontrada evidência elegível nesta base para fundamentar este fator. Isso não significa que a associação não exista, nem que o paciente não tenha doença."
                    )
                for d in docs:
                    st.write(d["summary"])
                    st.caption(
                        "Síntese documental cadastrada; não é texto gerado ao vivo."
                    )
                    st.markdown(f"**Trecho original:** “{d['excerpt']}”")
                    st.markdown(
                        f"[{d['id']} · {d['organization']} — abrir fonte]({d['url']})"
                    )
                    st.caption(
                        f"Seção: {d['section']} | revisão da página: {d['reviewed']} | consulta: {d['accessed']}"
                    )
        st.caption(
            "Fontes sobre diabetes tipo 2; a base do modelo não distingue tipos. Contexto documental geral, sem validação clínica. Revisão especializada pendente."
        )
        with st.expander("Ver gráfico de contribuições SHAP", expanded=False):
            chart = pd.DataFrame(
                {
                    "factor": [f["label"] for f in r["factors"]],
                    "contribution_pp": [
                        float(f["contribution"]) * 100 for f in r["factors"]
                    ],
                }
            )
            plot = chart.copy()
            plot["rank"] = range(len(plot))
            formatted = plot["contribution_pp"].map(lambda value: f"{value:+.2f}".replace(".", ","))
            plot["factor"] = plot["factor"] + "   " + formatted + " p.p."
            st.vega_lite_chart(plot, contribution_spec(colors), width="stretch", theme=None)
            with st.expander("Conferir valores das contribuições"):
                st.dataframe(
                    chart.rename(
                        columns={
                            "factor": "Fator",
                            "contribution_pp": "Contribuição (p.p.)",
                        }
                    ),
                    hide_index=True,
                    width="stretch",
                )
            st.caption(
                "Valores positivos aumentam a saída do modelo em relação à referência; negativos diminuem. A implementação verifica numericamente essa soma."
            )
        st.subheader("Explicação com fontes")
        if not os.environ.get("OLLAMA_MODEL"):
            st.write(
                "As fontes estão disponíveis acima. Para gerar um rascunho com IA, abra o aplicativo pelo iniciador com Ollama."
            )
        elif st.button(
            "Gerar rascunho com fontes", type="primary", icon=":material/auto_awesome:"
        ):
            with st.spinner("Gerando rascunhos para revisão…"):
                generate_result(st.session_state, generate)
                st.session_state["feedback_revision"] += 1
        if st.session_state.get("generation_error"):
            st.error(st.session_state["generation_error"])
        if st.session_state.get("generated"):
            st.warning(
                "Rascunho experimental: IDs de fontes foram conferidos; o suporte semântico e a correção clínica exigem revisão humana."
            )
            if not any(st.session_state["generated"].values()):
                st.info(
                    "O modelo não produziu afirmações com suporte suficiente. Confira as fontes acima."
                )
            for f, claims in st.session_state["generated"].items():
                for claim in claims:
                    st.write(
                        claim["text"] + " [" + ", ".join(claim["source_ids"]) + "]"
                    )
            r["generated_draft"] = st.session_state["generated"]
        st.subheader("Avalie a explicação")
        st.caption(
            "Avaliação acadêmica de clareza e rastreabilidade; não equivale a validação médica. Não informe dados pessoais."
        )
        with st.form(f"feedback_{st.session_state['feedback_revision']}"):
            rating = st.radio(
                "A apresentação permite conferir a explicação?",
                ["Concordo", "Discordo", "Não consigo avaliar"],
                horizontal=True,
                index=None,
            )
            comment = st.text_area("Comentário opcional", max_chars=500)
            submitted = st.form_submit_button("Salvar avaliação")
        if submitted and rating is None:
            st.warning("Selecione uma avaliação antes de salvar.")
        if submitted and rating is not None:
            try:
                st.session_state["feedback_id"] = save_feedback(r, rating, comment)
                st.success("Avaliação registrada.")
            except Exception:
                st.error(
                    "Não foi possível salvar. Nenhum sucesso de gravação foi confirmado."
                )
        if not os.environ.get("DATABASE_URL"):
            st.caption(
                "Nesta instalação, avaliações são salvas em SQLite local. Para persistência em hospedagem, configure PostgreSQL; arquivos locais podem ser descartados pela plataforma."
            )
        st.download_button(
            "Baixar registro deste caso",
            json.dumps(r, ensure_ascii=False, indent=2),
            "Fundamento_caso.json",
            "application/json",
        )
if navigation == "Evidências":
    st.title("Fontes documentais")
    st.write(
        "Três trechos curtos de uma fonte institucional. A ampliação da base e a revisão clínica estão pendentes."
    )
    for d in evidence():
        st.markdown(f"**{d['id']} — {d['title']}**")
        st.write(d["summary"])
        st.link_button("Consultar documento", d["url"])
        st.caption(d["status"])
    st.subheader("Camada de critérios — preparação para expertise")
    st.write(
        "As regras abaixo são de engenharia e rastreabilidade. Não representam conhecimento capturado e validado com médicos; não declaramos uma implementação clínica completa de XAG."
    )
    st.dataframe(pd.DataFrame(rules()), hide_index=True, width="stretch")
if navigation == "Método":
    m = metrics
    st.title("Como o modelo foi avaliado")
    st.write("Esta página resume o desempenho em registros históricos. Para ver a previsão do perfil selecionado, abra Análise.")
    st.button("Ver resultado do caso", on_click=choose_page, args=("Análise",))
    st.subheader("Acertos entre as previsões positivas")
    report = m["classification_report"]
    positive, sensitivity, specificity = st.columns(3)
    positive.metric("Precisão positiva", f"{report['1']['precision']:.2%}".replace(".", ","))
    sensitivity.metric("Sensibilidade", f"{report['1']['recall']:.2%}".replace(".", ","))
    specificity.metric("Especificidade", f"{report['0']['recall']:.2%}".replace(".", ","))
    false_positives = m["confusion_matrix"][0][1]
    true_positives = m["confusion_matrix"][1][1]
    st.write(
        f"Das {true_positives + false_positives} previsões positivas, "
        f"{true_positives} corresponderam à classe 1 observada."
    )
    with st.expander("Detalhes do treinamento e matriz de confusão"):
        st.write(
            "Árvore de decisão com profundidade máxima 4, quatro entradas e mínimo de 500 registros por folha. Divisão por grupos mantém perfis idênticos em apenas um lado do treino/teste."
        )
        a, b, c = st.columns(3)
        a.metric("Registros", f"{m['rows']:,}")
        b.metric("ROC AUC", f"{m['roc_auc']:.3f}")
        c.metric("Precisão média (AP)", f"{m['average_precision']:.3f}")
        st.caption(
            "ROC AUC mede ordenação; AP resume precisão e sensibilidade ao variar o limiar. Nenhuma dessas métricas prova calibração ou aptidão clínica."
        )
        st.write("**Rótulo:** " + m["target"])
        st.write(
            f"**Matriz de confusão, limiar {m['threshold']:.2f}:** linhas = rótulo observado; colunas = classe prevista."
        )
        st.caption(m["threshold_method"])
        st.dataframe(
            pd.DataFrame(
                m["confusion_matrix"],
                index=["Observado 0", "Observado 1"],
                columns=["Previsto 0", "Previsto 1"],
            )
        )
    for limit in m["limitations"]:
        st.write("• " + limit)
    st.link_button(
        "Metadados da base UCI",
        "https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators",
    )
    st.download_button(
        "Baixar métricas e proveniência",
        json.dumps(m, ensure_ascii=False, indent=2),
        "Fundamento_metricas.json",
        "application/json",
    )
    st.markdown(
        "**Ainda pendente:** conferir codificação original e licença, expandir fontes, revisar expertise, ampliar os testes de geração, conectar banco remoto, publicar e validar externamente."
    )

st.divider()
st.caption(
    "Fundamento · Projeto acadêmico independente · Sem validação clínica ou vínculo institucional oficial declarado."
)
