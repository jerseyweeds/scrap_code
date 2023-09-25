### WORKING COPY ###
# https://chat.openai.com/c/375cbf1a-3d07-4153-bd64-9a9d04a4cfcc
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np

# Simulating 52-week data
weeks = pd.date_range(start='2022-01-01', periods=52, freq='W')
companies = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'NVDA', 'JPM', 'V', 'MA']
sectors = ['Technology', 'Technology', 'Technology', 'Retail', 'Technology', 'Automotive', 'Technology', 'Finance', 'Finance', 'Finance']

data = []

for company, sector in zip(companies, sectors):
    earnings = np.random.uniform(20, 60, size=52)
    market_cap = np.random.uniform(1000, 2500, size=52)

    for week, earning, m_cap in zip(weeks, earnings, market_cap):
        data.append([company, sector, week, earning, m_cap])

original_df = pd.DataFrame(data, columns=['Company', 'Sector', 'Week', 'Earnings', 'Market_Cap'])
df = original_df.copy()

# Sort the sectors
sorted_sectors = sorted(df['Sector'].unique())

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id='company-dropdown',
        options=[{'label': c, 'value': c} for c in companies],
        value=companies,
        multi=True
    ),
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': s, 'value': s} for s in sorted_sectors],
        value=sorted_sectors,
        multi=True
    ),
    html.Button('Remove Selected Rows', id='remove-button'),
    html.Button('Reset', id='reset-button'),
    html.Div("Company Data Table"),
    dash_table.DataTable(
        id='table',
        style_table={'overflowX': 'scroll'},
        page_size=20,
        row_selectable='multi'
    ),
    html.Div("Summary Data Table"),
    dash_table.DataTable(
        id='summary-table',
        style_table={'overflowX': 'scroll'},
        page_size=5
    )
])

@app.callback(
    [Output('graph', 'figure'),
     Output('table', 'data'),
     Output('table', 'columns'),
     Output('summary-table', 'data'),
     Output('summary-table', 'columns')],
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

        # ... [Rest of the button operations]

    # Assign quintiles for each week based on 'Market_Cap'
    filtered_df['Quintile'] = filtered_df.groupby('Week')['Market_Cap'].transform(
        lambda x: pd.qcut(x, 5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
    )

    # Calculate median market cap for each quintile and week
    quintile_df = filtered_df.groupby(['Week', 'Quintile']).agg({
        'Market_Cap': 'median'
    }).reset_index()

    # Plot
    fig = px.line(quintile_df, x='Week', y='Market_Cap', color='Quintile', title='Median Market Cap by Quintile Over Time')

    # Pivot and reset index for the main table
    pivoted_df = pd.pivot_table(
        filtered_df,
        values='Market_Cap',
        index=['Sector', 'Company'],
        columns='Week'
    ).reset_index()

    # Round numerical values to 1 decimal place and format columns
    for col in pivoted_df.columns:
        if isinstance(col, pd.Timestamp) or col in ['Market_Cap']:
            pivoted_df[col] = pivoted_df[col].round(1)
    pivoted_df.columns = [str(col).split(' ')[0] if isinstance(col, pd.Timestamp) else str(col) for col in pivoted_df.columns]

    table_data = pivoted_df.to_dict('records')
    table_columns = [{'name': str(i), 'id': str(i)} for i in pivoted_df.columns]

    # Pivot and reset index for the summary table
    summary_pivoted_df = pd.pivot_table(
        quintile_df,
        values='Market_Cap',
        index=['Quintile'],
        columns='Week'
    ).reset_index()

    # Round numerical values to 1 decimal place and format columns
    for col in summary_pivoted_df.columns:
        if isinstance(col, pd.Timestamp) or col in ['Market_Cap']:
            summary_pivoted_df[col] = summary_pivoted_df[col].round(1)
    summary_pivoted_df.columns = [str(col).split(' ')[0] if isinstance(col, pd.Timestamp) else str(col) for col in summary_pivoted_df.columns]

    summary_table_data = summary_pivoted_df.to_dict('records')
    summary_table_columns = [{'name': str(i), 'id': str(i)} for i in summary_pivoted_df.columns]

    return fig, table_data, table_columns, summary_table_data, summary_table_columns

if __name__ == '__main__':
    app.run(jupyter_mode="external", port='22222')
