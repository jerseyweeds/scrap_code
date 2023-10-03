#https://chat.openai.com/c/20fde9ec-d33a-4915-9754-8cc3beacf9f6

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import base64

# Sample data generation
np.random.seed(42)
companies = ["Apple", "Google", "Microsoft", "Amazon", "Facebook", "Tesla", "Netflix", "Disney", "Zoom", "Slack"]
sectors = ["Tech", "Entertainment", "Tech", "Retail", "Tech", "Automotive", "Entertainment", "Entertainment", "Tech", "Tech"]

dates = pd.date_range("2022-01-01", periods=52, freq="W")
df = pd.DataFrame({
    "Date": np.tile(dates, len(companies)),
    "Company": np.repeat(companies, len(dates)),
    "Sector": np.repeat(sectors, len(dates)),
    "Earnings": np.random.rand(len(dates) * len(companies)) * 1e9,
    "MarketCap": np.random.rand(len(dates) * len(companies)) * 1e11,
    "EnterpriseValue": np.random.rand(len(dates) * len(companies)) * 1e11,
    "FreeCashFlow": np.random.rand(len(dates) * len(companies)) * 1e9,
})

# Create a master dictionary to store distinct companies grouped by sector
companies_by_sector = {sector: sorted(df[df['Sector'] == sector]['Company'].unique()) for sector in df['Sector'].unique()}

# Define columns to include in selector list
included_columns = ['MarketCap', 'EnterpriseValue', 'Earnings', 'FreeCashFlow']

# Streamlit app
st.title('S&P 500 Sector Analysis')
st.sidebar.title('Select Numerator and Denominator')

# Create filtered lists of options for numerator and denominator
numerator_options = included_columns
denominator_options = included_columns

# Set default values for numerator and denominator
default_numerator = 'MarketCap'
default_denominator = 'Earnings'

# Numerator and denominator selection via dropdown with default values
numerator = st.sidebar.selectbox('Select Numerator', numerator_options, index=numerator_options.index(default_numerator))
denominator = st.sidebar.selectbox('Select Denominator', denominator_options, index=denominator_options.index(default_denominator))

st.sidebar.title('Sector Selection')

# Sector selection via checkboxes
select_all_sectors = st.sidebar.checkbox('Select All Sectors', True)
if select_all_sectors:
    selected_sectors = list(companies_by_sector.keys())  # Use the master dictionary
else:
    selected_sectors = st.sidebar.multiselect('Select Sectors', list(companies_by_sector.keys()), default=list(companies_by_sector.keys()))

# Create a nested company selection panel
st.sidebar.title('Company Selection')

company_checkboxes = {}
excluded_companies = set()
selected_companies = []
for sector in selected_sectors:
    sector_companies = companies_by_sector[sector]
    sector_expander = st.sidebar.expander(sector, expanded=False)
    with sector_expander:
        select_all_in_sector = st.checkbox('Select All', True, key=f'SelectAll_{sector}')
        if select_all_in_sector:
            company_checkboxes[sector] = {company: True for company in sector_companies}
        else:
            company_checkboxes[sector] = {}
        for company in sector_companies:
            if select_all_in_sector:
                company_checkboxes[sector][company] = st.checkbox(company, True, key=f'{sector}_{company}')
            else:
                company_checkboxes[sector][company] = st.checkbox(company, False, key=f'{sector}_{company}')
            if not company_checkboxes[sector][company]:
                excluded_companies.add(company)
            else:
                selected_companies.append(company)

# Number of quantiles input
num_qcuts = st.sidebar.number_input('Number of Quantiles:', min_value=1, value=5)

# Add an "Update Charts" button
update_charts_button = st.sidebar.button('Update Charts')

# Boolean flag to control chart generation
generate_charts = False

# Check if the "Update Charts" button is pressed
if update_charts_button:
    generate_charts = True

# Chart generation based on the boolean flag
if generate_charts:
    # Calculate the data for the main chart
    filtered_df = df[(df['Sector'].isin(selected_sectors)) & (~df['Company'].isin(excluded_companies))]
    filtered_df['Ratio'] = filtered_df[numerator] / filtered_df[denominator]

    main_chart = alt.Chart(filtered_df).mark_line().encode(
        x='Date:T',
        y=alt.Y('mean(Ratio):Q', title='Ratio'),
        color='Sector:N'
    ).properties(
        width=800,
        height=400
    ).configure_axis(
        labelAngle=0
    )

    st.altair_chart(main_chart, use_container_width=True)

    # Calculate the data for the quantile chart
    quantile_chart_data = filtered_df.copy()
    quantile_chart_data['Quantile'] = pd.qcut(quantile_chart_data['MarketCap'], q=num_qcuts, labels=False)
    quantile_chart_data = quantile_chart_data.groupby(['Date', 'Quantile']).agg({
        numerator: 'sum',
        denominator: 'sum'
    }).reset_index()
    quantile_chart_data['Ratio'] = quantile_chart_data[numerator] / quantile_chart_data[denominator]

    quantile_chart = alt.Chart(quantile_chart_data).mark_line().encode(
        x='Date:T',
        y=alt.Y('mean(Ratio):Q', title='Ratio'),
        color='Quantile:N'
    ).properties(
        width=800,
        height=400
    )

    st.altair_chart(quantile_chart, use_container_width=True)

# Optional: Display data table
show_table = st.button('Show Company Data')
if show_table:
    st.write(filtered_df)

# Optional: Download buttons for dataframes
if not filtered_df.empty:
    csv_data = filtered_df.to_csv(index=False, encoding='utf-8')
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download Filtered Data</a>'
    st.markdown(href, unsafe_allow_html=True)

if not quantile_chart_data.empty:
    csv_quantile_data = quantile_chart_data.to_csv(index=False, encoding='utf-8')
    b64_quantile = base64.b64encode(csv_quantile_data.encode()).decode()
    href_quantile = f'<a href="data:file/csv;base64,{b64_quantile}" download="quantile_chart_data.csv">Download Quantile Chart Data</a>'
    st.markdown(href_quantile, unsafe_allow_html=True)
