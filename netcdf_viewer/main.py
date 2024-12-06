import argparse
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import xarray as xr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')

    args = parser.parse_args()
    path = Path(args.path).expanduser()

    try:
        ds = xr.open_dataset(path)
    except ValueError:
        ds = xr.open_dataset(path, decode_times=False)

    data_vars = list(ds.data_vars)
    data_var = data_vars[0]

    zmin = ds[data_var].min().values
    zmax = ds[data_var].max().values

    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    controls = [
        dash.html.Div([
            dash.html.Label('Var', htmlFor='var', style={'font-weight': 'bold'}),
            dbc.Select(id='var', value=data_vars[0], options=[
                {'label': data_var, 'value': data_var} for data_var in data_vars
            ])
        ], style={'width': '20vw'}),
        dash.html.Div([
            dash.html.Label('Time', htmlFor='number', style={'font-weight': 'bold'}),
            dbc.Input(id='time', type='number', value=0, min=0, max=ds.sizes.get('time', 0))
        ], className='me-auto', style={'width': '10vw'}),
        dash.html.Div([
            dash.html.Label('z min', htmlFor='number', style={'font-weight': 'bold'}),
            dbc.Input(id='zmin', type='number', value=zmin)
        ], style={'width': '10vw'}),
        dash.html.Div([
            dash.html.Label('z max', htmlFor='number', style={'font-weight': 'bold'}),
            dbc.Input(id='zmax', type='number', value=zmax)
        ], style={'width': '10vw'})
    ]

    app.layout = dash.html.Div([
        dash.html.Div(controls, className="d-flex flex-row gap-3 shadow p-3 mb-3 rounded"),
        dash.dcc.Graph(id='graph', className="flex-grow-1 shadow p-3 rounded")
    ], className='position-absolute top-0 end-0 bottom-0 start-0 d-flex flex-column gap-3 p-3')

    @dash.callback(
        dash.Output('graph', 'figure'),
        (
            dash.Input('var', 'value'),
            dash.Input('time', 'value'),
            dash.Input('zmin', 'value'),
            dash.Input('zmax', 'value')
        )
    )
    def update_graph(var_name, time_index, zmin, zmax):
        data = ds[var_name or data_vars[0]]
        if 'time' in ds.dims:
            data = data.isel(time=time_index or 0)

        fig = px.imshow(data, origin='lower', aspect='equal', zmin=zmin, zmax=zmax)
        fig.update_coloraxes(colorbar_title_side='right')
        fig['layout']['uirevision'] = True
        return fig

    app.run(debug=True)
