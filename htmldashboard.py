import pandas as pd
import plotly.express as px
import plotly.io as pio

# Load your dataset
df = pd.read_csv(r'D:\Projects\Dashboard\clean.csv')

# Aggregate CO2 emissions by continent and year
df_grouped = df.groupby(['continent', 'year'], as_index=False)['co2'].sum()

# Create the line chart for CO2 emissions per continent
fig_co2_line = px.line(
    df_grouped, 
    x='year', 
    y='co2', 
    color='continent', 
    title='CO₂ Emissions Per Continent Over Time'
)

# Calculate total CO₂ emissions by source
df_sources = df[['cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 'oil_co2', 'other_industry_co2']].sum()

# Create the pie chart for CO₂ emissions by source
fig_co2_sources_pie = px.pie(
    values=df_sources.values,
    names=df_sources.index,
    title="CO₂ Emissions by Source (Total for All Years)",
    color=df_sources.index,
)

# Sort data by CO2 per capita in descending order
df_sorted_bar = df.sort_values(by='co2_per_capita', ascending=False)

# Create the bar chart for CO2 emissions per capita by country
fig_co2_per_capita = px.bar(
    df_sorted_bar, 
    x='continent',  # Replace with the actual column name for countries
    y='co2_per_capita', 
    title='CO₂ Emissions Per Capita by Country', 
    labels={'co2_per_capita': 'CO₂ Emissions Per Capita'},
    height=400
)

# Customize the bar chart appearance
fig_co2_per_capita.update_traces(
    marker_color='#1f77b4',   # Solid color
    opacity=1,                # Fully opaque bars
    marker_line_width=0,      # No border
)

fig_co2_per_capita.update_layout(bargap=0.1)
fig_co2_per_capita.update_xaxes(categoryorder='total descending')

# Export each figure as an HTML file
pio.write_html(fig_co2_line, 'fig_co2_line.html')
pio.write_html(fig_co2_sources_pie, 'fig_co2_sources_pie.html')
pio.write_html(fig_co2_per_capita, 'fig_co2_per_capita.html')
