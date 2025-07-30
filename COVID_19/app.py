import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# CSS elements
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': '<KEY>',
        'crossorigin': 'anonymous'
    }
]

patients=pd.read_csv('IndividualDetails.csv')
total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

options=[
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([html.H1('Corona Virus Pandemic', style={'color': '#fff', 'textAlign': 'center'}),
                       html.Div([
                           html.Div([
                               html.Div([
                                   html.Div([
                                       html.H3('Total Cases', className='text-light'),
                                       html.H4(total, className='text-light')
                                   ], className='card-body')
                               ], className='card bg-danger')
                           ], className='col-md-3'),
                           html.Div([
                               html.Div([
                                   html.Div([
                                       html.H3('Active', className='text-light'),
                                       html.H4(active, className='text-light')
                                   ], className='card-body')
                               ], className='card bg-info')
                           ], className='col-md-3'),
                           html.Div([
                               html.Div([
                                   html.Div([
                                       html.H3('Recovered', className='text-light'),
                                       html.H4(recovered, className='text-light')
                                   ], className='card-body')
                               ], className='card bg-warning')
                           ], className='col-md-3'),
                           html.Div([
                               html.Div([
                                   html.Div([
                                       html.H3('Deaths', className='text-light'),
                                       html.H4(deaths, className='text-light')
                                   ], className='card-body')
                               ], className='card bg-success')
                           ], className='col-md-3')
                       ], className='row'), html.Div([
        html.Div([], className='col-md-6'),
        html.Div([], className='col-md-6')
    ], className='row'), html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options, value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ], className='col-md-12')
    ], className='row')
                       ], className='container')
@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):
    if type=='Deceased':
        npat = patients[patients['current_status']=='Deceased']
        npat = npat.dropna(subset=['detected_state'])

        pbar=npat['detected_state'].value_counts().reset_index()
        pbar.columns=['State','Count']

        return {'data': [go.Bar(x=pbar['State'],y=pbar['Count'])],
                'layout': go.Layout(title='Deceased Pandemic',)}

    elif type == 'Hospitalized':
        npat = patients[patients['current_status'] == 'Hospitalized']
        npat = npat.dropna(subset=['detected_state'])

        pbar = npat['detected_state'].value_counts().reset_index()
        pbar.columns = ['State', 'Count']

        return {'data': [go.Bar(x=pbar['State'],y=pbar['Count'])],
            'layout': go.Layout(title='State-wise Hospitalized Count')}

    elif type == 'Recovered':
        npat = patients[patients['current_status'] == 'Recovered']
        npat = npat.dropna(subset=['detected_state'])

        pbar = npat['detected_state'].value_counts().reset_index()
        pbar.columns = ['State', 'Count']

        return {'data': [go.Bar(x=pbar['State'], y=pbar['Count'])],
         'layout': go.Layout(title='State-wise Recovered Count ')}

    else:
        pbar=patients['detected_state'].value_counts().reset_index()
        pbar.columns= ['State','Count']
        return {'data': [go.Bar(x=pbar['State'], y=pbar['Count'])],
                'layout': go.Layout(title='State Total Count')}

if __name__ == '__main__':
    app.run(debug=True)


