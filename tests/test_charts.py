import unittest
import pandas as pd
import altair as alt
from src.charts import contribution_spec

class ChartTests(unittest.TestCase):
    def test_schema_uses_literal_fields_and_signed_domain(self):
        colors={'surface':'#10373c','text':'#eff9f7','muted':'#b4cfce','line':'#356064','accent':'#7ee5bd'}
        spec=contribution_spec(colors)
        spec['data']={'values':[{'factor':'a','contribution_pp':-2.0},{'factor':'b','contribution_pp':0.0},{'factor':'c','contribution_pp':3.0}]}
        alt.Chart.from_dict(spec, validate=True)
        self.assertEqual(spec['encoding']['x']['field'],'contribution_pp')
        self.assertTrue(spec['encoding']['x']['scale']['zero'])
        self.assertNotIn('domain', spec['encoding']['x']['scale'])
