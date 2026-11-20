import unittest
from src.clinical import evaluate_labs, SOURCES

class ClinicalTests(unittest.TestCase):
    def test_zero_data_abstains(self):
        self.assertEqual(evaluate_labs({}).status,'dados_insuficientes')
    def test_one_high_needs_confirm(self):
        r=evaluate_labs({'hba1c':6.8})
        self.assertEqual(r.status,'confirmacao_pendente')
        self.assertIsNone(r.probability)
    def test_two_positive(self):
        self.assertEqual(evaluate_labs({'hba1c':6.8,'glicemia_jejum':132}).status,'criterios_concordantes')
    def test_two_ttgo_times_do_not_confirm_as_independent(self):
        self.assertEqual(evaluate_labs({'ttgo_1h':215,'ttgo_2h':205}).status,'confirmacao_pendente')
    def test_contradiction(self):
        self.assertEqual(evaluate_labs({'hba1c':6.8,'glicemia_jejum':92}).status,'inconclusivo')
    def test_intermediate_borders(self):
        self.assertEqual(evaluate_labs({'glicemia_jejum':100}).status,'faixa_intermediaria')
        self.assertEqual(evaluate_labs({'hba1c':5.7}).status,'faixa_intermediaria')
        self.assertEqual(evaluate_labs({'ttgo_1h':155}).status,'faixa_intermediaria')
    def test_normal_does_not_exclude(self):
        r=evaluate_labs({'glicemia_jejum':92,'hba1c':5.4})
        self.assertEqual(r.status,'sem_criterio_nos_dados')
        self.assertIn('não exclui',r.explanation)
    def test_symptoms_and_random_200(self):
        self.assertEqual(evaluate_labs({'glicemia_casual':201},classic_symptoms=True).status,'necessita_avaliacao')
        self.assertEqual(evaluate_labs({'glicemia_casual':201},classic_symptoms=False).status,'dados_insuficientes')
    def test_pregnancy_and_child_abstain(self):
        self.assertEqual(evaluate_labs({'hba1c':9},pregnant=True).status,'fora_escopo')
        self.assertEqual(evaluate_labs({'hba1c':9},adult=False).status,'fora_escopo')
    def test_hba1c_interference(self):
        self.assertEqual(evaluate_labs({'hba1c':7.2},a1c_interference=True).status,'dados_insuficientes')
    def test_ogtt_nonstandard(self):
        self.assertEqual(evaluate_labs({'ttgo_2h':211},ogtt_75g_confirmed=False).status,'dados_insuficientes')
    def test_missing_fasting(self):
        self.assertEqual(evaluate_labs({'glicemia_jejum':140},fasting_confirmed=False).status,'dados_insuficientes')
    def test_invalid_numbers(self):
        for val in [float('nan'),float('inf'),-3,'xx']:
            with self.assertRaises(ValueError): evaluate_labs({'hba1c':val})
    def test_sources_and_json(self):
        r=evaluate_labs({'hba1c':'6,8'})
        self.assertEqual(len(SOURCES),3)
        self.assertIn('source_ids',r.to_dict())

if __name__=='__main__': unittest.main()

class SuggestionsTests(unittest.TestCase):
    def test_missing_labs_suggests_entry(self):
        r = evaluate_labs({})
        self.assertEqual(r.status, "dados_insuficientes")
        self.assertTrue(any("HbA1c" in s["exam"] for s in r.suggested_exams))

    def test_fasting_high_suggests_confirmation(self):
        r = evaluate_labs({"glicemia_jejum": 132})
        self.assertEqual(r.status, "confirmacao_pendente")
        self.assertIn("HbA1c", r.suggested_exams[0]["exam"])

    def test_hba1c_high_suggests_confirmation(self):
        r = evaluate_labs({"hba1c": 6.8})
        self.assertIn("Glicemia", r.suggested_exams[0]["exam"])

    def test_compatible_valid_labs_do_not_demand_extra_exam(self):
        r = evaluate_labs({"hba1c": 6.8, "glicemia_jejum": 132})
        self.assertEqual(r.suggested_exams, [])
        self.assertIn("tipo", r.follow_up_message)

    def test_conflicting_labs_suggest_repeating_positive(self):
        r = evaluate_labs({"hba1c": 5.5, "glicemia_jejum": 132})
        self.assertEqual(r.status, "inconclusivo")
        self.assertIn("jejum", r.suggested_exams[0]["exam"])

    def test_no_automatic_test_when_below_intermediate(self):
        r = evaluate_labs({"hba1c": 5.3, "glicemia_jejum": 92})
        self.assertEqual(r.suggested_exams, [])

    def test_out_of_scope_does_not_suggest_a_test(self):
        r = evaluate_labs({"hba1c": 9.2}, pregnant=True)
        self.assertEqual(r.suggested_exams, [])

    def test_suggestions_export_in_json(self):
        r = evaluate_labs({"glicemia_jejum": 132})
        self.assertIn("suggested_exams", r.to_dict())
        self.assertIsNone(r.probability)
