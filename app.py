import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser" # this is required to plot in browser

retail = pd.read_csv("retail_trade.csv", dtype = {'Year':object})
retail


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

year_options = retail['Year'].unique()
category_options = retail['Category'].unique()


app.layout = html.Div([
    html.Div([
        
        html.H1('Retail Trade - US', style={'text-align':'left','font-family':'open sans light'}),
    
        html.Div([
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': i, 'value': i} for i in year_options],
                value='2021')
                ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': i, 'value': i} for i in category_options],
                value='Clothing/Fashion')
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
            ]),
    
            dcc.Graph(id='retail-graphic')
    
])

@app.callback(
    Output('retail-graphic', 'figure'),
    Input('year-filter', 'value'),
    Input('category-filter','value'))
def update_figure(selected_year,
                  selected_category):
    
    filtered_df = retail[(retail['Year'] == selected_year)  & (retail['Category'] == selected_category)]
    
    fig = px.bar(filtered_df, x='Retail Type', y='Sales', 
                 barmode='group', height = 500)

    fig.update_layout(xaxis_tickangle=45, showlegend=False, xaxis={'categoryorder':'total descending'})
    fig.update_xaxes(tickfont=dict(size=8))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
