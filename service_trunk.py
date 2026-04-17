import streamlit as st
import matplotlib.pyplot as plt

# -----------------------
# PAGE SETUP
# -----------------------
st.set_page_config(layout="wide")
st.title("Parametric Modular Service Trunk (6 m)")

# -----------------------
# CONSTANTS
# -----------------------
MODULE_LENGTH = 6.0  # meters
G = 9.81

PIPE_WEIGHTS = {
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

FRAME_WEIGHT_PER_M = 45     # kg/m
TRAY_WEIGHT_PER_M = 15      # kg/m per tray level

# -----------------------
# SIDEBAR INPUTS
# -----------------------
st.sidebar.header("Input Parameters")

pipe_count = st.sidebar.slider("Number of pipes", 1, 6, 4)

pipe_sizes = []
for i in range(pipe_count):
    pipe_sizes.append(
        st.sidebar.selectbox(
            f"Pipe {i+1} size (DN)",
            list(PIPE_WEIGHTS.keys()),
            index=5,
        )
    )

tiers = st.sidebar.slider("Number of tiers", 1, 3, min(2, pipe_count))
module_width = st.sidebar.slider("Module width (mm)", 800, 3600, 2800)
module_height = st.sidebar.slider("Module height (mm)", 600, 1200, 800)
tray_levels = st.sidebar.slider("Cable tray levels", 0, 3, 2)

# -----------------------
# PIPE POSITIONING
# -----------------------
pipes = []
x_start = 300
x_step = (module_width - 600) / max(pipe_count, 1)
tier_height = 300

for idx, dn in enumerate(pipe_sizes):
    tier = idx % tiers
    x = x_start + idx * x_step
    y = 200 + tier * tier_height
    pipes.append({"dn": dn, "x": x, "y": y})

# -----------------------
# LOAD CALCULATION
# -----------------------
pipe_weight_total = sum(PIPE_WEIGHTS[dn] * MODULE_LENGTH for dn in pipe_sizes)
frame_weight = FRAME_WEIGHT_PER_M * MODULE_LENGTH
tray_weight = tray_levels * TRAY_WEIGHT_PER_M * MODULE_LENGTH

total_weight_kg = pipe_weight_total + frame_weight + tray_weight
total_load_kn = total_weight_kg * G / 1000
load_per_m_kn = total_load_kn / MODULE_LENGTH

# -----------------------
# DRAWING
# -----------------------
def draw_trunk(width, height, pipes, tray_levels):
    fig, ax = plt.subplots(figsize=(14, 4))

    ax.add_patch(
        plt.Rectangle((0, 0), width, height, fill=False, linewidth=2)
    )

    for i in range(1, tiers):
        ax.plot([0, width], [200 + i * tier_height], linestyle="--", linewidth=0.6)

    for i in range(tray_levels):
        y = height - (i + 1) * 80
        ax.plot([0, width], [y, y], linewidth=3)
        ax.text(10, y + 5, f"Cable tray {i+1}", fontsize=8)

    for p in pipes:
        r = p["dn"] / 2
        ax.add_patch(
            plt.Circle((p["x"], p["y"]), r, fill=False, linewidth=1.5)
        )
        ax.text(p["x"], p["y"], f"DN{p['dn']}", ha="center", va="center", fontsize=9)

    ax.set_aspect("equal")
    ax.set_xlim(-150, width + 150)
    ax.set_ylim(-150, height + 150)
    ax.axis("off")

    return fig

# -----------------------
# OUTPUT
# -----------------------
col1, col2 = st.columns([3, 1])

with col1:
    fig = draw_trunk(module_width, module_height, pipes, tray_levels)
    st.pyplot(fig)

with col2:
    st.subheader("Module Load Summary")
    st.write(f"**Pipe weight:** {pipe_weight_total:.0f} kg")
    st.write(f"**Frame weight:** {frame_weight:.0f} kg")
    st.write(f"**Tray weight:** {tray_weight:.0f} kg")
    st.markdown("---")
    st.write(f"**Total weight:** {total_weight_kg:.0f} kg")
    st.write(f"**Total load:** {total_load_kn:.2f} kN")
    st.write(f"**Load per meter:** {load_per_m_kn:.2f} kN/m")
