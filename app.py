import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_output.csv")
df["date"] = pd.to_datetime(df["date"])

app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f8f5f0",
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Arial, sans-serif"
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": "white",
                "padding": "30px",
                "borderRadius": "15px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.15)"
            },
            children=[
                html.H1(
                    "Soul Foods Pink Morsel Sales Dashboard",
                    style={
                        "textAlign": "center",
                        "color": "#c2185b",
                        "marginBottom": "10px"
                    }
                ),

                html.P(
                    "Explore Pink Morsel sales over time and compare performance before and after the price increase on 15 January 2021.",
                    style={
                        "textAlign": "center",
                        "color": "#555",
                        "fontSize": "16px",
                        "marginBottom": "25px"
                    }
                ),

                html.Div(
                    [
                        html.Label(
                            "Filter by Region:",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "18px",
                                "marginRight": "15px",
                                "color": "#333"
                            }
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            labelStyle={
                                "marginRight": "20px",
                                "fontSize": "16px",
                                "color": "#444"
                            },
                            style={"marginBottom": "30px"}
                        ),
                    ],
                    style={"textAlign": "center"}
                ),

                dcc.Graph(id="sales-chart")
            ]
        )
    ]
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["region"].str.lower() == selected_region]

    daily_sales = filtered_df.groupby("date", as_index=False)["sales"].sum()
    daily_sales = daily_sales.sort_values("date")

    title = "Pink Morsel Sales Over Time"
    if selected_region != "all":
        title = f"Pink Morsel Sales Over Time - {selected_region.capitalize()} Region"

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title=title,
        labels={"date": "Date", "sales": "Sales"},
        markers=True
    )

    fig.add_vline(x=pd.Timestamp("2021-01-15"), line_dash="dash")

    fig.update_layout(
        plot_bgcolor="#fffafc",
        paper_bgcolor="white",
        font=dict(color="#333", size=14),
        title_font=dict(size=22),
        xaxis=dict(showgrid=True, gridcolor="#f0d7e2"),
        yaxis=dict(showgrid=True, gridcolor="#f0d7e2"),
        margin=dict(l=40, r=40, t=70, b=40)
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)