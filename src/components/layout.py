from dash import Dash, html
import pandas as pd
from PIL import Image

from . import method_dropdown, purchaser_chart, supplier_chart, date_select, KPIs

#pil_img = Image.open("src/components/Stiesdal logo v1.png")

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
            #html.Img(src=pil_img, 
            #         style={"width": "100px", "display": "inline-block", "float": "right", "margin-top": "20px", "margin-right": "20px"}
            #),
            # horizontal line under the header
            html.Hr(),
            # another Div object inside the existing Div object
            html.Div(
                children=[date_select.render(app, data)],
                style={"margin-left": "10px", "width": "auto", "display": "inline-block"}
            ),
            html.Div(
                children=[KPIs.render(app, data)],
                style={"margin": "10px", "width": "75%", "height": "100px", "display": "inline-block"}
            ),
            html.Div(
                # name of the Div class
                className="dropdown-container",
                # objects of this Div class
                # need to pass the created app to the render function
                children=[method_dropdown.render(app, data)],
                style={'margin': '10px'}
            ),
            html.Div(
                children=[supplier_chart.render(app, data)],
                style={"width": "45%", "display": "inline-block", "margin-left": "10px"}
            ),
            html.Div(
                children=[purchaser_chart.render(app, data)],
                style={"width": "45%", "display": "inline-block", "margin-left": "60px"}
            )
        ]
    )
