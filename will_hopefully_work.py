import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash import dash_table

df = pd.read_csv(r'D:\Projects\Dashboard\clean.csv')

# Aggregate CO2 emissions by continent and year
df_grouped = df.groupby(['continent', 'year'], as_index=False)['co2'].sum()

# Create the line chart for CO2 emissions per continent
fig_co2_line = px.line(df_grouped, 
                       x='year', 
                       y='co2', 
                       color='continent', 
                       title='CO₂ Emissions Per Continent Over Time')

df_sources = df[['cement_co2', 'coal_co2', 'flaring_co2', 'gas_co2', 
    'oil_co2', 'other_industry_co2']].sum()

fig_co2_sources_pie = px.pie(
    df_sources, 
    names=df_sources.index,  # The source names will be the index of the series
    values=df_sources.values, 
    title="CO₂ Emissions by Source (Total for All Years)",
    color=df_sources.index,  # Assign different colors for each source
)

df_sorted_bar = df.sort_values(by='co2_per_capita', ascending=False)

# Create the bar chart for CO2 per capita by country
fig_co2_per_capita = px.bar(df_sorted_bar, 
                            x='continent',  # Replace with the actual column name for countries
                            y='co2_per_capita', 
                            title='CO₂ Emissions Per Capita by Country', 
                            labels={'co2_per_capita': 'CO₂ Emissions Per Capita'},
                            height=400)

# Ensure bars are fully opaque and non-transparent
fig_co2_per_capita.update_traces(
    marker_color='#1f77b4',   # Solid color
    opacity=1,                # Fully opaque bars
    marker_line_width=0,      # Ensure no border around bars that could cause transparency
    marker_line_color='black' # Optional: Add a black border if desired
)

fig_co2_per_capita.update_layout(bargap=0.1)  # Optional: Controls the gap between bars

# Optional: Sorting x-axis labels based on descending CO₂ emissions per capita
fig_co2_per_capita.update_xaxes(categoryorder='total descending')

# Calculate average CO2 emissions per continent for all years
df_avg_co2 = df.groupby('continent', as_index=False)['co2'].mean()

# Sort the DataFrame by average CO2 emissions in descending order
df_avg_co2 = df_avg_co2.sort_values(by='co2', ascending=False)

# Create the table for average CO2 emissions per continent (across all years)
table = dash_table.DataTable(
    id='average_co2_table',
    columns=[
        {'name': 'Continent', 'id': 'continent'},
        {'name': 'Average CO₂ Emissions per year', 'id': 'co2'}
    ],
    data=df_avg_co2.to_dict('records'),
    style_table={'height': '400px', 'overflowY': 'auto'},
    style_cell={'textAlign': 'center', 'padding': '8px', 'fontSize': '14px', 'fontFamily': 'Arial'},
    style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', 'color': 'black'},
    style_data_conditional=[
        {
            'if': {'column_id': 'co2', 'filter_query': '{co2} > 0'},
            'backgroundColor': 'rgb(255, 255, 255)',  # white for the background
            'color': 'black',
        },
        {
            'if': {'column_id': 'co2', 'filter_query': '{co2} <= 0'},
            'backgroundColor': 'rgb(255, 204, 204)',  # light red for values <= 0
            'color': 'black',
        },
    ],
    sort_action='native',  # Enable sorting functionality by column
    sort_by=[{'column_id': 'co2', 'direction': 'desc'}]  # Sort by CO₂ emissions in descending order
)

app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("CO₂ Emissions Dashboard", style={'text-align': 'center'}),

    # Create a container for the first row (line chart and table)
    html.Div([
        # First section: CO₂ Emissions per Continent (Line Chart)
        html.Div([
            dcc.Graph(id='co2_line_chart', figure=fig_co2_line)
        ], style={'width': '70%', 'padding': '20px', 'display': 'inline-block'}),  # Half width for line chart

        # Second section: Table for Average CO₂ Emissions per Continent
        html.Div([
            table
        ], style={'width': '30%', 'padding': '20px', 'display': 'inline-block', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),  # Center the table vertically

    ], style={'display': 'flex', 'justifyContent': 'space-between'}),  # Align charts and table horizontally

    # Create a container for the second row (pie chart and bar chart)
    html.Div([
        # Second section: CO₂ Sources (Pie Chart)
        html.Div([
            dcc.Graph(id='co2_sources_pie', figure=fig_co2_sources_pie)
        ], style={'width': '50%', 'padding': '20px', 'display': 'inline-block'}),  # Half width for pie chart

        # Third section: CO₂ Emissions per Capita by Country (Bar Chart)
        html.Div([
            dcc.Graph(id='co2_per_capita_bar', figure=fig_co2_per_capita)
        ], style={'width': '50%', 'padding': '20px', 'display': 'inline-block'}),  # Half width for bar chart

    ], style={'display': 'flex', 'justifyContent': 'space-between'}),  # Align pie chart and bar chart horizontally

])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
