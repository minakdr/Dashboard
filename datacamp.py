import pandas as pd
import plotly.express as px
ecom_sales = pd.read_csv('/usr/local/share/datasets/ecom_sales.csv')
ecom_sales = ecom_sales.groupby(['Year-Month','Country'])['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')

# Create the line graph
line_graph = px.line(
  # Set the appropriate DataFrame and title
  data_frame=ecom_sales, title='Total Sales by Country and Month' , 
  # Set the x and y arguments
  x='Year-Month', y='Total Sales ($)',
  # Ensure a separate line per country
  color='Country')

line_graph.show()


# Create the bar graph object
bar_fig = px.bar(
  # Set the DataFrame, x and y
  data_frame=ecom_sales, x='Total Sales ($)', y='Country',
  # Set the graph to be horizontal
  orientation ='h', title='Total Sales by Country')

# Increase the gap between bars
bar_fig.update_layout(bargap=0.5) 

bar_fig.show()