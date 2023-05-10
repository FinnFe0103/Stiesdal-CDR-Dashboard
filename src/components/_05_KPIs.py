import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

from . import _00_own_ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:

    @app.callback(
        Output(_00_own_ids.KPIS, "children"),
        [Input(_00_own_ids.METHOD_DROPDOWN, "value"), 
         Input(_00_own_ids.DATE_RANGE, "start_date"),
         Input(_00_own_ids.DATE_RANGE, "end_date")]
    )
    def update_KPIs(methods, start_date, end_date):
        filtered_data = data[(data["Announcement Date"] > start_date) & (data["Announcement Date"] < end_date)]
        if methods in list(data["CDR Method"].dropna().unique()):
            filtered_data = filtered_data[filtered_data["CDR Method"] == methods]

        fs = 40
        ts = 20
        hx = "#00497a"
        hx_t = "#212529"
        fig = go.Figure()
        fig.add_trace(
            go.Indicator(
                title = {"text": "Total Purchased (k)", "font":{"size":ts, "color":hx_t}},
                mode = "number",
                value = round(sum(filtered_data["Tons Purchased/Sold"])/1000, 2),
                number = {'valueformat':'.2f', "suffix": "t", "font":{"size":fs, "color":hx}},
                domain = {"row": 0, "column": 0}
            ),
        )
        fig.add_trace(
            go.Indicator(
                title = {"text": "Total Delivered (k)", "font":{"size":ts, "color":hx_t}},
                mode = "number",
                value = round(sum(filtered_data["Tons Delivered"])/1000, 2),
                number = {'valueformat':'.2f', "suffix": "t", "font":{"size":fs, "color":hx}},
                domain = {"row": 0, "column": 1}
            ),
        )
        fig.add_trace(
            go.Indicator(
                title = {"text": "Purchases Delivered", "font":{"size":ts, "color":hx_t}},
                mode = "number",
                value = sum(filtered_data["Tons Delivered"]) / sum(filtered_data["Tons Purchased/Sold"]) *100 if sum(filtered_data["Tons Purchased/Sold"]) != 0 else 0,
                number = {'valueformat':'.2f', "suffix": "%", "font":{"size":fs, "color":hx}},
                domain = {"row": 0, "column": 2}
            ),
        )
        fig.add_trace(
            go.Indicator(
                title = {"text": "# of Suppliers", "font":{"size":ts, "color":hx_t}},
                mode = "number",
                value = filtered_data["Supplier"].nunique(),
                number = {"font":{"size":fs, "color":hx}},
                domain = {"row": 0, "column": 3}
            ),
        )
        fig.add_trace(
            go.Indicator(
                title = {"text": "# of Purchasers", "font":{"size":ts, "color":hx_t}},
                mode = "number",
                value = filtered_data["Purchaser"].nunique(),
                number = {"font":{"size":fs, "color":hx}},
                domain = {"row": 0, "column": 4}
            ),
        )
        fig.add_trace(
            go.Indicator(
                title = {"text": "Average Price per Ton", "font":{"size":ts, "color":hx_t}},
                mode = "number",
                value = filtered_data["Price per Ton"].mean(),
                number = {'valueformat':'.2f', "prefix": "$","font":{"size":fs, "color":hx}},
                domain = {"row": 0, "column": 5}
            ),
        )
        fig.update_layout(
            grid = {'rows': 1, 'columns': 6, 'pattern': "coupled", "xgap": 0.1}, 
            height=150,
            width=1450,
            #paper_bgcolor="LightSteelBlue",
            margin_t=100,
            margin_b=20,
            margin_l=20,
            margin_r=20
            )

        return html.Div(dcc.Graph(figure=fig), id=_00_own_ids.KPIS)
    
    return html.Div(id=_00_own_ids.KPIS)
    