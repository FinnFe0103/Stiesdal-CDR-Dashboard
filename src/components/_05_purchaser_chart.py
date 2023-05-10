import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import _00_own_ids, _04_bar_plot

# render function again receives a dash app and returns a Div object
def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # Output: chaning bar-chart, updating the children of that Div
    # Input: dropdown, get value
    @app.callback(
        Output(_00_own_ids.P_CHART, "children"),
        [Input(_00_own_ids.METHOD_DROPDOWN, "value"), 
         Input(_00_own_ids.DATE_RANGE, "start_date"),
         Input(_00_own_ids.DATE_RANGE, "end_date")]
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
            filtered_data = filtered_data[filtered_data["CDR Method"] == methods]

        # filter the dataframe to exclude "Aggregate Purchase" and "Unallocated Pre Pruchase" as a Purchaser
        filtered_data = filtered_data[~filtered_data["Purchaser"].isin(["Aggregate Purchase", "Unallocated Pre-Purchase"])]

        #if filtered_data.shape[0] == 0:
        #    return html.Div("No data selected.", id=_00_own_ids.P_CHART)

        # creating the relevant graph "TOP_TEN_SUPPLIERS"
        fig = _04_bar_plot.build_plot(filtered_data[["Purchaser", "Tons Purchased"]], h=1)

        return html.Div(dcc.Graph(figure=fig), id=_00_own_ids.P_CHART)

    return html.Div(id=_00_own_ids.P_CHART)
