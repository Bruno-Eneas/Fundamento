"""Especificação única do gráfico usada pela interface e pelos testes."""


def contribution_spec(colors):
    return {
        "height": 165,
        "background": colors["surface"],
        "mark": {"type": "bar", "cornerRadiusEnd": 4, "height": 17},
        "encoding": {
            "y": {
                "field": "factor",
                "type": "nominal",
                "sort": {"field": "rank", "op": "min", "order": "ascending"},
                "axis": {"title": None, "labelLimit": 240, "labelFontSize": 12},
            },
            "x": {
                "field": "contribution_pp",
                "type": "quantitative",
                "scale": {"zero": True},
                "axis": {
                    "title": "Contribuição (pontos percentuais)",
                    "tickCount": 5,
                    "format": ".1f",
                },
            },
            "color": {
                "condition": {
                    "test": "datum.contribution_pp >= 0",
                    "value": colors["accent"],
                },
                "value": "#759bc9",
            },
            "tooltip": [
                {"field": "factor", "type": "nominal", "title": "Fator"},
                {
                    "field": "contribution_pp",
                    "type": "quantitative",
                    "format": "+.2f",
                    "title": "Contribuição (p.p.)",
                },
            ],
        },
        "config": {
            "view": {"stroke": None},
            "axis": {
                "domain": False,
                "gridColor": colors["line"],
                "labelColor": colors["muted"],
                "titleColor": colors["muted"],
                "titlePadding": 16,
            },
        },
    }
