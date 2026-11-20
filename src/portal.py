"""Telas de perfis fictícios; troca de papel NÃO é autenticação.

Não usar com pacientes identificáveis ou como ferramenta clínica de decisão.
"""
import pandas as pd
import streamlit as st
from datetime import date
from src.patients import (
    DEMO_PATIENT_ID, add_exam, add_note, add_patient, get_patient,
    list_exams, list_notes, list_patients,
)
from src.clinical import evaluate_labs, SOURCES
from src.lab_pdf import extract_labs_from_pdf

FIELDS = [
    ('glicemia_jejum', 'Glicemia de jejum (mg/dL)'),
    ('hba1c', 'Hemoglobina glicada — HbA1c (%)'),
    ('ttgo_1h', 'TTGO 1 hora (mg/dL), se disponível'),
    ('ttgo_2h', 'TTGO 2 horas (mg/dL), se disponível'),
    ('glicemia_casual', 'Glicemia casual (mg/dL), se disponível'),
]
STATUS_PATIENT = {
    'criterios_concordantes': ('Atenção: exames na faixa de diabetes', 'Dois resultados apresentam alterações que precisam ser avaliadas pelo médico.'),
    'confirmacao_pendente': ('Um resultado precisa de confirmação', 'Há alteração em um exame. Um profissional poderá orientar a confirmação.'),
    'inconclusivo': ('Resultados diferentes: é preciso investigar', 'Os exames não apontam todos na mesma direção.'),
    'faixa_intermediaria': ('Atenção: resultado em faixa intermediária', 'Há valores que merecem acompanhamento, mas não indicam diabetes confirmado.'),
    'sem_criterio_nos_dados': ('Sem alterações nas faixas analisadas', 'Os exames enviados ficaram abaixo das faixas avaliadas. Isso não exclui doença.'),
    'dados_insuficientes': ('Precisamos de mais informações', 'Os resultados informados ainda não são suficientes para a análise.'),
    'fora_escopo': ('Avaliação médica necessária', 'A situação informada exige avaliação fora das regras automáticas do protótipo.'),
    'necessita_avaliacao': ('Procure avaliação médica', 'Os resultados e sintomas informados precisam de avaliação médica.'),
}


def _result(exam):
    return evaluate_labs(exam['values'], **exam['conditions'])


def _latest(exams):
    return _result(exams[0]) if exams else None


def _summarize_measurements(result):
    for r in result.measurements:
        st.write(f"**{r['exame']}: {str(r['valor']).replace('.', ',')} {r['unidade']}** — {r['interpretação']}")


def _history_graph(exams):
    if len(exams) < 2:
        st.caption('O gráfico de evolução aparece quando houver pelo menos dois exames com data.')
        return
    df = pd.DataFrame([{'Data': ex['examined_on'],
                        'HbA1c (%)': ex['values'].get('hba1c'),
                        'Glicemia (mg/dL)': ex['values'].get('glicemia_jejum')}
                       for ex in reversed(exams)]).set_index('Data')
    col1, col2 = st.columns(2)
    if df['HbA1c (%)'].notna().any():
        col1.caption('Evolução da HbA1c (%)')
        col1.line_chart(df[['HbA1c (%)']])
    if df['Glicemia (mg/dL)'].notna().any():
        col2.caption('Evolução da glicemia de jejum (mg/dL)')
        col2.line_chart(df[['Glicemia (mg/dL)']])
    st.caption('Linhas conectam exames de datas diferentes; não são projeções futuras nem diagnóstico.')


def _exam_form(patient_id, actor):
    prefix = ('med_' if actor == 'Médico demonstrativo' else 'pac_') + patient_id
    with st.expander('Importar resultados de PDF fictício (opcional)'):
        st.caption('Aceita apenas PDF textual fictício ou anonimizado. Confira os valores extraídos antes de salvar.')
        pdf = st.file_uploader('PDF demonstrativo (até 5 MB)', type=['pdf'], key=prefix+'_file')
        if pdf and st.button('Preencher campos a partir do PDF', key=prefix+'_extract'):
            try:
                found, notices = extract_labs_from_pdf(pdf.getvalue())
                for msg in notices:
                    st.info(msg)
                if not found:
                    st.warning('Não foram encontrados valores interpretáveis. Digite os valores manualmente.')
                for key, value in found.items():
                    st.session_state[prefix + '_' + key] = str(value).replace('.', ',')
            except ValueError as e:
                st.error(str(e))
    with st.form(prefix + '_entry', clear_on_submit=False):
        when = st.date_input('Data do exame', value=date.today(), max_value=date.today(), key=prefix+'_when')
        c1, c2 = st.columns(2)
        values = {}
        for i, (name, label) in enumerate(FIELDS):
            target = c1 if i % 2 == 0 else c2
            values[name] = target.text_input(label, key=prefix+'_'+name,
                                             placeholder='Deixe em branco se não houver resultado')
        st.caption('Condições dos exames: assinale somente o que foi conferido no documento.')
        cc1, cc2 = st.columns(2)
        opts = {
            'adult': cc1.checkbox('Pessoa adulta', value=True, key=prefix+'_adult'),
            'pregnant': cc2.checkbox('Gestação', value=False, key=prefix+'_pregnant'),
            'known_diabetes': cc1.checkbox('Diagnóstico prévio relatado', value=False, key=prefix+'_known'),
            'fasting_confirmed': cc2.checkbox('Jejum confirmado', value=True, key=prefix+'_fasting'),
            'certified_a1c': cc1.checkbox('HbA1c com método padronizado', value=True, key=prefix+'_certified'),
            'a1c_interference': cc2.checkbox('Possível interferência na HbA1c', value=False, key=prefix+'_interference'),
            'ogtt_75g_confirmed': cc1.checkbox('TTGO com 75 g', value=True, key=prefix+'_ogtt'),
            'classic_symptoms': cc2.checkbox('Sintomas típicos relatados', value=False, key=prefix+'_symptoms'),
        }
        submitted = st.form_submit_button('Salvar exame neste perfil', type='primary')
    if submitted:
        try:
            add_exam(patient_id, when.isoformat(), values, opts, actor)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success('Exame fictício salvo neste perfil. A análise será atualizada.')
            st.rerun()


def _patient_snapshot(exams):
    if not exams:
        st.info('Nenhum exame cadastrado neste perfil fictício. Envie um exame para iniciar.')
        return
    result = _latest(exams)
    headline, message = STATUS_PATIENT.get(result.status, ('Análise laboratorial', result.explanation))
    st.markdown('#### Resultado do exame mais recente')
    if result.status in ('criterios_concordantes', 'confirmacao_pendente', 'inconclusivo', 'necessita_avaliacao'):
        st.warning('**' + headline + '**  \n' + message)
    else:
        st.info('**' + headline + '**  \n' + message)
    st.caption('Exame em ' + exams[0]['examined_on'] + ' · Resultado educativo, não confirma diabetes tipo 2.')
    st.write('**Por que recebemos esse resultado?**')
    _summarize_measurements(result)
    st.write('**O que fazer agora?**  Procure o médico responsável para revisar os exames e seu histórico.')
    if result.suggested_exams:
        st.caption('Informação adicional a discutir com o médico: ' + result.suggested_exams[0]['exam'])


def render_patient():
    patient = get_patient(DEMO_PATIENT_ID)
    exams = list_exams(DEMO_PATIENT_ID)
    st.markdown('<section class="f-hero"><h1>Meu acompanhamento</h1><p>Veja seus resultados e envie novos exames fictícios para construir um histórico.</p></section>', unsafe_allow_html=True)
    st.warning('**Área demonstrativa.** A seleção de papel não é login seguro. Não envie dados pessoais nem exames reais.')
    st.markdown(f'**{patient["label"]}** · Identificação fictícia: `{patient["id"]}`')
    _patient_snapshot(exams)
    st.divider()
    st.markdown('### Meu histórico')
    if exams:
        _history_graph(exams)
        with st.expander('Ver exames anteriores'):
            for ex in exams:
                with st.container(border=True):
                    st.write('**'+ex['examined_on']+'** · '+ex['recorded_by'])
                    _summarize_measurements(_result(ex))
    st.divider()
    st.markdown('### Enviar novo exame fictício')
    _exam_form(DEMO_PATIENT_ID, 'Paciente demonstrativo')
    st.caption('As observações internas dos profissionais não são exibidas na área do paciente.')


def render_doctor():
    st.markdown('<section class="f-hero"><h1>Pacientes e histórico</h1><p>Consulte análises, evolução dos exames e registros da equipe para cada perfil fictício.</p></section>', unsafe_allow_html=True)
    st.warning('**Módulo de demonstração:** papel de médico simulado, sem autenticação. Não utilizar dados de pacientes reais ou identificáveis.')
    patients = list_patients()
    labels = {p['id']: p['label'] + ' · ' + p['id'] for p in patients}
    pid = st.selectbox('Selecionar perfil fictício', list(labels), format_func=lambda x: labels[x], key='doctor_patient_choice')
    patient = get_patient(pid)
    st.markdown(f'### {patient["label"]}')
    st.caption(f'Identificação fictícia: {pid} · Idade informada: {patient["age"]} anos · Dados de demonstração')
    exams = list_exams(pid)
    if exams:
        result = _latest(exams)
        st.markdown('#### Conclusão resumida')
        st.info('**'+result.headline+'**  \n'+result.explanation)
        st.write('**Critérios e resultados utilizados**')
        _summarize_measurements(result)
        st.caption('Probabilidade individual de diabetes tipo 2: não disponível (modelo não validado).')
        if result.suggested_exams:
            st.write('**Informações complementares a considerar**')
            for suggestion in result.suggested_exams:
                st.write('• '+suggestion['exam']+' — '+suggestion['reason'])
        with st.expander('Critérios, limitações e fontes científicas'):
            for note in result.notes:
                st.warning(note)
            for sid in result.source_ids:
                st.markdown(f'[{SOURCES[sid]["title"]}]({SOURCES[sid]["url"]})')
        st.markdown('#### Evolução dos exames')
        _history_graph(exams)
        with st.expander('Consultar todos os exames registrados'):
            for ex in exams:
                with st.container(border=True):
                    st.write('**'+ex['examined_on']+'** · Inserido por '+ex['recorded_by'])
                    _summarize_measurements(_result(ex))
    else:
        st.info('Perfil sem exames registrados.')
    st.divider()
    st.markdown('### Evolução e observações da equipe médica')
    st.caption('Notas fictícias com autoria e data. Registros anteriores não podem ser apagados ou modificados nesta demonstração.')
    for note in list_notes(pid):
        with st.container(border=True):
            st.write(f'**{note["type"]}** · {note["author"]} · {note["created_at"][:16].replace("T", " ")} UTC')
            st.write(note['body'])
    with st.form('note_'+pid, clear_on_submit=True):
        note_type = st.selectbox('Tipo da observação', ['Observação','Pendência','Plano de acompanhamento'])
        body = st.text_area('Escrever observação fictícia para próximo atendimento', max_chars=1000,
                            placeholder='Ex.: conferir os resultados antes de nova avaliação')
        written = st.form_submit_button('Adicionar observação')
    if written:
        try:
            add_note(pid, 'Médico demonstrativo', note_type, body)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success('Observação fictícia registrada no histórico.')
            st.rerun()
    st.divider()
    with st.expander('Adicionar novo exame para este perfil'):
        _exam_form(pid, 'Médico demonstrativo')
    with st.expander('Cadastrar outro perfil de demonstração'):
        with st.form('new_demo_patient', clear_on_submit=True):
            alias = st.text_input('Identificação fictícia (não informar nome real)', placeholder='Ex.: Paciente fictício 003')
            age = st.number_input('Idade fictícia', min_value=18, max_value=110, value=45)
            add = st.form_submit_button('Criar perfil fictício')
        if add:
            try:
                new_id = add_patient(alias, int(age))
            except ValueError as e:
                st.error(str(e))
            else:
                st.success('Perfil fictício '+new_id+' criado. Selecione-o na lista acima.')
                st.rerun()
