
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
customer_df = pd.read_csv("customer_data.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Customer Insights Dashboard", style={"textAlign": "center"}),
    
    # Dropdown to filter by region
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": region, "value": region} for region in customer_df["Region"].unique()] + [{"label": "All", "value": "All"}],
            value="All"
        )
    ], style={"width": "50%", "margin": "auto"}),
    
    # KPI cards
    html.Div([
        html.Div(id="total-customers", style={"display": "inline-block", "margin": "10px"}),
        html.Div(id="avg-spend", style={"display": "inline-block", "margin": "10px"}),
        html.Div(id="churn-rate", style={"display": "inline-block", "margin": "10px"}),
    ], style={"textAlign": "center"}),
    
    # Segmentation scatter plot
    html.Div([
        dcc.Graph(id="cluster-plot")
    ]),

    # Churn pie chart
    html.Div([
        dcc.Graph(id="churn-pie-chart")
    ]),
])

# Callbacks to update visuals
@app.callback(
    [Output("total-customers", "children"),
     Output("avg-spend", "children"),
     Output("churn-rate", "children"),
     Output("cluster-plot", "figure"),
     Output("churn-pie-chart", "figure")],
    [Input("region-dropdown", "value")]
)
def update_dashboard(region):
    # Filter data by region
    if region != "All":
        filtered_df = customer_df[customer_df["Region"] == region]
    else:
        filtered_df = customer_df

    # KPIs
    total_customers = f"Total Customers: {len(filtered_df)}"
    avg_spend = f"Average Spend: ${filtered_df['PurchaseAmount'].mean():.2f}"
    churn_rate = f"Churn Rate: {filtered_df['Churn'].mean() * 100:.2f}%"

    # Cluster scatter plot
    scatter_fig = px.scatter(
        filtered_df,
        x="PurchaseAmount",
        y="Frequency",
        color="Cluster",
        title="Customer Segmentation",
        labels={"PurchaseAmount": "Purchase Amount", "Frequency": "Purchase Frequency"}
    )

    # Churn pie chart
    churn_fig = px.pie(
        filtered_df,
        names="Churn",
        title="Churn Distribution",
        labels={0: "Not Churn", 1: "Churn"},
    )

    return total_customers, avg_spend, churn_rate, scatter_fig, churn_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
