import streamlit as st
import matplotlib.pyplot as plt
import math

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(layout="wide")
st.title("Parametric Modular Service Trunk – 6 m")

# ============================================================
# CONSTANTS
# ============================================================
MODULE_LENGTH_M = 6.0          # meters
G = 9.81                       # gravity

PIPE_WEIGHTS_KG_PER_M = {
    25: 4,
    40: 6,
    50: 8,
    65: 11,
    80: 14,
    100: 20,
    125: 28,
    150: 38,
    200: 70,
}

FRAME_WEIGHT_KG_PER_M = 45     # steel frame
TRAY_WEIGHT_KG_PER_M = 15      # per tray level

# ============================================================
# SIDEBAR INPUTS
# ============================================================
st.sidebar.header("Module Inputs")

pipe_count = st.sidebar.slider(
    "Number of pipes",
    min_value=1,
    max_value=6,
    value=4
)

pipe_sizes = []
for i in range(pipe_count):
    dn = st.sidebar.selectbox(
        f"Pipe {i+1} DN",
        options=list(PIPE_WEIGHTS_KG_PER_M.keys()),
        index=5,
        key=f"dn_{i}"
    )
    pipe_sizes.append(dn)

tiers = st.sidebar.slider(
    "Number of vertical tiers",
    min_value=1,
    max_value=3,
    value=min(2, pipe_count)
)

module_width_mm = st.sidebar.slider(
    "Module width (mm)",
    min_value=800,
    max_value=3600,
    value=2800
)

module_height_mm = st.sidebar.slider(
    "Module height (mm)",
    min_value=600,
    max_value=1200,
    value=800
)

tray_levels = st.sidebar.slider(
    "Cable tray levels",
    min_value=0,
    max_value=3,
    value=2
)

# ============================================================
# PIPE POSITIONING (AUTOMATIC)
# ============================================================
pipes = []
x_start = 300
x_step = (module_width_mm - 600) / max(pipe_count, 1)
tier_height = 300

for idx, dn in enumerate(pipe_sizes):
    tier = idx % tiers
    x = x_start + idx * x_step
    y = 200 + tier * tier_height
    pipes.append({
        "dn": dn,
        "x": x,
        "y": y
    })

# ============================================================
# LOAD CALCULATION
# ============================================================
pipe_weight_kg = sum(
    PIPE_WEIGHTS_KG_PER_M[dn] * MODULE_LENGTH_M
    for dn in pipe_sizes
)

frame_weight_kg = FRAME_WEIGHT_KG_PER_M * MODULE_LENGTH_M
tray_weight_kg = tray_levels * TRAY_WEIGHT_KG_PER_M * MODULE_LENGTH_M

total_weight_kg = pipe_weight_kg + frame_weight_kg + tray_weight_kg
total_load_kn = total_weight_kg * G / 1000
load_per_m_kn = total_load_kn / MODULE_LENGTH_M

# ============================================================
# DRAWING FUNCTION
# ============================================================
def draw_trunk(width, height, pipes, tiers, trays):
    fig, ax = plt.subplots(figsize=(14, 4))

    # Frame
    ax.add_patch(
        plt.Rectangle((0, 0), width, height, fill=False, linewidth=2)
    )

    # Tier lines (FIXED BUG!)
    for i in range(1, tiers):
        y = 200 + i * tier_height
        ax.plot([0, width], [y, y], linestyle="--", linewidth=0.6)

    # Cable trays
    for i in range(trays):
        y = height - (i + 1) * 80
        ax.plot([0, width], [y, y], linewidth=3)
        ax.text(10, y + 5, f"Cable tray {i+1}", fontsize=8)

    # Pipes
    for p in pipes:
        r = p["dn"] / 2
        ax.add_patch(
            plt.Circle((p["x"], p["y"]), r, fill=False, linewidth=1.5)
        )
        ax.text(
            p["x"], p["y"],
            f"DN{p['dn']}",
            ha="center", va="center",
            fontsize=9
        )

    # Dimensions
    ax.text(width / 2, height + 40, f"{width} mm", ha="center")
    ax.text(-90, height / 2, f"{height} mm", rotation=90, va="center")

    ax.set_aspect("equal")
    ax.set_xlim(-150, width + 150)
    ax.set_ylim(-150, height + 150)
    ax.axis("off")

    return fig

# ============================================================
# OUTPUT LAYOUT
# ============================================================
left, right = st.columns([3, 1])

with left:
    fig = draw_trunk(
        module_width_mm,
        module_height_mm,
        pipes,
        tiers,
        tray_levels
    )
    st.pyplot(fig)

with right:
    st.subheader("Load Summary (per 6 m module)")
    st.write(f"**Pipe weight:** {pipe_weight_kg:.0f} kg")
    st.write(f"**Frame weight:** {frame_weight_kg:.0f} kg")
    st.write(f"**Tray weight:** {tray_weight_kg:.0f} kg")
    st.markdown("---")
    st.write(f"**Total weight:** {total_weight_kg:.0f} kg")
    st.write(f"**Total load:** {total_load_kn:.2f} kN")
    st.write(f"**Load per meter:** {load_per_m_kn:.2f} kN/m")
``
