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
        Output(_00_own_ids.PIE_CHART, "children"),
        [Input(_00_own_ids.METHOD_DROPDOWN, "value"), 
         Input(_00_own_ids.DATE_RANGE, "start_date"),
         Input(_00_own_ids.DATE_RANGE, "end_date")]
    )
    # function that updates the bar chart -> recieves a list of strings
    # return the children of bar_chart
    def update_pie_chart(methods: list[str], start_date, end_date) -> html.Div:
        # argument that changes is 'methods'
        # change in dropdown gives list of methods
        # filter the table for the methods specified
        # filter table for dates specified
        filtered_data = data[(data["Announcement Date"] > start_date) & (data["Announcement Date"] < end_date)]
        


        filtered_data = filtered_data[["CDR Method", "Tons Purchased/Sold"]].groupby(["CDR Method"]).sum()

        fig = go.Figure()
        if methods in list(data["CDR Method"].dropna().unique()):
            group = filtered_data.drop([methods]).sum(axis=0).rename({"Tons Purchased/Sold": "Other Methods"})
            single = filtered_data.loc[methods].rename({"Tons Purchased/Sold": methods})
            new = pd.DataFrame(pd.concat([group, single]), columns=["Tons Purchased/Sold"])
            fig = go.Figure(data=go.Pie(labels=new.index, values=new["Tons Purchased/Sold"], pull=[0, 0.2], textinfo='percent+label', textposition='inside'))
            fig.update_traces(textposition='outside', textinfo='percent+label', marker=dict(colors=['E5ECF6', '00497A']))
            fig.update_layout(showlegend=False, height=600, width=960, title="Share of"+str(methods)+" Tons Purchased/Sold")
        elif methods == "All Methods":

            fig = go.Figure(data=go.Pie(labels=filtered_data.index, values=filtered_data["Tons Purchased/Sold"], textinfo='percent+label', textposition='outside'))
            fig.update_traces(textposition='outside', textinfo='percent+label', marker=dict(colors=['acc2e2', '00497A', "001b2e", "002a47", "00365f", "00497a", "005e94", "0070b0", "0083cb", "0098e3"]))
            fig.update_layout(showlegend=False, height=600, width=960, title="Share of Tons Purchased/Sold by Method")

        return html.Div(dcc.Graph(figure=fig), id=_00_own_ids.PIE_CHART)

    return html.Div(id=_00_own_ids.PIE_CHART)
