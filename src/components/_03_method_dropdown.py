from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output
import pandas as pd

from . import _00_own_ids

# render function returns a Div that can be added to the layout
def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # defines what objects can be picked from the dropdown
    methods = list(data["CDR Method"].dropna().unique())
    methods.insert(0, "All Methods")

    # communication is enabled using callbacks and the ids of the objects
    @app.callback(
        # output: what object is changed -> dropdown value
        Output(_00_own_ids.METHOD_DROPDOWN, "value"),
        # input: what object creates the input -> select all button and inout is the # of clicks
        Input(_00_own_ids.SELECT_ALL_METHODS_BUTTON, "n_clicks"),
    )
    # function that is changed when callback recognizes a change
    # input argument for the function is always the parameter that is observed from the input object
    # returns a list of strings
    # _:int -> only listen whether parameter changed, actual value of the int is not interesting
    def select_all_methods(btn1):
        # only if button is triggered return all methods
        if _00_own_ids.SELECT_ALL_METHODS_BUTTON == ctx.triggered_id:
            return "All Methods"
        else:
            return "Biochar"

    # return said html.Div object with children
    return html.Div(
        children=[
            # heading 6
            html.H6("CDR Methods"),
            # dropdown component
            html.Div(
                children=[
                    html.Div(
                        className="dropdown-div",
                        children=[
                            dcc.Dropdown(
                                # id makes it able to refer to this dropdown in other files
                                id=_00_own_ids.METHOD_DROPDOWN,
                                # options needs to be a list of a dict containing objects + label of the object (same here)
                                options=[{"label": meth, "value": meth} for meth in methods],
                                # setting initial value (here all_methods => all objects of dropdown) [doesn't actually work bc of select all]
                                value=methods[0],
                                # able to select multiple objects of the dropdown
                                multi=False,
                                searchable=True
                            )
                        ]
                    ),
                    # adding a button that allows to select all at once
                    html.Button(
                        className="dropdown-button",
                        # only object in the Button class is its title
                        children=["Select All"],
                        # need id that lets us refer to the button
                        id=_00_own_ids.SELECT_ALL_METHODS_BUTTON,
                        # # clicks is the parameter that the callback function listens to
                        n_clicks=0,
                    )
                ]
            )
        ]
    )
