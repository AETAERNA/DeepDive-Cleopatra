"""
Muon tomography simulation for Taposiris Magna.

This script models muon flux attenuation through limestone for a rectangular search area
containing a 20 × 20 m void and an approximate tunnel running seaward. The
simulation computes the percentage excess in muon flux within the void relative
to the surrounding host rock and produces a heatmap showing flux excess across
the grid.  The result is saved in the `output/` directory, and the peak excess
value is printed to the console.
"""
import numpy as np
import matplotlib.pyplot as plt
import os

# Simulation parameters
GRID_SIZE = 50  # Total width and height of the grid (m)
RES = 1.0       # Grid resolution (m)
VOID_SIZE = 20  # Width and height of the void (m)
VOID_DEPTH_MIN, VOID_DEPTH_MAX = 25, 45  # Depth range of the cavity (m)
LIMESTONE_DENSITY = 2.7  # g/cm^3, approximate density of limestone
OVERBURDEN = 35  # Average overburden thickness above the void (m)
TUNNEL_REDUCTION = 10  # Reduction in overburden along the tunnel (m)

# Create coordinate grid
X, Y = np.meshgrid(
    np.arange(-GRID_SIZE / 2, GRID_SIZE / 2, RES),
    np.arange(-GRID_SIZE / 2, GRID_SIZE / 2, RES)
)

# Masks for the void and tunnel
in_void = (np.abs(X) < VOID_SIZE / 2) & (np.abs(Y) < VOID_SIZE / 2)
in_tunnel = (Y < -10) & (np.abs(X) < 5)  # Approximate straight tunnel path

# Compute overburden thickness at each grid cell
overburden = np.full(X.shape, OVERBURDEN, dtype=float)
overburden[in_void] -= (VOID_DEPTH_MAX - VOID_DEPTH_MIN)
overburden[in_tunnel] -= TUNNEL_REDUCTION

# Compute a simplified muon flux excess.  Instead of modelling the full exponential
# attenuation through rock, we approximate the percentage increase in muon counts
# relative to the average overburden thickness.  Overburden reductions (due to
# the void or tunnel) allow more muons to pass through.  The excess is
# calculated as (background_overburden - local_overburden) / background_overburden * 100.
bg_overburden = OVERBURDEN
excess = (bg_overburden - overburden) / bg_overburden * 100

# Create output directory
os.makedirs('output', exist_ok=True)

# Plot the excess map
fig, ax = plt.subplots()
img = ax.imshow(
    excess,
    extent=[-GRID_SIZE / 2, GRID_SIZE / 2, -GRID_SIZE / 2, GRID_SIZE / 2],
    vmin=-10,
    vmax=30
)
ax.set_title('Muon Flux Excess Map – Taposiris Anomaly & Tunnel')

# Draw the void boundary
void_rect = plt.Rectangle(
    (-VOID_SIZE / 2, -VOID_SIZE / 2),
    VOID_SIZE,
    VOID_SIZE,
    fill=False,
    linewidth=2
)
ax.add_patch(void_rect)

# Draw the approximate tunnel projection
ax.plot([0, 0], [-10, -GRID_SIZE / 2], linestyle='--')

# Add a colour bar (no specific colormap specified)
cb = plt.colorbar(img, ax=ax, label='Flux excess (%)')

# Save figure
fig.savefig('output/muon_sim_taposiris_2026.png', dpi=300)

print(f"Peak excess in chamber: {excess[in_void].max():.1f}%")