import streamlit as st
import matplotlib.pyplot as plt

# ===============================
# PAGE SETUP
# ===============================
st.set_page_config(layout="wide")
st.title("Parametric Modular Service Trunk – 6 m")

# ===============================
# CONSTANTS
# ===============================
MODULE_LENGTH_M = 6.0
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
    200: 70
}

FRAME_WEIGHT_PER_M = 45
TRAY_WEIGHT_PER_M = 15

# ===============================
# SIDEBAR INPUTS
# ===============================
st.sidebar.header("Input Parameters")

pipe_count = st.sidebar.slider("Number of pipes", 1, 6, 4)

pipe_sizes = []
for i in range(pipe_count):
    size = st.sidebar.selectbox(
        "Pipe DN " + str(i + 1),
        list(PIPE_WEIGHTS.keys()),
        key="pipe_" + str(i)
    )
    pipe_sizes.append(size)

tiers = st.sidebar.slider("Number of tiers", 1, 3, 2)

module_width = st.sidebar.slider("Module width (mm)", 800, 3600, 2800)
module_height = st.sidebar.slider("Module height (mm)", 600, 1200, 800)

tray_levels = st.sidebar.slider("Cable tray levels", 0, 3, 2)

# ===============================
# PIPE POSITIONING
# ===============================
pipes = []
x_start = 300
x_step = (module_width - 600) / max(pipe_count, 1)
tier_height = 300

index = 0
for dn in pipe_sizes:
    tier = index % tiers
    x = x_start + index * x_step
    y = 200 + tier * tier_height
    pipes.append({"dn": dn, "x": x, "y": y})
    index += 1

# ===============================
# LOAD CALCULATION
# ===============================
pipe_weight = 0
for dn in pipe_sizes:
    pipe_weight += PIPE_WEIGHTS[dn] * MODULE_LENGTH_M

frame_weight = FRAME_WEIGHT_PER_M * MODULE_LENGTH_M
tray_weight = tray_levels * TRAY_WEIGHT_PER_M * MODULE_LENGTH_M

total_weight = pipe_weight + frame_weight + tray_weight
total_load_kn = total_weight * G / 1000
load_per_m = total_load_kn / MODULE_LENGTH_M

# ===============================
# DRAWING
# ===============================
def draw_trunk(width, height, pipes, tiers, trays):
    fig, ax = plt.subplots(figsize=(14, 4))

    ax.add_patch(plt.Rectangle((0, 0), width, height, fill=False, linewidth=2))

    i = 1
    while i < tiers:
        y_line = 200 + i * tier_height
        ax.plot([0, width], [y_line, y_line], linestyle="--")
        i += 1

    t = 0
    while t < trays:
        y_tray = height - (t + 1) * 80
        ax.plot([0, width], [y_tray, y_tray], linewidth=3)
        t += 1

    for p in pipes:
        r = p["dn"] / 2
        ax.add_patch(plt.Circle((p["x"], p["y"]), r, fill=False))
        ax.text(p["x"], p["y"], "DN" + str(p["dn"]), ha="center", va="center", fontsize=9)

    ax.set_aspect("equal")
    ax.set_xlim(-150, width + 150)
    ax.set_ylim(-150, height + 150)
    ax.axis("off")

    return fig

# ===============================
# OUTPUT
# ===============================
left, right = st.columns([3, 1])

with left:
    fig = draw_trunk(module_width, module_height, pipes, tiers, tray_levels)
    st.pyplot(fig)

with right:
    st.subheader("Load Summary (6 m module)")
    st.write("Pipe weight: " + str(round(pipe_weight, 1)) + " kg")
    st.write("Frame weight: " + str(round(frame_weight, 1)) + " kg")
    st.write("Tray weight: " + str(round(tray_weight, 1)) + " kg")
    st.markdown("---")
    st.write("Total weight: " + str(round(total_weight, 1)) + " kg")
    st.write("Total load: " + str(round(total_load_kn, 2)) + " kN")
    st.write("Load per meter: " + str(round(load_per_m, 2)) + " kN/m")
