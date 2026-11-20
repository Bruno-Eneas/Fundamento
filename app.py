import json, os, base64, html
from pathlib import Path
import pandas as pd
import streamlit as st
from src.core import CASES, AGES, explain, retrieve, evidence, rules
from src.storage import save_feedback
from src.generation import generate
from src.session import generate_result
from src.charts import contribution_spec
from src.clinical import evaluate_labs, SOURCES
from src.lab_pdf import extract_labs_from_pdf
from src.patients import initialize_demo
from src.portal import render_patient, render_doctor

ROOT = Path(__file__).parent
st.set_page_config(
    page_title="Fundamento | Exames e evidências", page_icon="🌲", layout="wide"
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


def choose_role():
    if st.session_state["role"] == "Paciente demonstrativo":
        st.session_state["navigation"] = "Meu perfil"
    else:
        st.session_state["navigation"] = "Pacientes"


initialize_demo()
st.session_state.setdefault("appearance", "Claro")
st.session_state.setdefault("role", "Médico demonstrativo")
st.session_state.setdefault("navigation", "Exames")
appearance = st.session_state["appearance"]
dark = appearance == "Escuro"
colors = (
    {
        "bg": "#062f29", "surface": "#0a4235", "raised": "#0d4d3d",
        "text": "#f1fff7", "muted": "#b9dacc", "line": "#286f57",
        "accent": "#6fe3aa", "button": "#009e61", "onbutton": "#ffffff",
        "warning": "#49401c", "warntext": "#fff1bc", "warn-border": "#968139",
        "info": "#114d3f", "infotext": "#d5ffea", "side": "#03452f",
        "badge-bg": "#124c3d", "badge-text": "#e6fff2",
    }
    if dark
    else {
        "bg": "#fcfefd", "surface": "#f3fbf6", "raised": "#e8f7ee",
        "text": "#06432e", "muted": "#477766", "line": "#bfe4cf",
        "accent": "#007d4b", "button": "#007e4b", "onbutton": "#ffffff",
        "warning": "#fff5da", "warntext": "#654709", "warn-border": "#e9c969",
        "info": "#e9f8ef", "infotext": "#1f543b", "side": "#045538",
        "badge-bg": "#e6f6eb", "badge-text": "#065037",
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
hero_svg = (ROOT / "assets" / ("hero_dark.svg" if dark else "hero_light.svg")).read_bytes()
hero_data = base64.b64encode(hero_svg).decode("ascii")
css = (ROOT / "assets/theme.css").read_text(encoding="utf-8")
css = (
    css.replace(
        "__VARS__", ";".join("--" + k + ":" + v for k, v in colors.items()) + ";"
    )
    .replace("__SCHEME__", "dark" if dark else "light")
    .replace("__HERO__", hero_data)
)
st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)
metrics = json.loads((ROOT / "assets/metrics.json").read_text(encoding="utf-8"))
with st.sidebar:
    st.markdown(
        '<div class="f-brand"><span class="f-symbol" aria-hidden="true"></span> Fundamento</div>',
        unsafe_allow_html=True,
    )
    st.selectbox(
        "Visualizar como (acesso fictício, SEM login)",
        ["Médico demonstrativo", "Paciente demonstrativo"],
        key="role", on_change=choose_role,
    )
    with st.container(key="side_navigation"):
        pages = (
            [("Meu perfil", "Meu perfil e exames", ":material/person:")]
            if st.session_state["role"] == "Paciente demonstrativo" else
            [("Pacientes", "Pacientes e histórico", ":material/groups:"),
             ("Exames", "Laboratório demonstrativo", ":material/biotech:"),
             ("Análise", "Modelo experimental", ":material/bar_chart:"),
             ("Evidências", "Fontes e evidências", ":material/menu_book:"),
             ("Método", "Método e limites", ":material/science:")]
        )
        for page, label, icon in pages:
            st.button(
                label,
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
    if navigation == "Análise":
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
    else:
        st.caption("**Avaliação laboratorial**")
        st.caption("Use apenas exames fictícios ou anonimizados. Nenhum documento é salvo intencionalmente.")
        st.caption("Exames reais exigem proteção de dados e validação institucional.")

if navigation == "Análise":
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
            result["retrieved"] = {f["feature"]: retrieve(f["feature"]) for f in result["factors"]}
            result["rules_version"] = "0.1"
            st.session_state["result"] = result
if navigation == "Exames":
    st.markdown(
        '<section class="f-hero"><h1>Entenda seus exames de diabetes</h1>'
        '<p>Compare resultados laboratoriais com critérios públicos, confira as fontes e saiba quando faltam informações.</p></section>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="f-warning"><strong>ⓘ Demonstração acadêmica.</strong> '
        'Não é diagnóstico médico. Use somente resultados fictícios ou previamente anonimizados. '
        'A plataforma não calcula probabilidade clínica individual sem um modelo validado.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="f-title">01 · Informe os resultados</div>', unsafe_allow_html=True)
    st.caption('Preencha apenas os exames disponíveis; deixe os demais em branco. Confira unidades, datas e condições de coleta.')
    st.markdown('**Conheça primeiro com um caso fictício:**')
    ea, eb, ec = st.columns(3)
    demo_examples = {
        'A': {'glicemia_jejum': '90', 'hba1c': '5,3'},
        'B': {'glicemia_jejum': '132', 'hba1c': '6,8'},
        'C': {'glicemia_jejum': '94', 'hba1c': '6,7'},
    }
    chosen = None
    if ea.button('Exemplo A · Sem alteração', key='ex_A', width='stretch'):
        chosen = 'A'
    if eb.button('Exemplo B · Concordantes', key='ex_B', width='stretch'):
        chosen = 'B'
    if ec.button('Exemplo C · Discordantes', key='ex_C', width='stretch'):
        chosen = 'C'
    if chosen:
        for k in ['glicemia_jejum', 'hba1c', 'ttgo_1h', 'ttgo_2h', 'glicemia_casual']:
            st.session_state['lab_' + k] = demo_examples[chosen].get(k, '')
        st.session_state.pop('lab_result', None)
    with st.expander('Importar valores de PDF textual fictício (experimental)'):
        st.warning('Não envie documentos com nome, CPF, data de nascimento ou informações identificáveis. A leitura é local ao servidor e não usa IA externa.')
        document = st.file_uploader('PDF fictício e anonimizado de até 5 MB', type=['pdf'], key='lab_upload')
        if document and st.button('Ler rótulos e valores do PDF', key='read_lab_pdf'):
            try:
                found, notices = extract_labs_from_pdf(document.getvalue())
                for n in notices:
                    st.info(n)
                if found:
                    st.write('Valores identificados (confira antes de analisar):')
                    st.write(found)
                    for k, val in found.items():
                        st.session_state['lab_'+k] = str(val).replace('.', ',')
                    st.session_state.pop('lab_result',None)
            except ValueError as e:
                st.error(str(e))
    with st.form('exam_form'):
        f1, f2 = st.columns(2)
        f1.text_input('Glicemia plasmática em jejum (mg/dL)', placeholder='Ex.: 102', key='lab_glicemia_jejum')
        f2.text_input('Hemoglobina glicada HbA1c (%)', placeholder='Ex.: 5,8', key='lab_hba1c')
        f3, f4 = st.columns(2)
        f3.text_input('TTGO 75 g, 1 hora (mg/dL) · opcional', key='lab_ttgo_1h')
        f4.text_input('TTGO 75 g, 2 horas (mg/dL) · opcional', key='lab_ttgo_2h')
        st.text_input('Glicemia plasmática casual (mg/dL) · opcional', key='lab_glicemia_casual')
        with st.expander('Condições de coleta e segurança', expanded=True):
            a,b=st.columns(2)
            adult=a.checkbox('Pessoa adulta (18 anos ou mais)',value=True,key='lab_adult')
            pregnant=b.checkbox('Gestação',value=False,key='lab_pregnant')
            known=a.checkbox('Já possui diagnóstico conhecido de diabetes',value=False,key='lab_known')
            symptoms=b.checkbox('Sintomas típicos (sede intensa, muita urina ou perda de peso)',value=False,key='lab_symptoms')
            fasting=a.checkbox('Jejum de 8 a 12 h confirmado',value=True,key='lab_fasting')
            ogtt=b.checkbox('TTGO realizado com 75 g',value=True,key='lab_ogtt')
            certified=a.checkbox('Método de HbA1c padronizado pelo laboratório',value=True,key='lab_certified')
            interference=b.checkbox('Possível interferência na HbA1c (anemia, transfusão etc.)',value=False,key='lab_interference')
        analyzed=st.form_submit_button('Analisar exames', type='primary', width='stretch')
    if analyzed:
        values={k: st.session_state.get('lab_'+k) for k in
                ['glicemia_jejum','hba1c','ttgo_1h','ttgo_2h','glicemia_casual']}
        try:
            result=evaluate_labs(values,adult=adult,pregnant=pregnant,known_diabetes=known,
                fasting_confirmed=fasting,ogtt_75g_confirmed=ogtt,
                certified_a1c=certified,a1c_interference=interference,classic_symptoms=symptoms)
            st.session_state['lab_result']=result.to_dict()
        except ValueError as e:
            st.session_state.pop('lab_result',None)
            st.error(str(e))
    if st.session_state.get('lab_result'):
        r=st.session_state['lab_result']
        st.markdown('<div class="f-title">02 · Resultado em resumo</div>', unsafe_allow_html=True)
        status_label = {
            'criterios_concordantes': 'Dois critérios laboratoriais concordantes',
            'confirmacao_pendente': 'Confirmação pendente',
            'inconclusivo': 'Resultados discordantes',
            'faixa_intermediaria': 'Faixa intermediária',
            'sem_criterio_nos_dados': 'Sem alteração nos exames avaliados',
            'dados_insuficientes': 'Dados insuficientes',
            'fora_escopo': 'Fora do escopo automático',
            'necessita_avaliacao': 'Avaliação clínica necessária',
        }.get(r['status'], 'Avaliação laboratorial')
        st.markdown(
            '<section class="f-lab-summary">'
            '<div class="f-lab-eyebrow">RESUMO DA ANÁLISE · EXEMPLO EDUCACIONAL</div>'
            f'<div class="f-lab-status">{html.escape(status_label)}</div>'
            f'<h2>{html.escape(r["headline"])}</h2>'
            f'<p>{html.escape(r["explanation"])}</p>'
            '<div class="f-lab-probability"><b>Probabilidade individual de diabetes tipo 2: '
            'Não disponível.</b> Não existe modelo validado no Fundamento para informar esse percentual.</div>'
            '</section>', unsafe_allow_html=True,
        )
        if r['measurements']:
            st.markdown('**Por que o sistema chegou a este resultado?**')
            prominent = [x for x in r['measurements']
                         if 'diabetes' in x['interpretação'] or 'intermediária' in x['interpretação']]
            if not prominent:
                prominent = r['measurements']
            cards=[]
            for item in prominent[:3]:
                value = f"{item['valor']:g}".replace('.', ',')
                cards.append(
                    '<div class="f-lab-factor"><div><strong>' + html.escape(item['exame']) +
                    '</strong><small>' + html.escape(item['interpretação']) +
                    '</small></div><b>' + html.escape(value + ' ' + item['unidade']) + '</b></div>'
                )
            st.markdown('<div class="f-lab-factors">'+''.join(cards)+'</div>',unsafe_allow_html=True)
        st.markdown('**O que ainda falta conferir?**')
        st.caption(r.get('follow_up_message', 'A decisão sobre exames adicionais cabe ao médico.'))
        for suggestion in r.get('suggested_exams', []):
            st.markdown(
                '<div class="f-lab-recommend"><b>' + html.escape(suggestion['exam']) + '</b>'
                '<span>' + html.escape(suggestion['reason']) + '</span></div>',
                unsafe_allow_html=True,
            )
        with st.expander('Ver exames completos e orientações adicionais'):
            if r['measurements']:
                st.dataframe(pd.DataFrame(r['measurements']),hide_index=True,width='stretch')
            for note in r['notes']:
                st.warning(note)
            for step in r['next_steps']:
                st.write('• ' + step)
        st.markdown('<div class="f-title">03 · Fontes e critérios</div>',unsafe_allow_html=True)
        st.caption('Fontes para conferir a regra aplicada, não validação clínica do Fundamento.')
        for sid in r['source_ids']:
            src=SOURCES[sid]
            st.markdown(f'[{src["title"]}]({src["url"]})')
        st.caption('Regras determinísticas e transparentes. Nenhuma síntese clínica desta tela é gerada pelo Ollama.')
        st.download_button('Baixar resultado demonstrativo em JSON',
            json.dumps(r,ensure_ascii=False,indent=2),file_name='Fundamento_exames.json',mime='application/json')
    else:
        st.caption('Ao selecionar “Analisar exames”, o Fundamento informa se os valores atendem a alguma faixa de referência, se exigem confirmação ou se faltam dados.')
    st.divider()
    st.markdown('**Outros exames** podem ser necessários conforme a situação clínica. A seleção depende de profissional habilitado; o aplicativo não prescreve testes.')
    st.caption('A etapa estatística de probabilidade calibrada permanece em desenvolvimento e depende de dados e validação externos. A aba Análise contém um modelo histórico de indicadores de saúde, separado da avaliação laboratorial.')

if navigation == "Análise":
    st.markdown(
        '<section class="f-hero"><h1>Como o modelo interpreta este perfil?</h1>'
        '<p>Escolha um dos três casos fictícios para explorar o resultado e conferir suas fontes.</p></section>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="f-warning"><strong>ⓘ Uso educacional.</strong> '
        'Estes casos ilustram um modelo treinado com dados históricos. O aplicativo não '
        'determina se uma pessoa tem diabetes nem prevê se ela vai desenvolver a doença.</div>',
        unsafe_allow_html=True,
    )
    if "result" not in st.session_state:
        st.markdown(
            """<div class="f-empty"><div class="f-eyebrow" >UMA EXPLICAÇÃO QUE VOCÊ PODE CONFERIR</div>
        <h3>Do resultado à evidência.</h3><p>Escolha um perfil fictício no painel lateral e clique em <strong>Analisar caso</strong> para explorar o resultado.</p>
        <div class="f-steps"><div class="f-step"><b>01 · Entenda</b>Veja quais fatores contribuíram para a saída do modelo.</div><div class="f-step"><b>02 · Confira</b>Consulte os trechos e as fontes de cada fator.</div><div class="f-step"><b>03 · Avalie</b>Identifique os limites e avalie a clareza da explicação.</div></div></div>""",
            unsafe_allow_html=True,
        )
    else:
        r = st.session_state["result"]
        st.markdown(
            f'<div class="f-title">{case.split(" —")[0]} · Leitura do resultado</div>',
            unsafe_allow_html=True,
        )
        threshold = metrics["threshold"]
        positive = r["score"] >= threshold
        label = "Classe 1" if positive else "Classe 0"
        comparison = "atingiu ou superou" if positive else "ficou abaixo de"
        cutoff = f"{threshold:.0%}"
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
        c1.metric("Proporção positiva no grupo histórico", score_label)
        c2.metric("Referência histórica do modelo", base_label)
        st.markdown(
            f'<div class="prediction"><span>Classificação experimental · {label}</span>'
            f'<p>O escore do grupo ({score_label}) {comparison} o limiar técnico de '
            f'<strong>{cutoff}</strong>. Classe 1 significa o rótulo combinado de pré-diabetes ou '
            'diabetes nos registros históricos; classe 0 significa ausência desse rótulo. '
            '<strong>Não é diagnóstico nem previsão de doença futura.</strong></p></div>',
            unsafe_allow_html=True,
        )
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
    st.write("As fontes clínicas abaixo embasam a avaliação laboratorial. A documentação histórica do modelo experimental aparece em seguida.")
    for sid, src in SOURCES.items():
        st.markdown(f'**{sid}** · [{src["title"]}]({src["url"]})')
    st.subheader("Documentos recuperados pelo modelo experimental")
    st.caption("Três trechos de uma página institucional, sem validação do escore clínico; curadoria adicional pendente.")
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
    st.title("Método e limites")
    st.warning("O módulo Exames usa critérios públicos explícitos, não um modelo probabilístico. O modelo abaixo usa dados históricos de autorrelato e não pode fornecer probabilidade diagnóstica baseada em exames.")
    st.write("Esta página resume o desempenho do modelo de demonstração (quatro variáveis não laboratoriais). Para o módulo principal, abra Exames.")
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


if navigation == "Pacientes" and st.session_state["role"] == "Médico demonstrativo":
    render_doctor()

if navigation == "Meu perfil" and st.session_state["role"] == "Paciente demonstrativo":
    render_patient()
