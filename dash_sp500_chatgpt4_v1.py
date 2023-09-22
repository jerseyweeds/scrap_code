### WORKING COPY ###
# https://chat.openai.com/c/375cbf1a-3d07-4153-bd64-9a9d04a4cfcc

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
#from dash_extensions import Download
#from dash_extensions.snippets import send_data_frame

import plotly.express as px
import pandas as pd
import numpy as np

pd.set_option('display.float_format', '{:.10f}'.format)


# Simulating 52-week data
weeks = pd.date_range(start='2022-01-01', periods=52, freq='W')
companies = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'MA']
sectors = ['Technology', 'Technology', 'Technology', 'Retail', 'Technology', 'Automotive', 'Technology', 'Finance', 'Finance', 'Finance']

data = []

for company, sector in zip(companies, sectors):
    earnings = np.random.uniform(20, 60, size=52)
    market_cap = np.random.uniform(1000, 2500, size=52)
    pe_ratio = market_cap / earnings

    for week, earning, m_cap, pe in zip(weeks, earnings, market_cap, pe_ratio):
        data.append([company, sector, week, earning, m_cap, pe])

original_df = pd.DataFrame(data, columns=['Company', 'Sector', 'Week', 'Earnings', 'Market_Cap', 'PE_Ratio'])
original_df['PE_Ratio'] = original_df['PE_Ratio'].round(1)


df = original_df.copy()

# Sort the sectors
sorted_sectors = sorted(df['Sector'].unique())

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': s, 'value': s} for s in sorted_sectors],
        value=sorted_sectors,
        multi=True
    ),
    
    dcc.Graph(id='graph'),
    
    dcc.Dropdown(
        id='company-dropdown',
        options=[{'label': c, 'value': c} for c in companies],
        value=companies,
        multi=True
    ),
    
  
    dash_table.DataTable(
        id='table',
        style_table={'overflowX': 'scroll'},
        page_size=20,
        row_selectable='multi'
    ),
    
    html.Button('Remove Selected Rows', id='remove-button'),
    html.Button('Reset', id='reset-button'),
    html.Button("Download Data", id="btn_csv"),
    dcc.Download(id="download"),
])

@app.callback(
    [Output('graph', 'figure'),
     Output('table', 'data'),
     Output('table', 'columns')],
    [Input('company-dropdown', 'value'),
     Input('sector-dropdown', 'value'),
     Input('remove-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('table', 'selected_rows'),
     State('table', 'data')]
)
def update(selected_companies, selected_sectors, n_remove_clicks, n_reset_clicks, selected_rows, table_data):
    ctx = dash.callback_context

    if not selected_companies or not selected_sectors:
        selected_companies = companies
        selected_sectors = sorted_sectors

    if not ctx.triggered:
        filtered_df = original_df.copy()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        filtered_df = df[df['Company'].isin(selected_companies) & df['Sector'].isin(selected_sectors)]

        if button_id == 'remove-button':
            if selected_rows is not None:
                for i in sorted(selected_rows, reverse=True):
                    del table_data[i]
                # Convert back to DataFrame after removing rows
                filtered_df = pd.DataFrame(table_data)
                if 'Sector' in filtered_df.columns and 'Company' in filtered_df.columns:
                    filtered_df = filtered_df.melt(id_vars=['Sector', 'Company'], var_name='Week', value_name='PE_Ratio')
                else:
                    return dash.no_update, dash.no_update, dash.no_update
        elif button_id == 'reset-button':
            filtered_df = original_df.copy()

    # Plot
    fig = px.line(filtered_df, x='Week', y='PE_Ratio', color='Company', line_dash='Sector')

    # Pivot and reset index
    pivoted_df = pd.pivot_table(
        filtered_df,
        values='PE_Ratio',
        index=['Sector', 'Company'],
        columns='Week'
    ).reset_index()
    

    # Cast the Week columns to string with format YYYY-MM-DD
    pivoted_df.columns = [str(col).split(' ')[0] if isinstance(col, pd.Timestamp) else str(col) for col in pivoted_df.columns]

    table_data = pivoted_df.to_dict('records')
    table_columns = [{'name': str(i), 'id': str(i)} for i in pivoted_df.columns]

    return fig, table_data, table_columns



@app.callback(
    Output("download", "data"),
    [Input("btn_csv", "n_clicks"),
     State("table", "data")],
)
def generate_csv(n_clicks, table_data):
    if not n_clicks:
        return dash.no_update

    df_to_download = pd.DataFrame.from_dict(table_data)
    return send_data_frame(df_to_download.to_csv, "download.csv", index=False)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='3000')
