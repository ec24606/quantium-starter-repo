import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load your processed data
df = pd.read_csv("formatted_output.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Group by date
daily_sales = df.groupby("date", as_index=False)["sales"].sum()
daily_sales = daily_sales.sort_values("date")

# Create graph
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time",
    labels={"date": "Date", "sales": "Sales"}
)

# Add vertical line for price increase
fig.add_vline(x=pd.Timestamp("2021-01-15"), line_dash="dash")

# Create app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Sales Dashboard"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)