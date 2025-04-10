# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options=[{'label': 'Alle Startplätze', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, {'label': 'KSC LC-39A','value': 'KSC LC-39A'}, {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                                value='ALL', placeholder='Wählen Sie einen Startplatz aus', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                    min=0,
                                                    max=10000,
                                                    step=1000,
                                                    marks={0: '0',
                                                        1000: '1000 kg',
                                                        2000: '2000 kg',
                                                        3000: '3000 kg',
                                                        4000: '4000 kg',
                                                        5000: '5000 kg',
                                                        6000: '6000 kg',
                                                        7000: '7000 kg',
                                                        8000: '8000 kg',
                                                        9000: '9000 kg',
                                                        10000: '10000 kg',
                                                    },
                                                    value=[min_payload, max_payload]),
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def update_piegraph(site_dropdown):
    if site_dropdown == 'ALL':
        data  = spacex_df[spacex_df['class'] == 1] 
        fig = px.pie(
                data,
                names = 'Launch Site',
                title = 'Total Success Launches by All Sites',
            )
    else:
        data  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
                data,
                names = 'class',
                title = 'Total Success Launches for Site &#8608; '+site_dropdown,
            )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='payload-slider',component_property='value')])

def update_scatterplot(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        low, high = payload_slider
        data = spacex_df
        inrange = (data['Payload Mass (kg)'] > low) & (data['Payload Mass (kg)'] < high)
        fig = px.scatter(
            data[inrange],
            x='Payload Mass (kg)',
            y= 'class',
            color='Booster Version Category'
        )
    else:
        low, high = payload_slider
        data  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        inrange = (data['Payload Mass (kg)'] > low) & (data['Payload Mass (kg)'] < high)
        fig = px.scatter(
            data[inrange],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
