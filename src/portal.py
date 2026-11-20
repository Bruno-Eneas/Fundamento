"""Portal acadêmico de acesso separado; somente dados fictícios.

Senhas demonstrativas NÃO significam prontuário seguro para uso real.
"""
import html
import pandas as pd
import streamlit as st
from datetime import date
from src.patients import (
    add_exam, add_note, add_patient, get_patient,
    list_exams, list_notes, list_patients,
)
from src.clinical import evaluate_labs, SOURCES
from src.lab_pdf import extract_labs_from_pdf
from src.auth import create_patient_login, can_view_profile, can_edit_profile
from src.presentation import brief_status

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
    prefix = 'med_' + patient_id
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
            'fasting_confirmed': cc2.checkbox('Jejum confirmado', value=False, key=prefix+'_fasting'),
            'certified_a1c': cc1.checkbox('HbA1c com método padronizado', value=False, key=prefix+'_certified'),
            'a1c_interference': cc2.checkbox('Possível interferência na HbA1c', value=False, key=prefix+'_interference'),
            'ogtt_75g_confirmed': cc1.checkbox('TTGO com 75 g', value=False, key=prefix+'_ogtt'),
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


def _status_card(result, *, patient_view=True):
    info = brief_status(result)
    st.markdown(
        '<div class="f-result-card">'
        '<div class="f-result-level">' + html.escape(info["level"]) + '</div>'
        '<h2>' + html.escape(info["title"]) + '</h2>'
        '<p>' + html.escape(info["reason"]) + '</p>'
        '<div class="f-result-next"><strong>O que fazer:</strong> '
        + html.escape(info["next_step"]) + '</div></div>',
        unsafe_allow_html=True,
    )
    if patient_view:
        st.caption('Este resumo é educativo, não confirma nem exclui diabetes tipo 2.')
    else:
        st.caption('Conclusão laboratorial, não diagnóstico do tipo 2. Probabilidade individual: não disponível (modelo não validado).')


def render_patient(account):
    if account.get('role') != 'patient' or not account.get('patient_id'):
        st.error('Acesso não autorizado.'); st.stop()
    pid = account['patient_id']  # sempre da conta, nunca um seletor livre
    if not can_view_profile(account, pid):
        st.error('Acesso negado.'); st.stop()
    patient = get_patient(pid)
    if not patient:
        st.error('Perfil não encontrado.'); st.stop()
    exams = list_exams(pid)
    st.markdown('<section class="f-hero"><h1>Meu resultado</h1>'
                '<p>Seus exames explicados de forma simples.</p></section>', unsafe_allow_html=True)
    st.write('**' + patient['label'] + '**')
    st.caption('Número do perfil: ' + pid + ' · Demonstração com dados fictícios')
    if exams:
        _status_card(_latest(exams))
        st.markdown(f'**Último exame:** {exams[0]["examined_on"]}')
        st.caption(f'Exames cadastrados: {len(exams)}')
        with st.expander('Datas dos meus exames'):
            for ex in exams:
                status = brief_status(_result(ex))
                st.write(ex['examined_on'] + ' · ' + status['level'])
    else:
        st.info('Você ainda não tem exames cadastrados. Seu médico poderá adicioná-los.')
    st.caption('Somente a equipe médica pode lançar exames ou observações neste protótipo.')
    st.caption('Não use esta demonstração para tomar decisões sobre sua saúde.')


def render_doctor(account, *, readonly=False, walkthrough=False):
    if account.get('role') != 'doctor':
        st.error('Acesso restrito à área médica demonstrativa.'); st.stop()
    st.markdown('<section class="f-hero"><h1>Pacientes</h1>'
                '<p>Pesquise um perfil, confira o resultado e registre a evolução.</p></section>',
                unsafe_allow_html=True)
    st.info('Ambiente acadêmico com pacientes fictícios. Não enviar exames reais nem informações identificáveis.')
    if walkthrough:
        st.success('Demonstração sugerida: 1. Selecione DEMO-001. 2. Veja o resultado e os exames anteriores. 3. Abra o lançamento de exame e as observações.')
    if readonly:
        st.caption('Vitrine pública somente leitura. Não é possível criar pacientes, lançar exames ou registrar notas.')
    if 'new_patient_credentials' in st.session_state:
        new_id, pwd = st.session_state['new_patient_credentials']
        st.success('Novo perfil criado. Guarde estes dados fictícios antes de ocultar:')
        st.code('Número: ' + new_id + '\nSenha: ' + pwd)
        if st.button('Ocultar a senha gerada', key='hide_new_pwd'):
            st.session_state.pop('new_patient_credentials', None)
            st.rerun()
    query = st.text_input('Pesquisar paciente por número ou nome fictício',
                          placeholder='Ex.: DEMO-001', key='doctor_query').strip().casefold()
    patients = [p for p in list_patients()
                if query in p['id'].casefold() or query in p['label'].casefold()]
    if not patients:
        st.warning('Nenhum paciente encontrado. Tente outro número ou nome fictício.')
        if not readonly:
            _new_patient_form()
        return
    labels = {p['id']: p['label'] + ' · ' + p['id'] for p in patients}
    pid = st.selectbox('Selecionar paciente', list(labels),
                       format_func=lambda x: labels[x], key='doctor_patient_choice')
    if not can_edit_profile(account, pid):
        st.error('Acesso negado.'); st.stop()
    patient = get_patient(pid)
    exams = list_exams(pid)
    st.markdown('### ' + patient['label'])
    st.caption('Perfil ' + pid + ' · ' + str(patient['age']) + ' anos · Histórico fictício')
    if exams:
        st.markdown('#### Resultado mais recente')
        result = _latest(exams)
        _status_card(result, patient_view=False)
        c1, c2 = st.columns(2)
        c1.metric('Último exame', exams[0]['examined_on'])
        c2.metric('Exames registrados', str(len(exams)))
        st.write('**Principais resultados:**')
        _summarize_measurements(result)
        with st.expander('Abrir justificativa completa e fontes'):
            st.write(result.explanation)
            if result.suggested_exams:
                st.write('**Informações complementares a considerar:**')
                for suggestion in result.suggested_exams:
                    st.write('• ' + suggestion['exam'] + ': ' + suggestion['reason'])
            for note in result.notes:
                st.warning(note)
            for sid in result.source_ids:
                st.markdown(f'[{SOURCES[sid]["title"]}]({SOURCES[sid]["url"]})')
        with st.expander('Consultar evolução e histórico completo'):
            _history_graph(exams)
            for ex in exams:
                with st.container(border=True):
                    st.write('**' + ex['examined_on'] + '** · ' + ex['recorded_by'])
                    _summarize_measurements(_result(ex))
    else:
        st.info('Perfil ainda sem exames registrados.')
    if not readonly:
        with st.expander('Adicionar exame ao histórico deste paciente'):
            _exam_form(pid, 'Médico demonstrativo · ' + account['login'])
    st.divider()
    st.markdown('### Notas para acompanhamento')
    st.caption('Observações médicas ficam restritas à área do médico e mantêm autoria e data.')
    for note in list_notes(pid):
        with st.container(border=True):
            st.write(f'**{note["type"]}** · {note["author"]} · {note["created_at"][:16].replace("T", " ")} UTC')
            st.write(note['body'])
    if not readonly:
        _doctor_note_form(pid, account)
        _new_patient_form()


def _doctor_note_form(pid, account):
    with st.form('note_' + pid, clear_on_submit=True):
        note_type = st.selectbox('Categoria', ['Observação','Pendência','Plano de acompanhamento'])
        body = st.text_area('Nova observação para próximos atendimentos', max_chars=1000,
                            placeholder='Ex.: conferir exame de controle no próximo retorno')
        written = st.form_submit_button('Salvar observação')
    if written:
        try:
            add_note(pid, 'Médico demonstrativo · ' + account['login'], note_type, body)
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success('Observação registrada no histórico fictício.')
            st.rerun()

def _new_patient_form():
    with st.expander('Cadastrar novo paciente fictício'):
        with st.form('new_demo_patient', clear_on_submit=True):
            alias = st.text_input('Nome ou apelido fictício', placeholder='Ex.: Paciente fictício 003')
            age = st.number_input('Idade fictícia', min_value=18, max_value=110, value=45)
            add = st.form_submit_button('Criar perfil e acesso')
        if add:
            try:
                new_id = add_patient(alias, int(age))
                pwd = create_patient_login(new_id)
            except ValueError as exc:
                st.error(str(exc))
            else:
                # A senha é entregue ao médico uma vez, jamais incluída em logs ou URLs.
                st.session_state['new_patient_credentials'] = (new_id, pwd)
                st.rerun()
