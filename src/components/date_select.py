from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
from dateutil.relativedelta import relativedelta
import datetime as dt
import pandas as pd

from . import own_ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # find the max and min date of the announcement date column
    # have to use dropna, to ignore the nan values in the evaluation
    min_date = dt.datetime.strptime(min(data["Announcement Date"].dropna()), "%Y-%m-%d").date()
    max_date = dt.datetime.strptime(max(data["Announcement Date"].dropna()), "%Y-%m-%d").date()

    @app.callback(
        # output: adjusted start and end date
        [Output(own_ids.DATE_RANGE, "start_date"),
         Output(own_ids.DATE_RANGE, "end_date")],
        # input: # of clicks for the WHOLE_RANGE button
        [Input(own_ids.SELECT_WHOLE_RANGE_BUTTON, "n_clicks"),
         Input(own_ids.SELECT_LAST_MONTH_BUTTON, "n_clicks"),
         Input(own_ids.SELECT_LAST_YEAR_BUTTON, "n_clicks")],
    )
    # just evaluate if value changed (# of clicks is not relevant)
    def update_range(btn1, btn2, btn3):
        min_date = dt.datetime.strptime(min(data["Announcement Date"].dropna()), "%Y-%m-%d").date()
        max_date = dt.datetime.strptime(max(data["Announcement Date"].dropna()), "%Y-%m-%d").date()
        # whole range button does not need an if statement -> just returns min, max date

        # Select last 30 days button
        if own_ids.SELECT_LAST_MONTH_BUTTON == ctx.triggered_id:
            min_date = max_date - dt.timedelta(30)
        # Select last year button
        elif own_ids.SELECT_LAST_YEAR_BUTTON == ctx.triggered_id:
            min_date = max_date - relativedelta(years=1)
        return min_date, max_date

    return html.Div(
        children=[
            # heading 6
            html.H6("Select Date Range"),
            html.Div(
                # dropdown component
                dcc.DatePickerRange(
                    id=own_ids.DATE_RANGE,
                    month_format='MMMM YYYY',
                    start_date=min_date,
                    end_date=max_date
                )
            ),
            html.Div(
                className="date-button-group",
                children=[
                    html.Button(
                        className="date-button",
                        # only object in the Button class is its title
                        children=["Whole range"],
                        # need id that lets us refer to the button
                        id=own_ids.SELECT_WHOLE_RANGE_BUTTON,
                        # # clicks is the parameter that the callback function listens to
                        n_clicks=0,
                    ),
                    html.Button(
                        className="date-button",
                        # only object in the Button class is its title
                        children=["Last year"],
                        # need id that lets us refer to the button
                        id=own_ids.SELECT_LAST_YEAR_BUTTON,
                        # # clicks is the parameter that the callback function listens to
                        n_clicks=0,
                        style={"margin-left": "5px"}
                    ),
                    html.Button(
                        className="date-button",
                        # only object in the Button class is its title
                        children=["Last 30 days"],
                        # need id that lets us refer to the button
                        id=own_ids.SELECT_LAST_MONTH_BUTTON,
                        # # clicks is the parameter that the callback function listens to
                        n_clicks=0,
                        style={"margin-left": "5px"}
                    )
                ]
            )
        ]
    )
