import copy

from dash import html, Output, Input, State, dcc
from dash_extensions.enrich import (DashProxy,
                                    ServersideOutputTransform,
                                    MultiplexerTransform)
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
from queries import read_data
from datetime import datetime
import numpy as np
import pandas as pd
from colors import get_colors, update_colors

CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '500px'})


class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)


app = EncostDash(name=__name__)

df = read_data()


def create_timeline(colors: dict):
    # customdata = np.stack((
    #     df['state'],
    #     df['reason'],
    #     df['state_begin'],
    #     df['duration_min'],
    #     df['shift_day'],
    #     df['shift_name'],
    #     df['operator']
    # ), axis=-1)
    #
    tl = px.timeline(df, x_start="state_begin", x_end="state_end",
                     color_discrete_map=colors,
                     color='state', y="client_name", custom_data=['state', 'reason', 'state_begin', 'duration_min',
                                                                  'shift_day', 'shift_name', 'operator'])
    tl.update_layout(showlegend=True, xaxis_title='', yaxis_title='')
    tl.update_traces(hovertemplate='Состояние %{customdata[0]}<br>'
                                   'Причина: %{customdata[1]}<br>'
                                   'Начало %{customdata[2]|%Y-%m-%d %H:%M:%S}<br>'
                                   'Длительность: %{customdata[3]:.2f} мин<br><br>'
                                   'Сменный день: %{customdata[4]|%Y-%m-%d}<br>'
                                   'Смена %{customdata[5]}<br>'
                                   'Оператор: %{customdata[6]}<br>'
                     )
    return tl


color_map = get_colors()
my_pie = px.pie(df, values='duration_hour', names='state',
                color='state', color_discrete_map=color_map)
my_tl = create_timeline(color_map)
chooses = [x for x in color_map.keys()]
chooses.append("Все состояния")


def get_layout():
    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                        dcc.Dropdown(
                            chooses,
                            id='input'),
                        dmc.Button(
                            'Фильтровать',
                            id='button1'),
                        html.Div(
                            id='output')],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(figure=my_pie)
                    ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(figure=my_tl,
                                  id='timeline')
                    ],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl", )
        ])
    ])


app.layout = get_layout()


@app.callback(
    Output('timeline', 'figure'),
    State('input', 'value'),
    Input('button1', 'n_clicks'),
    # prevent_initial_call=True,
)
def update_div1(
        value,
        click
):
    if click is None:
        raise PreventUpdate
    up_tl = create_timeline(update_colors(value))
    return up_tl


if __name__ == '__main__':
    app.run_server(debug=True)
