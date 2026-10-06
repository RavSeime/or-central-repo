import json
import matplotlib.pyplot as plt
import numpy as np
import os

# Read solver output
with open("solver.output.json") as f:
    data = json.load(f)

no_short = data["no_short_selling"]
short = data["short_selling"]

# Extract data
returns_no_short = [p["target_return"] for p in no_short]
variance_no_short = [p["variance"] for p in no_short]

returns_short = [p["target_return"] for p in short]
variance_short = [p["variance"] for p in short]

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Plot frontiers
ax.plot(variance_no_short, returns_no_short, 'o-', linewidth=2.5, markersize=5,
        label='No Short Selling', color='#1f77b4', alpha=0.8)
ax.plot(variance_short, returns_short, 's-', linewidth=2.5, markersize=5,
        label='Short Selling Allowed', color='#ff7f0e', alpha=0.8)

# Labels and title
ax.set_xlabel('Variance', fontsize=14, fontweight='bold')
ax.set_ylabel('Expected Return', fontsize=14, fontweight='bold')
ax.set_title('Optimization Results',
             fontsize=16, fontweight='bold', pad=20)

# Grid and styling
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=12, loc='best', framealpha=0.95)
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

plt.tight_layout()

# Save as PNG
plt.savefig('efficient_frontier.png', dpi=300, bbox_inches='tight')
print("Visualization saved to: codebase/src/codebase/efficient_frontier.png")

plt.close()

#### Tangent Portfolio Analysis

# Read risk-free rate from environment
rf_rate_weekly = os.getenv('RISK_FREE_RATE')
if rf_rate_weekly is None:
    raise ValueError("RISK_FREE_RATE environment variable not set. Please set it to the weekly risk-free rate (e.g., 0.001).")

rf_rate_weekly = float(rf_rate_weekly)
rf_rate_annual = rf_rate_weekly * 52

# Calculate annualized Sharpe ratio for each point on short-selling frontier
sharpe_ratios = []
for p in short:
    ret = p["target_return"]
    var = p["variance"]

    ret_annual = ret * 52
    var_annual = var * 52
    std_annual = np.sqrt(var_annual)

    sharpe = (ret_annual - rf_rate_annual) / std_annual if std_annual > 0 else -np.inf
    sharpe_ratios.append(sharpe)

# Find tangent portfolio (max Sharpe ratio)
max_sharpe_idx = np.argmax(sharpe_ratios)
max_sharpe = sharpe_ratios[max_sharpe_idx]

# Check if tangent portfolio is better than risk-free rate
if max_sharpe <= 0:
    print(f"WARNING: No portfolio on the short-selling frontier has positive Sharpe ratio (max Sharpe = {max_sharpe:.4f}).")
    print("Skipping tangent portfolio visualization.")
else:
    tangent_portfolio = short[max_sharpe_idx]
    tangent_return = tangent_portfolio["target_return"]
    tangent_variance = tangent_portfolio["variance"]
    tangent_weights = tangent_portfolio["weights"]

    # Print tangent portfolio details
    print("\n========== TANGENT PORTFOLIO (SHORT SELLING ALLOWED) ==========")
    print(f"Annualized Sharpe Ratio: {max_sharpe:.4f}")
    print(f"Weekly Return: {tangent_return:.6f}")
    print(f"Annualized Return: {tangent_return * 52:.6f}")
    print(f"Weekly Variance: {tangent_variance:.6f}")
    print(f"Annualized Variance: {tangent_variance * 52:.6f}")
    print(f"Annualized Std Dev: {np.sqrt(tangent_variance * 52):.6f}")
    print("\nPortfolio Weights:")
    for ticker, weight in tangent_weights.items():
        if abs(weight) > 1e-6:
            print(f"  {ticker}: {weight:.6f}")
    print("=" * 60 + "\n")

    # Create tangent portfolio visualization
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot short-selling frontier
    ax.plot(variance_short, returns_short, 's-', linewidth=2.5, markersize=5,
            label='Short Selling Allowed', color='#ff7f0e', alpha=0.8)

    # Find the tangent line: a straight line from rf_rate that touches frontier at one point
    # At the tangent point, slope of line from rf = derivative of frontier curve

    # Calculate frontier derivatives using finite differences
    frontier_slopes = []
    for i in range(1, len(variance_short) - 1):
        dret = returns_short[i + 1] - returns_short[i - 1]
        dvar = variance_short[i + 1] - variance_short[i - 1]
        slope = dret / dvar if dvar != 0 else 0
        frontier_slopes.append((i, slope))

    # For each frontier point, check if line from rf is tangent
    best_tangent_idx = None
    best_error = float('inf')

    for i in range(1, len(variance_short) - 1):
        line_slope = (returns_short[i] - rf_rate_weekly) / (variance_short[i] - 0)
        frontier_slope = frontier_slopes[i - 1][1]

        # Error: how close is the line slope to frontier slope
        error = abs(line_slope - frontier_slope)

        if error < best_error:
            best_error = error
            best_tangent_idx = i

    # Draw tangent line through the tangent point
    if best_tangent_idx is not None:
        tangent_var = variance_short[best_tangent_idx]
        tangent_ret = returns_short[best_tangent_idx]
        line_slope = (tangent_ret - rf_rate_weekly) / tangent_var

        # Extend line across variance range
        var_line = np.linspace(0, max(variance_short) * 1.1, 100)
        ret_line = rf_rate_weekly + line_slope * var_line
        ax.plot(var_line, ret_line, '--', linewidth=2.5, color='#2ca02c', alpha=0.9, label='Tangent Line')

    # Plot risk-free rate point
    ax.plot(0, rf_rate_weekly, 'D', markersize=8, color='#2ca02c', alpha=0.9, label='Risk-Free Rate')

    # Plot tangent portfolio at the geometric tangent point
    if best_tangent_idx is not None:
        geometric_tangent_var = variance_short[best_tangent_idx]
        geometric_tangent_ret = returns_short[best_tangent_idx]
        ax.plot(geometric_tangent_var, geometric_tangent_ret, '*', markersize=25, color='#d62728',
                label=f'Tangent Portfolio', zorder=5)

    # Labels and title
    ax.set_xlabel('Variance', fontsize=14, fontweight='bold')
    ax.set_ylabel('Expected Return', fontsize=14, fontweight='bold')
    ax.set_title('Tangent Portfolio',
                 fontsize=16, fontweight='bold', pad=20)

    # Grid and styling
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=12, loc='best', framealpha=0.95)
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')

    plt.tight_layout()

    # Save as PNG
    plt.savefig('tangent_portfolio.png', dpi=300, bbox_inches='tight')
    print("Tangent portfolio visualization saved to: codebase/src/codebase/tangent_portfolio.png")

    plt.close()
