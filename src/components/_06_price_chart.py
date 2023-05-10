import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import _00_own_ids

# render function again receives a dash app and returns a Div object
def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # Output: chaning bar-chart, updating the children of that Div
    # Input: dropdown, get value
    @app.callback(
        Output(_00_own_ids.PPT_CHART, "children"),
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

        fig = go.Figure()

        if methods in list(data["CDR Method"].dropna().unique()):
            filtered_data = filtered_data[filtered_data["CDR Method"] == methods].dropna(subset=["Price per Ton"]).sort_values("Announcement Date")
            fig = px.line(filtered_data, x="Announcement Date", y="Price per Ton", title="Price per Ton over Time", height=600, width=960, hover_data={"Supplier": True}, markers=True)
            fig.update_layout(xaxis_title="Announcement Date", yaxis_title="Price per Ton", showlegend=False)
            fig.update_traces(line_color="#00497a")

        elif methods == "All Methods":
            filtered_data = filtered_data.dropna(subset=["Price per Ton"]).sort_values("Announcement Date")
            fig = px.line(filtered_data, x="Announcement Date", y="Price per Ton", color="CDR Method", title="Price per Ton over Time", height=600, width=960, markers=True)
            #fig.update_traces(line_color="#00497a")
        
        return html.Div(dcc.Graph(figure=fig), id=_00_own_ids.PPT_CHART)

    return html.Div(id=_00_own_ids.PPT_CHART)
