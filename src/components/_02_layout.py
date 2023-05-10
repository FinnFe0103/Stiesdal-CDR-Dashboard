from dash import Dash, html
import pandas as pd

from . import _03_date_select, _03_method_dropdown, _05_purchaser_chart, _05_supplier_chart, _05_KPIs, _06_price_chart

image_path = "../assets/Stiesdal logo v1.png"

def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        # name of the Div class
        className="app-div",
        # objects of this Div class (called children)
        children=[
            # header of the dashboard
            html.H1(app.title,
                    style={"width": "75%", "display": "inline-block", "margin-left": "10px", "margin-top": "20px", "font-size": "1.5em", "color": "black"}
            ),
            html.Img(src=image_path, 
                     style={"width": "100px", "display": "inline-block", "float": "right", "margin-top": "20px", "margin-right": "20px"}
            ),
            # horizontal line under the header
            html.Hr(),
            # another Div object inside the existing Div object
            html.Div(
                children=[_03_date_select.render(app, data)],
                style={"margin-left": "10px", "width": "auto", "display": "inline-block"}
            ),
            html.Div(
                children=[_05_KPIs.render(app, data)],
                style={"margin": "10px", "width": "75%", "height": "100px", "display": "inline-block"}
            ),
            html.Div(
                # name of the Div class
                className="dropdown-container",
                # objects of this Div class
                # need to pass the created app to the render function
                children=[_03_method_dropdown.render(app, data)],
                style={'margin': '10px'}
            ),
            html.Div(
                children=[_05_supplier_chart.render(app, data)],
                style={"width": "45%", "display": "inline-block", "margin-left": "10px"}
            ),
            html.Div(
                children=[_05_purchaser_chart.render(app, data)],
                style={"width": "45%", "display": "inline-block", "margin-left": "60px"}
            ),
            html.Div(
                children=[_06_price_chart.render(app, data)],
                style={"width": "45%", "display": "inline-block", "margin-left": "10px"}
            ),
        ]
    )
