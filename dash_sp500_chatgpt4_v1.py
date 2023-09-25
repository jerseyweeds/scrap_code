### WORKING COPY ###
# https://chat.openai.com/c/375cbf1a-3d07-4153-bd64-9a9d04a4cfcc
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px

# Sample data generation
np.random.seed(42)
companies = ["Apple", "Google", "Microsoft", "Amazon", "Facebook", "Tesla", "Netflix", "Disney", "Zoom", "Slack"]
sectors = ["Tech", "Entertainment", "Tech", "Retail", "Tech", "Automotive", "Entertainment", "Entertainment", "Tech", "Tech"]

dates = pd.date_range("2022-01-01", periods=52, freq="W")
original_df = pd.DataFrame({
    "Date": np.tile(dates, len(companies)),
    "Company": np.repeat(companies, len(dates)),
    "Sector": np.repeat(sectors, len(dates)),
    "Earnings": np.random.rand(len(dates) * len(companies)) * 1e9,
    "Market Cap": np.random.rand(len(dates) * len(companies)) * 1e11,
})
original_df["PE_Ratio"] = original_df["Market Cap"] / original_df["Earnings"]

global df
df = original_df.copy()

app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("S&P 500 P/E Ratio Analysis"),
    html.Label("Select Companies:"),
    dcc.Dropdown(
        id='company-dropdown',
        options=[{'label': company, 'value': company} for company in companies],
        value=companies,
        multi=True
    ),
    html.Label("Select Sectors:"),
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': sector, 'value': sector} for sector in sorted(df['Sector'].unique())],
        value=sorted(df['Sector'].unique()),
        multi=True
    ),
    dcc.Graph(id='graph'),
    html.Button('Remove Selected Rows', id='remove-button', n_clicks=0),
    html.Button('Reset', id='reset-button', n_clicks=0),
    dash_table.DataTable(
        id='table',
        row_selectable='multi',
        page_size=20
    ),
    html.H3("Quintile Summary"),
    dash_table.DataTable(
        id='summary-table'
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
    global df
    ctx = dash.callback_context

    if not ctx.triggered:
        filtered_df = df.copy()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'reset-button':
            df = original_df.copy()

        if button_id == 'remove-button' and selected_rows is not None:
            rows_to_remove = [table_data[idx] for idx in selected_rows]
            companies_to_remove = [row['Company'] for row in rows_to_remove]
            df = df[~df['Company'].isin(companies_to_remove)]

        filtered_df = df[df['Company'].isin(selected_companies) & df['Sector'].isin(selected_sectors)]

    quintile_labels = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    filtered_df['Quintile'] = filtered_df.groupby('Date')['Market Cap'].transform(
        lambda x: pd.qcut(x, 5, labels=quintile_labels)
    )

    quintile_df = filtered_df.groupby(['Date', 'Quintile']).sum().reset_index()
    fig = px.line(quintile_df, x="Date", y="Market Cap", color="Quintile", title="Market Cap by Quintile Over Time")

    pivoted_df = filtered_df.pivot_table(index=['Sector', 'Company'], columns='Date', values='PE_Ratio').reset_index()
    summary_pivoted_df = quintile_df.pivot_table(index='Quintile', columns='Date', values='Market Cap').reset_index()

    pivoted_df.columns = [str(col).split(' ')[0] if isinstance(col, pd.Timestamp) else str(col) for col in pivoted_df.columns]
    summary_pivoted_df.columns = [str(col).split(' ')[0] if isinstance(col, pd.Timestamp) else str(col) for col in summary_pivoted_df.columns]

    table_data = pivoted_df.to_dict('records')
    table_columns = [{'name': str(i), 'id': str(i)} for i in pivoted_df.columns]

    summary_table_data = summary_pivoted_df.to_dict('records')
    summary_table_columns = [{'name': str(i), 'id': str(i)} for i in summary_pivoted_df.columns]

    return fig, table_data, table_columns, summary_table_data, summary_table_columns

# if __name__ == '__main__':
#     app.run_server(debug=True)


if __name__ == '__main__':
    app.run(jupyter_mode="external", port='22222')
