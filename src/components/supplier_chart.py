import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import bar_plot, own_ids

# render function again receives a dash app and returns a Div object
def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # Output: chaning bar-chart, updating the children of that Div
    # Input: dropdown, get value
    @app.callback(
        Output(own_ids.S_CHART, "children"),
        [Input(own_ids.METHOD_DROPDOWN, "value"), 
         Input(own_ids.DATE_RANGE, "start_date"),
         Input(own_ids.DATE_RANGE, "end_date")]
    )
    # function that updates the bar chart -> recieves a list of strings
    # return the children of bar_chart
    def update_bar_chart(methods: list[str], start_date, end_date) -> html.Div:
        # argument that changes is 'methods'
        # change in dropdown gives list of methods
        # filter the table for the methods specified
        # filter table for dates specified
        filtered_data = data[(data["Announcement Date"] > start_date) & (data["Announcement Date"] < end_date)]
        if methods in list(data["CDR Method"].dropna().unique()):
            filtered_data = filtered_data[data["CDR Method"] == methods]
            # filtered_data = data[data["CDR Method"].isin(methods)]

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=own_ids.S_CHART)

        # creating the relevant graph "TOP_TEN_SUPPLIERS"
        fig = bar_plot.build_plot(filtered_data[["Supplier", "Tons Purchased"]], h=1)

        return html.Div(dcc.Graph(figure=fig), id=own_ids.S_CHART)

    return html.Div(id=own_ids.S_CHART)
