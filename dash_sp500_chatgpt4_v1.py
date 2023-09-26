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

pd.set_option('display.float_format', '{:.1f}'.format)


# Simulating 52-week data
weeks = pd.date_range(start='2022-01-01', periods=26, freq='W')
companies = ["Las Vegas Sands Corp.", "Salesforce, Inc.", "Molson Coors Beverage Company", "Welltower Inc.", "Palo Alto Networks, Inc.", "Insulet Corporation", "NVIDIA Corporation", "Ventas, Inc.", "Catalent, Inc.", "STERIS plc (Ireland)", "Axon Enterprise, Inc.", "Clorox Company (The)", "First Solar, Inc.", "DexCom, Inc.", "Amazon.com, Inc.", "Tyler Technologies, Inc.", "Digital Realty Trust, Inc.", "Merck & Company, Inc.", "Cardinal Health, Inc.", "Equinix, Inc.", "Align Technology, Inc.", "American Tower Corporation (REIT)", "Boston Scientific Corporation", "News Corporation", "CoStar Group, Inc.", "News Corporation", "Live Nation Entertainment, Inc.", "ServiceNow, Inc.", "Eli Lilly and Company", "Intuitive Surgical, Inc.", "Walt Disney Company (The)", "Verisk Analytics, Inc.", "Cadence Design Systems, Inc.", "V.F. Corporation", "International Business Machines Corporation", "Invitation Homes Inc.", "Synopsys, Inc.", "The Cooper Companies, Inc.", "Intuit Inc.", "Tesla, Inc.", "Tyson Foods, Inc.", "West Pharmaceutical Services, Inc.", "Estee Lauder Companies, Inc. (The)", "Camden Property Trust", "PTC Inc.", "Xylem Inc.", "S&P Global Inc.", "Quanta Services, Inc.", "Monolithic Power Systems, Inc.", "Autodesk, Inc.", "Church & Dwight Company, Inc.", "Paycom Software, Inc.", "Fair Isaac Corporation", "IDEXX Laboratories, Inc.", "Rollins, Inc.", "Duke Energy Corporation (Holding Company)", "Zimmer Biomet Holdings, Inc.", "Becton, Dickinson and Company", "ANSYS, Inc.", "Adobe Inc.", "SBA Communications Corporation", "Generac Holdings Inc.", "Chipotle Mexican Grill, Inc.", "Progressive Corporation (The)", "Transdigm Group Inc.", "Iron Mountain Incorporated (Delaware)", "MSCI Inc.", "FirstEnergy Corp.", "Equifax, Inc.", "Bio-Techne Corp", "Constellation Energy Corporation", "Corning Incorporated", "Ecolab Inc.", "L3Harris Technologies, Inc.", "Netflix, Inc.", "Arthur J. Gallagher & Co.", "Fortinet, Inc.", "Monster Beverage Corporation", "Realty Income Corporation", "Moody’s Corporation", "Brown Forman Inc", "Colgate-Palmolive Company", "Roper Technologies, Inc.", "MGM Resorts International", "Global Payments Inc.", "Costco Wholesale Corporation", "Incyte Corporation", "Stryker Corporation", "Corteva, Inc.", "Vulcan Materials Company (Holding Company)", "Ingersoll Rand Inc.", "A.O. Smith Corporation", "Howmet Aerospace Inc.", "Zoetis Inc.", "Trimble Inc.", "Oracle Corporation", "Hologic, Inc.", "Intercontinental Exchange Inc.", "Cintas Corporation", "Moderna, Inc.", "Southwest Airlines Company", "MarketAxess Holdings, Inc.", "IQVIA Holdings, Inc.", "Mastercard Incorporated", "Electronic Arts Inc.", "Thermo Fisher Scientific Inc", "Copart, Inc.", "Abbott Laboratories", "Johnson & Johnson", "Alaska Air Group, Inc.", "Old Dominion Freight Line, Inc.", "Akamai Technologies, Inc.", "Alexandria Real Estate Equities, Inc.", "Fortive Corporation", "Edwards Lifesciences Corporation", "Weyerhaeuser Company", "Broadridge Financial Solutions, Inc.", "Arista Networks, Inc.", "Activision Blizzard, Inc", "Meta Platforms, Inc.", "Enphase Energy, Inc.", "FactSet Research Systems Inc.", "Prologis, Inc.", "McCormick & Company, Incorporated", "Linde plc", "Microsoft Corporation", "Nike, Inc.", "Eaton Corporation, PLC", "Hilton Worldwide Holdings Inc.", "Motorola Solutions, Inc.", "SolarEdge Technologies, Inc.", "Kimco Realty Corporation (HC)", "Agilent Technologies, Inc.", "PepsiCo, Inc.", "CBRE Group Inc", "Baker Hughes Company", "Prudential Financial, Inc.", "Jack Henry & Associates, Inc.", "AbbVie Inc.", "Visa Inc.", "Automatic Data Processing, Inc.", "Walmart Inc.", "Fiserv, Inc.", "Sherwin-Williams Company (The)", "Teradyne, Inc.", "Hess Corporation", "Keurig Dr Pepper Inc.", "Mettler-Toledo International, Inc.", "VeriSign, Inc.", "Westinghouse Air Brake Technologies Corporation", "Danaher Corporation", "Starbucks Corporation", "Republic Services, Inc.", "Fastenal Company", "Apple Inc.", "CVS Health Corporation", "Aptiv PLC", "Air Products and Chemicals, Inc.", "Equity Residential", "Comcast Corporation", "American Water Works Company, Inc.", "Medtronic plc.", "AMETEK, Inc.", "Marsh & McLennan Companies, Inc.", "Essex Property Trust, Inc.", "UDR, Inc.", "Regency Centers Corporation", "Domino’s Pizza Inc", "Waste Management, Inc.", "CarMax Inc", "Gartner, Inc.", "IDEX Corporation", "Martin Marietta Materials, Inc.", "F5, Inc.", "Mid-America Apartment Communities, Inc.", "Paychex, Inc.", "Edison International", "Teleflex Incorporated", "Amphenol Corporation", "Brown & Brown, Inc.", "Match Group, Inc.", "ResMed Inc.", "Alphabet Inc.", "T-Mobile US, Inc.", "Accenture plc", "Alphabet Inc.", "Freeport-McMoRan, Inc.", "Vertex Pharmaceuticals Incorporated", "EPAM Systems, Inc.", "Kimberly-Clark Corporation", "Booking Holdings Inc. Common Stock", "Otis Worldwide Corporation", "TJX Companies, Inc. (The)", "Broadcom Inc.", "Nordson Corporation", "Yum! Brands, Inc.", "O’Reilly Automotive, Inc.", "PPL Corporation", "McDonald’s Corporation", "Procter & Gamble Company (The)", "Avery Dennison Corporation", "Crown Castle Inc.", "CDW Corporation", "Aon plc", "Coca-Cola Company (The)", "Ross Stores, Inc.", "The Hershey Company", "Teledyne Technologies Incorporated", "PPG Industries, Inc.", "Analog Devices, Inc.", "CME Group Inc.", "Parker-Hannifin Corporation", "Cboe Global Markets, Inc.", "Kellogg Company", "CenterPoint Energy, Inc (Holding Co)", "Trane Technologies plc", "MetLife, Inc.", "Southern Company (The)", "Waters Corporation", "Rockwell Automation, Inc.", "Mondelez International, Inc.", "Illinois Tool Works Inc.", "J.B. Hunt Transport Services, Inc.", "Nasdaq, Inc.", "Pool Corporation", "Laboratory Corporation of America Holdings", "Hormel Foods Corporation", "Dollar Tree, Inc.", "Honeywell International Inc.", "Jacobs Solutions Inc.", "Targa Resources, Inc.", "Marriott International", "CMS Energy Corporation", "RTX Corporation", "Juniper Networks, Inc.", "Henry Schein, Inc.", "Pentair plc.", "UnitedHealth Group Incorporated", "Dow Inc.", "Hewlett Packard Enterprise Company", "AmerisourceBergen Corporation", "Assurant, Inc.", "Tractor Supply Company", "Pinnacle West Capital Corporation", "C.H. Robinson Worldwide, Inc.", "Zebra Technologies Corporation", "Ball Corporation", "Regeneron Pharmaceuticals, Inc.", "Lowe’s Companies, Inc.", "Schlumberger N.V.", "ConAgra Brands, Inc.", "Carrier Global Corporation", "FleetCor Technologies, Inc.", "Charles River Laboratories International, Inc.", "ON Semiconductor Corporation", "Healthpeak Properties, Inc.", "DaVita Inc.", "Extra Space Storage Inc", "Federal Realty Investment Trust", "Sysco Corporation", "Union Pacific Corporation", "Keysight Technologies Inc.", "American Electric Power Company, Inc.", "Home Depot, Inc. (The)", "AvalonBay Communities, Inc.", "W.W. Grainger, Inc.", "Willis Towers Watson Public Limited Company", "WEC Energy Group, Inc.", "Atmos Energy Corporation", "Texas Instruments Incorporated", "Molina Healthcare Inc", "KLA Corporation", "Darden Restaurants, Inc.", "Johnson Controls International plc", "TE Connectivity Ltd. New Switzerland Registered Shares", "Lam Research Corporation", "Garmin Ltd.", "BlackRock, Inc.", "Dover Corporation", "Quest Diagnostics Incorporated", "AutoZone, Inc.", "Alliant Energy Corporation", "Eversource Energy (D/B/A)", "Norfolk Southern Corporation", "Expedia Group, Inc.", "Ameren Corporation", "Applied Materials, Inc.", "Exelon Corporation", "Leidos Holdings, Inc.", "NXP Semiconductors N.V.", "Xcel Energy Inc.", "Allegion plc", "General Dynamics Corporation", "Ulta Beauty, Inc.", "NiSource Inc", "Microchip Technology Incorporated", "Humana Inc.", "Philip Morris International Inc", "FMC Corporation", "Genuine Parts Company", "Target Corporation", "Pacific Gas & Electric Co.", "Dominion Energy, Inc.", "DBA Sempra", "Cisco Systems, Inc.", "Simon Property Group, Inc.", "Amgen Inc.", "Revvity, Inc.", "Gilead Sciences, Inc.", "eBay Inc.", "Expeditors International of Washington, Inc.", "Elevance Health, Inc.", "Textron Inc.", "Charles Schwab Corporation (The)", "The Travelers Companies, Inc.", "Evergy, Inc.", "Stanley Black & Decker, Inc.", "Caterpillar, Inc.", "FedEx Corporation", "Huntington Ingalls Industries, Inc.", "NextEra Energy, Inc.", "PayPal Holdings, Inc.", "Bristol-Myers Squibb Company", "Lockheed Martin Corporation", "DTE Energy Company", "Campbell Soup Company", "Franklin Resources, Inc.", "American Express Company", "General Mills, Inc.", "Caesars Entertainment, Inc.", "Skyworks Solutions, Inc.", "Cognizant Technology Solutions Corporation", "T. Rowe Price Group, Inc.", "Masco Corporation", "Williams Companies, Inc. (The)", "Kinder Morgan, Inc.", "McKesson Corporation", "Ameriprise Financial, Inc.", "CSX Corporation", "Packaging Corporation of America", "Dollar General Corporation", "Host Hotels", "LyondellBasell Industries NV", "Boston Properties, Inc.", "Morgan Stanley", "Snap-On Incorporated", "United Parcel Service, Inc.", "Robert Half Inc.", "Ralph Lauren Corporation", "Entergy Corporation", "Halliburton Company", "Fox Corporation", "QUALCOMM Incorporated", "Chubb Limited", "Eastman Chemical Company", "Northrop Grumman Corporation", "Biogen Inc.", "Charter Communications, Inc.", "LKQ Corporation", "Goldman Sachs Group, Inc. (The)", "VICI Properties Inc.", "Northern Trust Corporation", "United Rentals, Inc.", "Lamb Weston Holdings, Inc.", "Kroger Company (The)", "General Electric Company", "W.R. Berkley Corporation", "Amcor plc", "Fox Corporation", "Interpublic Group of Companies, Inc. (The)", "Universal Health Services, Inc.", "Raymond James Financial, Inc.", "Best Buy Co., Inc.", "HCA Healthcare, Inc.", "The Kraft Heinz Company", "Centene Corporation", "Globe Life Inc.", "Cummins Inc.", "Sealed Air Corporation", "NetApp, Inc.", "NVR, Inc.", "Consolidated Edison, Inc.", "The Bank of New York Mellon Corporation", "Arch Capital Group Ltd.", "The Cigna Group", "PACCAR Inc.", "Cincinnati Financial Corporation", "ONEOK, Inc.", "Public Storage", "Principal Financial Group Inc", "HP Inc.", "Omnicom Group Inc.", "Loews Corporation", "Deere & Company", "Ford Motor Company", "Everest Group, Ltd.", "Bath & Body Works, Inc.", "Hartford Financial Services Group, Inc. (The)", "ConocoPhillips", "Altria Group, Inc.", "Archer-Daniels-Midland Company", "Public Service Enterprise Group Incorporated", "Invesco Ltd", "Occidental Petroleum Corporation", "Wells Fargo & Company", "Advance Auto Parts Inc.", "U.S. Bancorp", "Chevron Corporation", "Pioneer Natural Resources Company", "Celanese Corporation", "AFLAC Incorporated", "BorgWarner Inc.", "American International Group, Inc. New", "Gen Digital Inc.", "Pfizer, Inc.", "JP Morgan Chase & Co.", "APA Corporation", "State Street Corporation", "Tapestry, Inc.", "Delta Air Lines, Inc.", "Berkshire Hathaway Inc. New", "EOG Resources, Inc.", "Exxon Mobil Corporation", "Bunge Limited Bunge Limited", "PNC Financial Services Group, Inc. (The)", "Bank of America Corporation", "D.R. Horton, Inc.", "Marathon Oil Corporation", "Regions Financial Corporation", "International Paper Company", "Capital One Financial Corporation", "Lennar Corporation", "DuPont de Nemours, Inc.", "Nucor Corporation", "Diamondback Energy, Inc.", "Organon & Co.", "M&T Bank Corporation", "Viatris Inc.", "Fifth Third Bancorp", "KeyCorp", "Huntington Bancshares Incorporated", "Coterra Energy Inc.", "Devon Energy Corporation", "Citigroup, Inc.", "Truist Financial Corporation", "Verizon Communications Inc.", "PulteGroup, Inc.", "CF Industries Holdings, Inc.", "Discover Financial Services", "Citizens Financial Group, Inc.", "Mosaic Company (The)", "Synchrony Financial", "Steel Dynamics, Inc.", "Zions Bancorporation N.A.", "United Airlines Holdings, Inc.", "Albemarle Corporation", "Marathon Petroleum Corporation", "Phillips 66", "Comerica Incorporated", "EQT Corporation", "General Motors Company", "Valero Energy Corporation", "American Airlines Group, Inc."]
sectors = ["Consumer Services", "Technology Services", "Consumer Non-Durables", "Finance", "Technology Services", "Health Technology", "Electronic Technology", "Finance", "Health Technology", "Health Technology", "Electronic Technology", "Consumer Non-Durables", "Electronic Technology", "Health Technology", "Retail Trade", "Technology Services", "Finance", "Health Technology", "Distribution Services", "Finance", "Health Technology", "Finance", "Distribution Services", "Consumer Services", "Technology Services", "Consumer Services", "Consumer Services", "Technology Services", "Health Technology", "Health Technology", "Consumer Services", "Technology Services", "Technology Services", "Consumer Non-Durables", "Technology Services", "Finance", "Technology Services", "Health Technology", "Technology Services", "Consumer Durables", "Consumer Non-Durables", "Health Technology", "Consumer Non-Durables", "Finance", "Technology Services", "Producer Manufacturing", "Commercial Services", "Industrial Services", "Electronic Technology", "Technology Services", "Consumer Non-Durables", "Technology Services", "Technology Services", "Health Technology", "Consumer Services", "Utilities", "Health Technology", "Health Technology", "Technology Services", "Technology Services", "Finance", "Producer Manufacturing", "Consumer Services", "Finance", "Electronic Technology", "Finance", "Technology Services", "Utilities", "Commercial Services", "Health Technology", "Utilities", "Electronic Technology", "Process Industries", "Electronic Technology", "Technology Services", "Finance", "Technology Services", "Consumer Non-Durables", "Finance", "Commercial Services", "Consumer Non-Durables", "Consumer Non-Durables", "Technology Services", "Consumer Services", "Commercial Services", "Retail Trade", "Health Technology", "Health Technology", "Process Industries", "Non-Energy Minerals", "Producer Manufacturing", "Producer Manufacturing", "Electronic Technology", "Health Technology", "Technology Services", "Technology Services", "Health Technology", "Finance", "Consumer Services", "Health Technology", "Transportation", "Finance", "Health Services", "Commercial Services", "Technology Services", "Health Technology", "Commercial Services", "Health Technology", "Health Technology", "Transportation", "Transportation", "Technology Services", "Finance", "Electronic Technology", "Health Technology", "Finance", "Technology Services", "Electronic Technology", "Technology Services", "Technology Services", "Electronic Technology", "Technology Services", "Finance", "Consumer Non-Durables", "Process Industries", "Technology Services", "Consumer Non-Durables", "Producer Manufacturing", "Consumer Services", "Electronic Technology", "Producer Manufacturing", "Finance", "Health Technology", "Consumer Non-Durables", "Finance", "Industrial Services", "Finance", "Technology Services", "Health Technology", "Commercial Services", "Technology Services", "Retail Trade", "Finance", "Process Industries", "Electronic Technology", "Energy Minerals", "Consumer Non-Durables", "Health Technology", "Technology Services", "Producer Manufacturing", "Health Technology", "Consumer Services", "Industrial Services", "Distribution Services", "Electronic Technology", "Retail Trade", "Producer Manufacturing", "Process Industries", "Finance", "Consumer Services", "Utilities", "Health Technology", "Producer Manufacturing", "Finance", "Finance", "Finance", "Finance", "Consumer Services", "Industrial Services", "Retail Trade", "Technology Services", "Producer Manufacturing", "Non-Energy Minerals", "Technology Services", "Finance", "Technology Services", "Utilities", "Health Technology", "Electronic Technology", "Finance", "Technology Services", "Health Technology", "Technology Services", "Communications", "Technology Services", "Technology Services", "Non-Energy Minerals", "Health Technology", "Technology Services", "Consumer Non-Durables", "Consumer Services", "Producer Manufacturing", "Retail Trade", "Electronic Technology", "Producer Manufacturing", "Consumer Services", "Retail Trade", "Utilities", "Consumer Services", "Consumer Non-Durables", "Process Industries", "Finance", "Technology Services", "Finance", "Consumer Non-Durables", "Retail Trade", "Consumer Non-Durables", "Electronic Technology", "Process Industries", "Electronic Technology", "Finance", "Producer Manufacturing", "Finance", "Consumer Non-Durables", "Utilities", "Producer Manufacturing", "Finance", "Utilities", "Health Technology", "Electronic Technology", "Consumer Non-Durables", "Producer Manufacturing", "Transportation", "Finance", "Distribution Services", "Health Services", "Consumer Non-Durables", "Retail Trade", "Electronic Technology", "Technology Services", "Utilities", "Consumer Services", "Utilities", "Electronic Technology", "Technology Services", "Distribution Services", "Producer Manufacturing", "Health Services", "Process Industries", "Electronic Technology", "Distribution Services", "Finance", "Retail Trade", "Utilities", "Transportation", "Electronic Technology", "Process Industries", "Health Technology", "Retail Trade", "Industrial Services", "Consumer Non-Durables", "Producer Manufacturing", "Commercial Services", "Commercial Services", "Electronic Technology", "Finance", "Health Services", "Finance", "Finance", "Transportation", "Transportation", "Electronic Technology", "Utilities", "Retail Trade", "Finance", "Distribution Services", "Finance", "Utilities", "Utilities", "Electronic Technology", "Health Services", "Electronic Technology", "Consumer Services", "Producer Manufacturing", "Electronic Technology", "Producer Manufacturing", "Electronic Technology", "Finance", "Producer Manufacturing", "Health Services", "Retail Trade", "Utilities", "Utilities", "Transportation", "Consumer Services", "Utilities", "Producer Manufacturing", "Utilities", "Electronic Technology", "Electronic Technology", "Utilities", "Producer Manufacturing", "Electronic Technology", "Retail Trade", "Utilities", "Electronic Technology", "Health Services", "Consumer Non-Durables", "Process Industries", "Distribution Services", "Retail Trade", "Utilities", "Utilities", "Utilities", "Technology Services", "Finance", "Health Technology", "Health Technology", "Health Technology", "Retail Trade", "Transportation", "Health Services", "Electronic Technology", "Finance", "Finance", "Utilities", "Consumer Durables", "Producer Manufacturing", "Transportation", "Electronic Technology", "Utilities", "Commercial Services", "Health Technology", "Electronic Technology", "Utilities", "Consumer Non-Durables", "Finance", "Finance", "Consumer Non-Durables", "Consumer Services", "Electronic Technology", "Technology Services", "Finance", "Producer Manufacturing", "Industrial Services", "Industrial Services", "Distribution Services", "Finance", "Transportation", "Process Industries", "Retail Trade", "Finance", "Process Industries", "Finance", "Finance", "Consumer Durables", "Transportation", "Commercial Services", "Consumer Non-Durables", "Utilities", "Industrial Services", "Consumer Services", "Electronic Technology", "Finance", "Process Industries", "Electronic Technology", "Health Technology", "Consumer Services", "Consumer Durables", "Finance", "Finance", "Finance", "Finance", "Consumer Non-Durables", "Retail Trade", "Producer Manufacturing", "Finance", "Process Industries", "Consumer Services", "Commercial Services", "Health Services", "Finance", "Retail Trade", "Health Services", "Consumer Non-Durables", "Health Services", "Finance", "Producer Manufacturing", "Process Industries", "Electronic Technology", "Consumer Durables", "Utilities", "Finance", "Finance", "Health Services", "Producer Manufacturing", "Finance", "Industrial Services", "Finance", "Finance", "Electronic Technology", "Commercial Services", "Finance", "Producer Manufacturing", "Consumer Durables", "Finance", "Retail Trade", "Finance", "Energy Minerals", "Consumer Non-Durables", "Process Industries", "Utilities", "Finance", "Energy Minerals", "Finance", "Retail Trade", "Finance", "Energy Minerals", "Energy Minerals", "Process Industries", "Finance", "Producer Manufacturing", "Finance", "Technology Services", "Health Technology", "Finance", "Energy Minerals", "Finance", "Retail Trade", "Transportation", "Finance", "Energy Minerals", "Energy Minerals", "Process Industries", "Finance", "Finance", "Consumer Durables", "Energy Minerals", "Finance", "Process Industries", "Finance", "Consumer Durables", "Process Industries", "Non-Energy Minerals", "Energy Minerals", "Health Technology", "Finance", "Health Technology", "Finance", "Finance", "Finance", "Energy Minerals", "Energy Minerals", "Finance", "Finance", "Communications", "Consumer Durables", "Process Industries", "Finance", "Finance", "Process Industries", "Finance", "Non-Energy Minerals", "Finance", "Transportation", "Process Industries", "Energy Minerals", "Energy Minerals", "Finance", "Energy Minerals", "Consumer Durables", "Energy Minerals", "Transportation"]

data = []

for company, sector in zip(companies, sectors):
    earnings = np.random.uniform(20, 60, size=52)
    market_cap = np.random.uniform(1000, 2500, size=52)

    for week, earning, m_cap in zip(weeks, earnings, market_cap):
        data.append([company, sector, week, earning, m_cap])

original_df = pd.DataFrame(data, columns=['Company', 'Sector', 'Week', 'Earnings', 'Market_Cap'])
original_df['PE_Ratio'] = (original_df['Market_Cap'] / original_df['Earnings']).round(1)

global df
df = original_df.copy()


# Sort the sectors
sorted_sectors = sorted(df['Sector'].unique())

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': s, 'value': s} for s in sorted_sectors],
        value=['Utilities'],
        multi=True
    ),
    
    dcc.Graph(id='graph'),
    
    html.Button('Remove Selected Rows', id='remove-button'),
    
    html.Button('Reset', id='reset-button'),
    
    html.Button("Download Data", id="btn_csv"),
    
    dcc.Download(id="download"),        
    
    dash_table.DataTable(
        id='table',
        style_table={'overflowX': 'scroll'},
        page_size=10,
        row_selectable='multi',
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        
    ),
    

    
#     dcc.Dropdown(
#         id='company-dropdown',
#         style={
#             'height': '2px', 
#             'width': '100px', 
#             'font-size': "50%",
#             'min-height': '1px',
#             },
#         options=[{'label': c, 'value': c} for c in companies],
#         value=companies,
#         multi=True
#     ),    
    
])

@app.callback(
    [Output('graph', 'figure'),
     Output('table', 'data'),
     Output('table', 'columns')],
    [Input('sector-dropdown', 'value'),
     Input('remove-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('table', 'selected_rows'),
     State('table', 'data')]
    
)

def update(selected_sectors, n_remove_clicks, n_reset_clicks, selected_rows, table_data):
    
    global filtered_df
    filtered_df = original_df.copy()

    ctx = dash.callback_context
    
    if not selected_sectors:
        selected_sectors = sorted_sectors

    if not ctx.triggered:
        filtered_df = original_df.copy()
        
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        #filtered_df = df[df['Company'].isin(selected_companies) & df['Sector'].isin(selected_sectors)]
        filtered_df = df[df['Sector'].isin(selected_sectors)]

        if button_id == 'remove-button':
            if selected_rows is not None:
                for i in sorted(selected_rows, reverse=True):
                    del table_data[i]
                # Convert back to DataFrame after removing rows
                filtered_df = pd.DataFrame(table_data)
                if 'Sector' in filtered_df.columns:
                    filtered_df = filtered_df.melt(id_vars=['Sector', 'Company'], var_name='Week', value_name='PE_Ratio')
                else:
                    return dash.no_update, dash.no_update, dash.no_update
        elif button_id == 'reset-button':
            filtered_df = original_df.copy()


    filtered_df = df[df['Sector'].isin(selected_sectors)]

    quintile_labels = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    filtered_df['Quintile'] = filtered_df.groupby('Week')['Market_Cap'].transform(lambda x: pd.qcut(x, 5, labels=quintile_labels))
    
    global quintile_df    
    quintile_df = filtered_df.groupby(['Quintile', 'Week']).apply(lambda x: sum(x['Market_Cap']) / sum(x['Earnings'])).round(1)
    quintile_df = quintile_df.reset_index()
    quintile_df.columns = ['Quintile', 'Week', 'PE_Ratio']
    quintile_df['PE_Ratio'] = quintile_df['PE_Ratio'].round(1)
    
    # Plot
    #fig = px.line(filtered_df, x='Week', y='PE_Ratio', color='Company', line_dash='Sector', title="PE Ratio by Quintile Over Time")
    fig = px.line(quintile_df, x='Week', y='PE_Ratio', color='Quintile', title="PE Ratio by Quintile Over Time")

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
    app.run_server(host='0.0.0.0', port='22222')
