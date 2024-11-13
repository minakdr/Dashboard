import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv(r'D:\Projects\Dashboard\clean.csv')

# Aggregate CO2 emissions by continent and year
df_grouped = df.groupby(['continent', 'year'], as_index=False)['co2'].sum()

# Create the line chart for CO2 emissions per continent
fig_co2_line = px.line(df_grouped, 
                       x='year', 
                       y='co2', 
                       color='continent', 
                       title='CO₂ Emissions Per Continent Over Time')
fig_co2_line_html = fig_co2_line.to_html(full_html=False, include_plotlyjs='cdn')

# Create the pie chart for CO2 emissions by source
df_sources = df[['cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 'oil_co2', 'other_industry_co2']].sum()
fig_co2_sources_pie = px.pie(
    df_sources, 
    names=df_sources.index, 
    values=df_sources.values, 
    title="CO₂ Emissions by Source (Total for All Years)"
)
fig_co2_sources_pie_html = fig_co2_sources_pie.to_html(full_html=False, include_plotlyjs=False)

# Sort and create the bar chart for CO2 emissions per capita
df_sorted_bar = df.sort_values(by='co2_per_capita', ascending=False)
fig_co2_per_capita = px.bar(df_sorted_bar, 
                            x='continent',  
                            y='co2_per_capita', 
                            title='CO₂ Emissions Per Capita by Country', 
                            labels={'co2_per_capita': 'CO₂ Emissions Per Capita'},
                            height=400)
fig_co2_per_capita.update_traces(
    marker_color='#1f77b4',
    opacity=1,
    marker_line_width=0
)
fig_co2_per_capita.update_layout(bargap=0.1)
fig_co2_per_capita.update_xaxes(categoryorder='total descending')
fig_co2_per_capita_html = fig_co2_per_capita.to_html(full_html=False, include_plotlyjs=False)

# Calculate average CO2 emissions per continent
df_avg_co2 = df.groupby('continent', as_index=False)['co2'].mean()
df_avg_co2 = df_avg_co2.sort_values(by='co2', ascending=False)

# Generate HTML table for average CO2 emissions
table_html = df_avg_co2.to_html(index=False, classes='dataframe', border=0)

# Combine everything into a single HTML file
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CO₂ Emissions Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
        }}
        .container {{
            display: flex;
            justify-content: space-between;
            padding: 20px;
        }}
        .chart-container {{
            width: 48%;
        }}
        .table-container {{
            margin: 20px auto;
            width: 70%;
        }}
        .dataframe {{
            width: 100%;
            border-collapse: collapse;
        }}
        .dataframe th, .dataframe td {{
            padding: 8px;
            border: 1px solid #ddd;
        }}
        .dataframe th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>

    <h1>CO₂ Emissions Dashboard</h1>

    <div class="container">
        <div class="chart-container">
            <h2>CO₂ Emissions Per Continent Over Time</h2>
            {fig_co2_line_html}
        </div>
        <div class="table-container">
            <h2>Average CO₂ Emissions per Continent (All Years)</h2>
            {table_html}
        </div>
    </div>

    <div class="container">
        <div class="chart-container">
            <h2>CO₂ Emissions by Source (Total for All Years)</h2>
            {fig_co2_sources_pie_html}
        </div>
        <div class="chart-container">
            <h2>CO₂ Emissions Per Capita by Country</h2>
            {fig_co2_per_capita_html}
        </div>
    </div>

</body>
</html>
"""

# Save the combined HTML content to a file
with open("output.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Static HTML dashboard has been generated as 'output.html'")
