from flask import Flask, render_template
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from pyspark.sql import SparkSession
import pandas as pd
import time
import mysql.connector
from pyspark.sql import functions as F

# Initialize Flask app
server = Flask(__name__)

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("StarMeter") \
    .config("spark.jars", "jars/mysql-connector-java-8.4.0.jar") \
    .getOrCreate()

def get_fan_counts():
    try:
        df = spark.read.format("jdbc") \
            .option("url", "jdbc:mysql://127.0.0.1:3306/starmeter_sim") \
            .option("dbtable", "user_dynamic_preferences") \
            .option("user", "root") \
            .option("password", "zipcode123") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .load()

        fan_counts_df = df.groupBy("current_favorite").count().withColumnRenamed("count", "fan_count")
        fan_counts_pd = fan_counts_df.toPandas()
        return fan_counts_pd

    except Exception as e:
        print(f"Error retrieving data: {e}")
        return pd.DataFrame(columns=['current_favorite', 'fan_count'])

def fetch_and_calculate_changes():
    try:
        df = spark.read.format("jdbc") \
            .option("url", "jdbc:mysql://localhost:3306/starmeter_sim") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", "event_log") \
            .option("user", "root") \
            .option("password", "zipcode123") \
            .load()

        pdf = df.select("event_date", "celebrity", "event_description", "current_fan_count") \
            .orderBy(F.desc("event_date")) \
            .limit(10) \
            .toPandas()

        pdf['fan_count_change'] = pdf['current_fan_count'].diff().fillna(0).astype(int)
        event_log_html = html.Div([
            html.H4("Event Log", style={'fontSize': '20px', 'marginBottom': '10px'}),
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Date", style={'fontSize': '12px', 'fontWeight': 'bold', 'padding': '5px'}),
                    html.Th("Celebrity", style={'fontSize': '12px', 'fontWeight': 'bold', 'padding': '5px'}),
                    html.Th("Event", style={'fontSize': '12px', 'fontWeight': 'bold', 'padding': '5px'}),
                    html.Th("Change", style={'fontSize': '12px', 'fontWeight': 'bold', 'padding': '5px'})
                ])),
                html.Tbody([
                    html.Tr([
                        html.Td(row['event_date'].strftime('%Y-%m-%d'), style={'fontSize': '12px', 'padding': '5px'}),
                        html.Td(row['celebrity'], style={'fontSize': '12px', 'padding': '5px'}),
                        html.Td(row['event_description'], style={'fontSize': '12px', 'padding': '5px'}),
                        html.Td(f"{row['fan_count_change']:+d}", style={'fontSize': '12px', 'padding': '5px', 'color': 'green' if row['fan_count_change'] > 0 else 'red' if row['fan_count_change'] < 0 else 'black'})
                    ]) for _, row in pdf.iterrows()
                ])
            ], style={'width': '100%', 'textAlign': 'left', 'borderCollapse': 'collapse'})
        ])
        return event_log_html
    except Exception as e:
        print(f"Error calculating changes: {e}")
        return html.Div(["Error fetching event log"])

# Initialize Dash app
dash_app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define custom styles for KPI cards
card_styles = [
    {"backgroundColor": "#0075A4", "color": "white", "padding": "0px", "borderRadius": "10px", "width": "200px", "height": "60px", "lineHeight": "1"},
    {"backgroundColor": "#008FAD", "color": "white", "padding": "0px", "borderRadius": "10px", "width": "200px", "height": "60px", "lineHeight": "1"},
    {"backgroundColor": "#00A697", "color": "white", "padding": "0px", "borderRadius": "10px", "width": "200px", "height": "60px", "lineHeight": "1"},
    {"backgroundColor": "#1EB769", "color": "white", "padding": "0px", "borderRadius": "10px", "width": "200px", "height": "60px", "lineHeight": "1"}
]

# Initialize layout with KPI cards next to each other and graph with legend on top
dash_app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.Button('Start', id='start-stop-button', n_clicks=0, className="btn btn-primary"), width="auto"),
        dbc.Col(html.H1("StarMeter", style={"fontSize": "24px"}), width=True)
    ], align='center', className="mb-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Fans (in thousands)", className="card-title", style={"fontSize": "12px", "margin": "0"}),
                html.H5(id='total-fans', className="card-text", style={"fontSize": "16px", "margin": "0"})
            ])
        ], style=card_styles[0], className="mb-2"), width=2),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Most Popular Celebrity", className="card-title", style={"fontSize": "12px", "margin": "0"}),
                html.H5(id='most-popular-celebrity', className="card-text", style={"fontSize": "16px", "margin": "0"})
            ])
        ], style=card_styles[1], className="mb-2"), width=2),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Average Fans", className="card-title", style={"fontSize": "12px", "margin": "0"}),
                html.H5(id='average-fans', className="card-text", style={"fontSize": "16px", "margin": "0"})
            ])
        ], style=card_styles[2], className="mb-2"), width=2),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Events", className="card-title", style={"fontSize": "12px", "margin": "0"}),
                html.H5(id='total-events', className="card-text", style={"fontSize": "16px", "margin": "0"})
            ])
        ], style=card_styles[3], className="mb-2"), width=2),
    ], className="g-1"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='live-update-graph'), width=8),
        dbc.Col(html.Div(id='event-log', children="Event log will be displayed here.", style={"height": "400px", "overflowY": "auto", "border": "1px solid #ddd", "padding": "10px"}), width=4)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart'), width=12)
    ]),
    
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update every 1 second
        n_intervals=0,
        disabled=True
    )
])

@dash_app.callback(
    [Output('live-update-graph', 'figure'),
     Output('bar-chart', 'figure'),
     Output('total-fans', 'children'),
     Output('most-popular-celebrity', 'children'),
     Output('average-fans', 'children'),
     Output('total-events', 'children'),
     Output('event-log', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_graph_and_kpis(n):
    print(f"Callback triggered, n_intervals: {n}")  # Debug statement
    try:
        fan_counts_df = get_fan_counts()
        event_log_html = fetch_and_calculate_changes()
        
        fan_counts_data = {}
        time_data = []
        for celebrity in fan_counts_df['current_favorite'].unique():
            fan_counts_data[celebrity] = []
        
        total_fans = 0
        most_popular_celeb = None
        max_fans = 0
        total_events = 0
        current_fan_counts = []
        colors = ['#0075A4', '#008FAD', '#00A697', '#1EB769']

        if not fan_counts_df.empty:
            current_time = time.time()
            time_data.append(current_time - time_data[0] if time_data else 0)

            for idx, celebrity in enumerate(fan_counts_data.keys()):
                fan_count = fan_counts_df[fan_counts_df['current_favorite'] == celebrity]['fan_count'].sum() if not fan_counts_df[fan_counts_df['current_favorite'] == celebrity].empty else 0
                fan_counts_data[celebrity].append(fan_count)
                current_fan_counts.append(fan_count)
                total_events += len(fan_counts_data[celebrity])

                total_fans += fan_count
                if fan_count > max_fans:
                    max_fans = fan_count
                    most_popular_celeb = celebrity

            line_fig = go.Figure()
            for idx, (celebrity, fan_counts) in enumerate(fan_counts_data.items()):
                line_fig.add_trace(go.Scatter(
                    x=time_data,
                    y=fan_counts,
                    mode='lines+markers',
                    name=celebrity,
                    marker=dict(size=5, color=colors[idx]),
                    line=dict(color=colors[idx]),
                    text=['Event happened here'] * len(fan_counts),
                    hoverinfo='text',
                    customdata=list(range(len(fan_counts))),
                ))

            if len(time_data) > 1:
                line_fig.update_layout(
                    xaxis=dict(range=[max(time_data) - 100, max(time_data)]),
                )

            line_fig.update_layout(
                xaxis=dict(
                    range=[max(0, max(time_data) - 100), max(time_data)],
                    fixedrange=True,
                    showticklabels=False,
                ),
                xaxis_title='Time (Days)',
                yaxis_title='Number of Fans (in thousands)',
                margin=dict(l=0, r=0, t=40, b=0),
                autosize=False,
                width=900,
                height=400,
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=1.15,
                    xanchor='right',
                    x=1
                ),
                modebar=dict(
                    remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale2d', 'lasso2d', 'zoom2d', 'resetScale', 'toImage', 'plotly_logo']
                )
            )

            bar_fig = go.Figure(data=[
                go.Bar(
                    x=list(fan_counts_data.keys()),
                    y=current_fan_counts,
                    marker_color=colors,
                    width=0.4
                )
            ])
            bar_fig.update_layout(
                title='Current Fans per Celebrity',
                xaxis_title='Celebrity',
                yaxis_title='Current Fans',
                yaxis=dict(range=[0, (total_fans/2)-1000]),
                margin=dict(l=40, r=40, t=40, b=80),
                autosize=True,
                width=400,
                height=400,
                showlegend=False,
                modebar=dict(
                    remove=['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale2d', 'lasso2d', 'zoom2d', 'resetScale', 'toImage', 'plotly_logo']
                )
            )
            bar_fig.update_xaxes(tickangle=-45)

        else:
            line_fig = go.Figure().update_layout(
                title='No data available',
                xaxis_title='Time (seconds)',
                yaxis_title='Number of Fans'
            )
            bar_fig = go.Figure().update_layout(
                title='No data available',
                xaxis_title='Celebrity',
                yaxis_title='Current Fans'
            )

        average_fans = total_fans // len(fan_counts_data) if fan_counts_data else 0

        return line_fig, bar_fig, f'{total_fans}', most_popular_celeb or 'No data', f'{average_fans}', f'{total_events}', event_log_html

    except Exception as e:
        print(f"Error in updating graph and KPIs: {e}")
        return go.Figure().update_layout(title="Error updating graph"), go.Figure().update_layout(title="Error updating graph"), 'Error', 'Error', 'Error', 'Error', html.Div(["Error updating event log"])

@dash_app.callback(
    [Output('interval-component', 'disabled'),
     Output('start-stop-button', 'children')],
    [Input('start-stop-button', 'n_clicks')],
    [State('interval-component', 'disabled')]
)
def toggle_interval(n_clicks, is_disabled):
    if n_clicks % 2 == 0:
        print("Interval disabled")  # Debug statement
        return True, 'Start'
    else:
        print("Interval enabled")  # Debug statement
        return False, 'Stop'

# Define a route for the Flask app
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(debug=True)
