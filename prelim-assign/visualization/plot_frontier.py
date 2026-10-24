import json
import plotly.graph_objects as go
import numpy as np

# Read solver output
with open("../codebase/solver.output.json") as f:
    data = json.load(f)

no_short = data["no_short_selling"]
short = data["short_selling"]

# Extract data
returns_no_short = [p["target_return"] for p in no_short]
variance_no_short = [p["variance"] for p in no_short]
volatility_no_short = [np.sqrt(v) for v in variance_no_short]

returns_short = [p["target_return"] for p in short]
variance_short = [p["variance"] for p in short]
volatility_short = [np.sqrt(v) for v in variance_short]

# Create figure
fig = go.Figure()

# Add no short selling frontier
fig.add_trace(go.Scatter(
    x=volatility_no_short,
    y=returns_no_short,
    mode='lines+markers',
    name='No Short Selling',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=6, opacity=0.7),
    hovertemplate='<b>No Short Selling</b><br>Volatility: %{x:.4f}<br>Return: %{y:.4f}<extra></extra>'
))

# Add short selling frontier
fig.add_trace(go.Scatter(
    x=volatility_short,
    y=returns_short,
    mode='lines+markers',
    name='Short Selling Allowed',
    line=dict(color='#ff7f0e', width=3),
    marker=dict(size=6, opacity=0.7),
    hovertemplate='<b>Short Selling Allowed</b><br>Volatility: %{x:.4f}<br>Return: %{y:.4f}<extra></extra>'
))

# Update layout
fig.update_layout(
    title={
        'text': '<b>Efficient Frontier: No Short Selling vs. Short Selling Allowed</b>',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24}
    },
    xaxis_title='<b>Volatility (Standard Deviation)</b>',
    yaxis_title='<b>Expected Return</b>',
    hovermode='closest',
    template='plotly_white',
    plot_bgcolor='rgba(240, 240, 240, 0.5)',
    width=1200,
    height=700,
    font=dict(size=12),
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='#444',
        borderwidth=1
    )
)

# Add grid
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Save
fig.write_html("efficient_frontier.html")
print("Visualization saved to: visualization/efficient_frontier.html")
