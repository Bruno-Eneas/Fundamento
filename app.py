import json,os
from pathlib import Path
import pandas as pd
import streamlit as st
from src.core import CASES,AGES,explain,retrieve,evidence,rules
from src.storage import save_feedback
from src.generation import generate
ROOT=Path(__file__).parent
st.set_page_config(page_title='Fundamento | Demonstração',page_icon='🔎',layout='wide')
# Segredos só são lidos no servidor, nunca colocados na interface.
for name in ['DATABASE_URL','OLLAMA_URL','OLLAMA_MODEL']:
    try:
        if name in st.secrets: os.environ[name]=str(st.secrets[name])
    except FileNotFoundError: pass
def choose_appearance(value):
    st.session_state['appearance'] = value

def choose_page(value):
    st.session_state['navigation'] = value

st.session_state.setdefault('appearance', 'Claro')
st.session_state.setdefault('navigation', 'Análise')
appearance = st.session_state['appearance']
dark = appearance == 'Escuro'
colors = ({'bg':'#09272b','surface':'#10373c','raised':'#16454a','text':'#eff9f7','muted':'#b4cfce','line':'#356064','accent':'#7ee5bd','button':'#008655','onbutton':'#ffffff','warning':'#463615','warntext':'#ffe8ad','info':'#163e43','infotext':'#d2ece8','side':'#062125'} if dark else
          {'bg':'#f6f8f7','surface':'#ffffff','raised':'#eef5f1','text':'#123a2c','muted':'#4f6a60','line':'#d6e3dd','accent':'#00794d','button':'#00794d','onbutton':'#ffffff','warning':'#fff0cf','warntext':'#654207','info':'#eaf4ef','infotext':'#244d3a','side':'#005238'})
with st.container(key='topbar'):
    heading, theme_control = st.columns([3, 2])
    with heading:
        st.markdown('<span class="f-badge">PROTÓTIPO ACADÊMICO</span>',unsafe_allow_html=True)
    with theme_control:
        with st.container(key='theme_buttons'):
            light_button, dark_button = st.columns(2, gap='small')
            light_button.button('Claro', key='theme_light', type='primary' if not dark else 'secondary', on_click=choose_appearance,args=('Claro',),width='stretch')
            dark_button.button('Escuro', key='theme_dark', type='primary' if dark else 'secondary', on_click=choose_appearance,args=('Escuro',),width='stretch')
# Ilustração vetorial incorporada: não depende de downloads nem de arquivos extras.
import base64
if dark:
    forest = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 190"><g fill="none" stroke="#208d78" stroke-width="1.4"><path d="M0 182Q140 177 215 138T400 161M32 186Q186 153 292 174T400 164M288 18L257 65H272L235 110H254L212 158H364L322 110H341L304 65H319Z"/><path d="M288 18L257 65 319 65 235 110 341 110 212 158 364 158 288 18M257 65L341 110M319 65L212 158M235 110L364 158" opacity=".65"/></g><g fill="#8be7c3">'+''.join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x,y in [(288,18),(257,65),(319,65),(235,110),(341,110),(212,158),(364,158)])+'</g></svg>'
else:
    forest = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 190"><path fill="#e4f3eb" d="M30 190L245 30 400 190Z"/><path fill="#cae9d9" d="M180 190L335 65 400 125V190Z"/>'
    for x,y,scale in [(230,105,.65),(320,50,1.1),(377,116,.55)]:
        forest += f'<g transform="translate({x} {y}) scale({scale})"><path fill="#72bd99" d="M0 0L-22 35H-12L-34 65H-18L-45 100H45L18 65H34L12 35H22Z"/></g>'
    forest += '</svg>'
forest_uri='data:image/svg+xml;base64,'+base64.b64encode(forest.encode()).decode()
css = '\n:root {__VARS__}\n.stApp {background:var(--bg)!important;color:var(--text)!important;color-scheme:__SCHEME__;}\n[data-testid="stHeader"] {background:var(--bg)!important;}\n.block-container {max-width:1390px;padding:3.7rem 2.4rem 2.5rem;}\nh1,h2,h3,h4,p,label,input,textarea,[data-testid="stMarkdownContainer"],[data-testid="stWidgetLabel"] {font-family:\'Segoe UI\',Arial,sans-serif!important;}\n[data-testid="stMarkdownContainer"],[data-testid="stWidgetLabel"],h1,h2,h3 {color:var(--text)!important;}\nh2 {font-size:1.42rem!important;letter-spacing:-.03em;padding-top:1rem!important;}\n[data-testid="stCaptionContainer"] p {color:var(--muted)!important;font-size:12px!important;line-height:1.65;}\na {color:var(--accent)!important;text-underline-offset:4px;}\nhr {border-color:var(--line)!important;margin:18px 0!important;}\n[data-testid="stSidebar"] {background:var(--side)!important;border-right:1px solid #ffffff19;--text:#f0faf5;--muted:#bfd8ce;--surface:#ffffff08;--raised:#ffffff10;--line:#ffffff35;--accent:#b9efd7;--button:#008655;--onbutton:#ffffff;}\n[data-testid="stSidebarContent"] {padding-top:0!important;}\n.f-brand {display:flex;align-items:center;gap:11px;margin:0 0 26px;font-size:24px;font-weight:750;letter-spacing:-.8px;color:#f0faf5;}\n.f-symbol {flex-shrink:0;background:url(\'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA3MiI+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjcyIiByeD0iMTQiIGZpbGw9IiMyOTljNjkiLz48cGF0aCBmaWxsPSIjZjVmYWY2IiBkPSJNMjggOFEzMiAzIDM2IDhMNDkgMjVRNTIgMjkgNDcgMjlIMzlMNTMgNDZRNTYgNTAgNTEgNTBINDJMNTcgNjhIN0wyMiA1MEgxM1E4IDUwIDExIDQ2TDI1IDI5SDE3UTEyIDI5IDE1IDI1WiIvPjwvc3ZnPg==\') center / contain no-repeat;width:37px;height:43px;}\n.f-badge {display:inline-block;border:1px solid var(--line);background:var(--raised);padding:6px 11px;border-radius:9px;color:var(--text);font-size:10px;font-weight:650;letter-spacing:.4px;}\n.st-key-theme_buttons {max-width:210px;margin-left:auto;}\n.st-key-theme_buttons [data-testid="stHorizontalBlock"] {gap:5px!important;flex-wrap:nowrap!important;}\n.st-key-theme_buttons [data-testid="stColumn"] {min-width:0!important;flex:1!important;}\n.st-key-theme_buttons button {min-height:32px!important;height:32px!important;border-radius:18px!important;padding:3px 12px!important;}\n.st-key-theme_buttons button p {font-size:12px!important;}\n.st-key-side_navigation {margin-bottom:18px;}\n.st-key-side_navigation button {justify-content:flex-start!important;min-height:45px!important;padding:8px 14px!important;border-radius:10px!important;}\n.st-key-side_navigation button p {font-size:15px!important;font-weight:650!important;}\n.f-hero {position:relative;overflow:hidden;min-height:165px;padding:24px 0 25px;margin:0;}\n.f-hero:after {content:\'\';position:absolute;right:0;bottom:0;width:43%;height:100%;background:url(\'__FOREST__\') right bottom / contain no-repeat;pointer-events:none;}\n.f-hero h1,.f-hero p {position:relative;z-index:1;max-width:80%;margin:0;padding:0;color:var(--text);font-size:clamp(27px,2.8vw,40px)!important;font-weight:700;letter-spacing:-1.3px;line-height:1.2;}\n.f-hero p {margin-top:3px;}\n.f-warning {border:1px solid #b9904255;background:var(--warning);color:var(--warntext);border-radius:12px;padding:12px 16px;font-size:12px;line-height:1.65;margin-bottom:16px;}\n.f-warning strong {font-size:14px;}\n.f-profile {background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:3px 13px;margin:8px 0 2px;}\n.f-row {display:flex;justify-content:space-between;gap:12px;font-size:12px;padding:12px 0;border-bottom:1px solid var(--line);}\n.f-row:last-child {border:0;}.f-row span {color:var(--muted);}.f-row strong {color:var(--text);text-align:right;}\n.f-status {padding:10px 12px;background:var(--surface);border:1px solid var(--line);border-radius:11px;color:var(--muted);font-size:11px;line-height:1.7;}\n[data-testid="stMetric"] {border:1px solid var(--line);background:var(--surface)!important;border-radius:14px;padding:18px 16px;box-shadow:0 5px 18px #00000005;}\n[data-testid="stMetricLabel"] {height:auto;min-height:30px;}\n[data-testid="stMetricLabel"] p {color:var(--muted)!important;font-size:12px!important;white-space:normal!important;}\n[data-testid="stMetricValue"] {color:var(--text)!important;font-weight:750;letter-spacing:-1px;font-size:34px!important;}\n[data-testid="stExpander"],[data-testid="stForm"] {border:1px solid var(--line)!important;background:var(--surface)!important;border-radius:13px!important;overflow:hidden;}\n[data-testid="stExpander"] summary {background:var(--raised)!important;color:var(--text)!important;min-height:48px;}\n[data-testid="stExpander"] summary p {font-size:13px!important;}\n.stButton button,.stDownloadButton button,.stLinkButton a,[data-testid="stFormSubmitButton"] button {color:var(--accent)!important;background:var(--surface)!important;border:1px solid var(--line)!important;border-radius:10px;min-height:42px;transition:filter .15s;}\n.stButton button p,.stDownloadButton button p,[data-testid="stFormSubmitButton"] button p {color:inherit!important;}\nbutton[kind="primary"] {background:var(--button)!important;color:var(--onbutton)!important;border:1px solid var(--button)!important;}\nbutton[kind="primary"] p {color:var(--onbutton)!important;font-weight:650;}\n.stButton button:hover {filter:brightness(1.12);}\nbutton:focus-visible,a:focus-visible {outline:3px solid var(--accent)!important;outline-offset:3px;}\n[data-baseweb="select"] > div {background:var(--surface)!important;color:var(--text)!important;border-color:var(--line)!important;border-radius:10px;}\n[data-baseweb="select"] > div > div {background:transparent!important;color:var(--text)!important;}\n[data-baseweb="select"] svg {fill:var(--text)!important;}\n[data-baseweb="input"],[data-baseweb="textarea"] {background:var(--surface)!important;border-color:var(--line)!important;}\ntextarea,input {background:var(--surface)!important;color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;}\n[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"],[role="option"] {background:var(--bg)!important;color:var(--text)!important;}\n[data-baseweb="radio"] p {color:var(--text)!important;}\n[data-testid="stAlert"] {border-radius:12px!important;overflow:hidden;}\n[data-testid="stAlert"] > div {background:var(--info)!important;color:var(--infotext)!important;border:1px solid var(--line)!important;}\n[data-testid="stAlert"] [data-testid="stMarkdownContainer"],[data-testid="stAlert"] p {color:inherit!important;}\n[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) > div {background:var(--warning)!important;color:var(--warntext)!important;}\n[data-testid="stAlert"]:has([data-testid="stAlertContentError"]) > div {background:#fbe4df!important;color:#7d2015!important;}\n[data-testid="stVegaLiteChart"] {border:1px solid var(--line);border-radius:14px;background:var(--surface);padding:12px;}\n.f-empty {padding:25px;border:1px solid var(--line);background:var(--surface);border-radius:15px;}\n.f-empty h3 {margin:0 0 12px;padding:0;font-size:25px;}.f-empty p {color:var(--muted);}\n.f-eyebrow {color:var(--accent);letter-spacing:1px;font-size:10px;font-weight:700;margin-bottom:15px;}\n.f-steps {display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px;}.f-step {border-top:2px solid var(--line);padding-top:13px;font-size:13px;color:var(--muted);}.f-step b {display:block;color:var(--accent);margin-bottom:7px;}\n@media(max-width:800px) {.block-container {padding:3.7rem 1rem 2rem;}.f-hero {min-height:145px;padding-top:18px;}.f-hero:after {opacity:.28;width:48%;}.f-hero h1,.f-hero p {max-width:100%;font-size:28px!important;}.f-steps {grid-template-columns:1fr;}}\n'
css += '\n.block-container {padding-top:3.1rem;max-width:1250px;padding-left:2rem;padding-right:2rem;}\n[data-testid="stSidebar"] {width:260px!important;min-width:260px!important;}\n[data-testid="stSidebarUserContent"] {padding:1.7rem 1.1rem!important;}\n.st-key-side_navigation [data-testid="stVerticalBlock"] {gap:8px;}\n.f-brand {margin-bottom:18px;font-size:23px;}\n.f-hero {min-height:133px;padding-top:18px;padding-bottom:21px;}\n.f-hero h1,.f-hero p {font-size:clamp(25px,2.6vw,35px)!important;line-height:1.15;letter-spacing:-.9px;}\n.f-hero:after {width:35%;opacity:.9;}\n.f-warning {padding:10px 14px;margin-bottom:9px;}\n[data-testid="stMetric"] {padding:14px;border-radius:12px;}\n[data-testid="stMetricValue"] {font-size:30px!important;}\n[data-testid="stMetricLabel"] {min-height:24px;}\n.f-row {padding:10px 0;}\n[data-testid="stExpander"] summary {min-height:42px;}\n[data-testid="stSelectbox"] [data-baseweb="select"] > div {background:var(--raised)!important;color:var(--text)!important;}\n[data-testid="stSelectbox"] [data-baseweb="select"] > div > div {background:transparent!important;}\n[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {background:#ffffff0d!important;color:#f0faf5!important;}\n@media(max-width:700px) {.block-container {padding-left:1rem;padding-right:1rem;}.f-hero:after {opacity:.2;}.f-hero {min-height:125px;}}\n'
css=css.replace('__VARS__',';'.join('--'+k+':'+v for k,v in colors.items())+';').replace('__FOREST__',forest_uri).replace('__SCHEME__','dark' if dark else 'light')
st.markdown('<style>'+css+'</style>',unsafe_allow_html=True)
st.markdown('<section class="f-hero"><h1>Entenda os fatores.</h1><p>Confira as evidências.</p></section>',unsafe_allow_html=True)
st.markdown('<div class="f-warning"><strong>Não confirma nem descarta diabetes.</strong><br>O escore representa a classe 1 da base histórica; não é risco clínico validado nem previsão futura.</div>',unsafe_allow_html=True)
with st.sidebar:
    st.markdown('<div class="f-brand"><span class="f-symbol" aria-hidden="true"></span> Fundamento</div>',unsafe_allow_html=True)
    with st.container(key='side_navigation'):
        for page, icon in [('Análise', ':material/bar_chart:'), ('Evidências', ':material/menu_book:'), ('Método', ':material/science:')]:
            st.button(page, key='nav_'+page, icon=icon, width='stretch', type='primary' if st.session_state['navigation']==page else 'secondary', on_click=choose_page, args=(page,))
    navigation = st.session_state['navigation']
    st.divider()
    case=st.selectbox('Perfil demonstrativo',list(CASES),index=1 if len(CASES)>1 else 0)
    v=CASES[case]
    st.markdown(f"""<div class="f-profile">
    <div class="f-row"><span>Faixa etária</span><strong>{AGES[v['Age']-1]} anos</strong></div>
    <div class="f-row"><span>IMC</span><strong>{v['BMI']} kg/m²</strong></div>
    <div class="f-row"><span>Atividade física¹</span><strong>{'Sim' if v['PhysActivity'] else 'Não'}</strong></div>
    <div class="f-row"><span>Hipertensão relatada</span><strong>{'Sim' if v['HighBP'] else 'Não'}</strong></div>
    </div>""",unsafe_allow_html=True)
    st.caption('¹ Nos últimos 30 dias.')
    st.caption('Perfis fictícios. Não representam pacientes da Unimed.')
    analyze=st.button('Analisar caso',type='primary',width='stretch',on_click=choose_page,args=('Análise',))
    st.divider()
    st.caption('Geração: '+('conector configurado' if os.environ.get('OLLAMA_MODEL') else 'modelo não configurado'))
    st.caption('Expertise clínica: revisão especializada pendente.')
if st.session_state.get('case') != case:
    for k in ['result','feedback_id','generated','generation_error']:
        st.session_state.pop(k,None)
    st.session_state['case']=case
if analyze or 'result' not in st.session_state:
    for stale in ['generated','generation_error','feedback_id']:
        st.session_state.pop(stale,None)
    with st.spinner('Calculando as contribuições e buscando evidências…'):
        result=explain(v)
        result['case']=case
        result['inputs']=v
        result['retrieved']={f['feature']:retrieve(f['feature']) for f in result['factors']}
        result['rules_version']='0.1'
        st.session_state['result']=result
if navigation == 'Análise':
    if 'result' not in st.session_state:
        st.markdown("""<div class="f-empty"><div class="f-eyebrow" >UMA EXPLICAÇÃO QUE VOCÊ PODE CONFERIR</div>
        <h3>Do resultado à evidência.</h3><p>Escolha um perfil fictício no painel lateral e clique em <strong>Analisar caso</strong> para explorar o resultado.</p>
        <div class="f-steps"><div class="f-step"><b>01 · Entenda</b>Veja quais fatores contribuíram para a saída do modelo.</div><div class="f-step"><b>02 · Confira</b>Consulte os trechos e as fontes de cada fator.</div><div class="f-step"><b>03 · Avalie</b>Identifique os limites e avalie a clareza da explicação.</div></div></div>""",unsafe_allow_html=True)
    else:
        r=st.session_state['result']; c1,c2,c3=st.columns(3)
        c1.metric('Saída do modelo · classe 1',f"{r['score']*100:.1f}%")
        c2.metric('Referência SHAP',f"{r['base']*100:.1f}%")
        supported=sum(bool(d) for d in r['retrieved'].values())
        c3.metric('Fatores com fontes',f"{supported} / {len(r['factors'])}")
        st.caption('Referência + contribuições SHAP = saída do modelo. Contribuição estatística não é causa clínica.')
        st.subheader('Evidências por fator')
        for f in r['factors']:
            docs=r['retrieved'][f['feature']]
            with st.expander(f"{f['label']} · {f['contribution']*100:+.2f} p.p. · "+('contexto encontrado' if docs else 'sem evidência na base'),expanded=False):
                if not docs:
                    st.warning('Não foi encontrada evidência elegível nesta base para fundamentar este fator. Isso não significa que a associação não exista, nem que o paciente não tenha doença.')
                for d in docs:
                    st.write(d['summary'])
                    st.caption('Síntese documental cadastrada; não é texto gerado ao vivo.')
                    st.markdown(f"**Trecho original:** “{d['excerpt']}”")
                    st.markdown(f"[{d['id']} · {d['organization']} — abrir fonte]({d['url']})")
                    st.caption(f"Seção: {d['section']} | revisão da página: {d['reviewed']} | consulta: {d['accessed']}")
        st.caption('Fontes sobre diabetes tipo 2; a base do modelo não distingue tipos. Contexto documental geral, sem validação clínica. Revisão especializada pendente.')
        with st.expander('Ver gráfico de contribuições SHAP',expanded=False):
            chart=pd.DataFrame({'factor':[f['label'] for f in r['factors']],'contribution_pp':[float(f['contribution'])*100 for f in r['factors']]})
            st.vega_lite_chart(chart, {
                'height':240, 'background':colors['surface'],
                'mark':{'type':'bar','cornerRadiusEnd':4,'height':24},
                'encoding':{
                    'y':{'field':'factor','type':'nominal','sort':None,'axis':{'title':None,'labelLimit':240,'labelFontSize':12}},
                    'x':{'field':'contribution_pp','type':'quantitative','scale':{'zero':True},'axis':{'title':'Contribuição (pontos percentuais)','tickCount':5,'format':'.1f'}},
                    'color':{'condition':{'test':'datum.contribution_pp >= 0','value':colors['accent']},'value':'#759bc9'},
                    'tooltip':[{'field':'factor','type':'nominal','title':'Fator'},{'field':'contribution_pp','type':'quantitative','format':'+.2f','title':'Contribuição (p.p.)'}]},
                'config':{'view':{'stroke':None},'axis':{'domain':False,'gridColor':colors['line'],'labelColor':colors['muted'],'titleColor':colors['muted'],'titlePadding':16}}
            },width='stretch',theme=None)
            with st.expander('Conferir valores das contribuições'):
                st.dataframe(chart.rename(columns={'factor':'Fator','contribution_pp':'Contribuição (p.p.)'}),hide_index=True,width='stretch')
            st.caption('Valores positivos aumentam a saída do modelo em relação à referência; negativos diminuem. A implementação verifica numericamente essa soma.')
        st.subheader('Explicação com fontes')
        if not os.environ.get('OLLAMA_MODEL'):
            st.write('Ainda não há um modelo de linguagem conectado. A versão atual apresenta busca e sínteses documentais; não simula RAG completo.')
        elif st.button('Gerar rascunho com fontes',type='primary',icon=':material/auto_awesome:'):
            drafts={}
            try:
                with st.spinner('Gerando rascunhos para revisão…'):
                    for f in r['factors']:
                        docs=r['retrieved'][f['feature']]
                        if docs: drafts[f['feature']]=generate(f,docs)
                st.session_state['generated']=drafts
                st.session_state.pop('generation_error',None)
            except Exception:
                st.session_state.pop('generated',None)
                st.session_state['generation_error']='Geração indisponível ou resposta inválida. Nenhum texto gerado foi liberado; a consulta documental continua disponível.'
        if st.session_state.get('generation_error'):st.error(st.session_state['generation_error'])
        if st.session_state.get('generated'):
            st.warning('Rascunho experimental: IDs de fontes foram conferidos; o suporte semântico e a correção clínica exigem revisão humana.')
            for f,claims in st.session_state['generated'].items():
                for claim in claims: st.write(claim['text']+' ['+', '.join(claim['source_ids'])+']')
            r['generated_draft']=st.session_state['generated']
        st.subheader('Avalie a explicação')
        st.caption('Avaliação acadêmica de clareza e rastreabilidade; não equivale a validação médica. Não informe dados pessoais.')
        with st.form('feedback'):
            rating=st.radio('A apresentação permite conferir a explicação?',['Concordo','Discordo','Não consigo avaliar'],horizontal=True)
            comment=st.text_area('Comentário opcional',max_chars=500)
            submitted=st.form_submit_button('Salvar avaliação')
        if submitted:
            try:
                st.session_state['feedback_id']=save_feedback(r,rating,comment)
                st.success('Avaliação registrada.')
            except Exception: st.error('Não foi possível salvar. Nenhum sucesso de gravação foi confirmado.')
        if not os.environ.get('DATABASE_URL'):
            st.caption('Nesta instalação, avaliações são salvas em SQLite local. Para persistência em hospedagem, configure PostgreSQL; arquivos locais podem ser descartados pela plataforma.')
        st.download_button('Baixar registro deste caso',json.dumps(r,ensure_ascii=False,indent=2),'Fundamento_caso.json','application/json')
if navigation == 'Evidências':
    st.subheader('Base pequena, identificável e auditável')
    st.write('Três trechos curtos de uma fonte institucional. A ampliação da base e a revisão clínica estão pendentes.')
    for d in evidence():
        st.markdown(f"**{d['id']} — {d['title']}**")
        st.write(d['summary']);st.link_button('Consultar documento',d['url']);st.caption(d['status'])
    st.subheader('Camada de critérios — preparação para expertise')
    st.write('As regras abaixo são de engenharia e rastreabilidade. Não representam conhecimento capturado e validado com médicos; não declaramos uma implementação clínica completa de XAG.')
    st.dataframe(pd.DataFrame(rules()),hide_index=True,width='stretch')
if navigation == 'Método':
    m=json.loads((ROOT/'assets/metrics.json').read_text(encoding='utf-8'))
    st.subheader('Treinamento e avaliação interna')
    st.write('Árvore de decisão com profundidade máxima 4, quatro entradas e mínimo de 500 registros por folha. Divisão por grupos mantém perfis idênticos em apenas um lado do treino/teste.')
    a,b,c=st.columns(3);a.metric('Registros',f"{m['rows']:,}");b.metric('ROC AUC',f"{m['roc_auc']:.3f}");c.metric('Precisão média (AP)',f"{m['average_precision']:.3f}")
    st.caption('ROC AUC mede ordenação; AP resume precisão e sensibilidade ao variar o limiar. Nenhuma dessas métricas prova calibração ou aptidão clínica.')
    st.write('**Rótulo:** '+m['target'])
    st.write(f"**Matriz de confusão, limiar {m['threshold']:.2f}:** linhas = rótulo observado; colunas = classe prevista.")
    st.caption(m['threshold_method'])
    st.dataframe(pd.DataFrame(m['confusion_matrix'],index=['Observado 0','Observado 1'],columns=['Previsto 0','Previsto 1']))
    for limit in m['limitations']:st.write('• '+limit)
    st.link_button('Metadados da base UCI','https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators')
    st.download_button('Baixar métricas e proveniência',json.dumps(m,ensure_ascii=False,indent=2),'Fundamento_metricas.json','application/json')
    st.markdown('**Ainda pendente:** conferir codificação original e licença, expandir fontes, revisar expertise, ampliar os testes de geração, conectar banco remoto, publicar e validar externamente.')

st.divider()
st.caption('Fundamento · Projeto acadêmico independente · Sem validação clínica ou vínculo institucional oficial declarado.')
