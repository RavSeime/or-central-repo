import json
import matplotlib.pyplot as plt
import numpy as np

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
