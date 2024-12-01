#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


#hello


# In[ ]:





# In[1]:

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# List of continent names (case-insensitive matching)
continents = ['Africa', 'Asia', 'Europe', 'Oceania', 'North America', 'South America']

# Function to extract continent names directly from the 'country' column
def get_continent(country):
    country = str(country).lower()  # Make sure the string is lowercase for case-insensitive matching
    for continent in continents:
        if continent.lower() in country:  # Check if the continent name is in the country string
            return continent
    return 'Unknown'  # If no continent is found

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/refs/heads/master/owid-co2-data.csv")

# Apply the get_continent function to the 'country' column to extract continents
df['continent'] = df['country'].apply(get_continent)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("CO2 Emissions Dashboard"),

    # Slider for selecting year
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        step=1,
        marks={year: str(year) for year in range(df['year'].min(), df['year'].max() + 1, 5)},  # Show marks every 5 years
        value=df['year'].min(),  # Default value
        tooltip={"placement": "bottom", "always_visible": True},
    ),

    # CO2 Emissions Over Time by Continent
    dcc.Graph(id='co2-continent-plot'),

    # CO2 vs GDP Scatterplot
    dcc.Graph(id='co2-gdp-plot'),

    # CO2 Sources by Continent Bar Chart
    dcc.Graph(id='co2-sources-plot'),
])

# Callback to update graphs based on selected year
@app.callback(
    [Output('co2-continent-plot', 'figure'),
     Output('co2-gdp-plot', 'figure'),
     Output('co2-sources-plot', 'figure')],
    [Input('year-slider', 'value')]
)
def update_plots(selected_year):
    # Filter data by the selected year
    filtered_df = df[df['year'] == selected_year]

    # 1. CO2 Emissions Over Time by Continent (Line plot with one line per continent)
    co2_continent_plot = px.line(filtered_df, x='year', y='co2', color='continent', 
                                 title="CO2 Emission Over Time by Continent")

    # 2. CO2 vs GDP Scatterplot
    co2_gdp_plot = px.scatter(filtered_df, x='gdp', y='co2', color='continent', 
                               title="CO2 vs GDP Scatterplot")

    # 3. Bar Chart with CO2 Sources by Continent
    co2_sources_plot = px.bar(filtered_df, x='continent', y='cement_co2', 
                               title="CO2 Sources by Continent")

    return co2_continent_plot, co2_gdp_plot, co2_sources_plot

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
