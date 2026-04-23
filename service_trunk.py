import streamlit as st
import matplotlib.pyplot as plt
import math
import pandas as pd
from io import BytesIO

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(layout="wide")
st.title("Parametric Modular Service Trunk – 6 m")

# ============================================================
# CONSTANTS
# ============================================================
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

# ============================================================
# SIDEBAR INPUTS
# ============================================================
st.sidebar.header("Module Inputs")

pipe_count = st.sidebar.slider("Number of pipes", 1, 6, 4)

pipe_sizes = []
for i in range(pipe_count):
    dn = st.sidebar.selectbox(
        f"Pipe DN {i+1}",
        list(PIPE_WEIGHTS.keys()),
        key=f"dn_{i}"
    )
    pipe_sizes.append(dn)

tiers = st.sidebar.slider("Number of tiers", 1, 3, min(2, pipe_count))

module_width = st.sidebar.slider("Module width (mm)", 800, 3600, 2800)
module_height = st.sidebar.slider("Module height (mm)", 600, 1200, 800)

tray_levels = st.sidebar.slider("Cable tray levels", 0, 3, 2)

hanger_spacing = st.sidebar.slider(
    "Hanger spacing (m)",
    min_value=1.5,
    max_value=3.0,
    value=2.0,
    step=0.1
)

# ============================================================
# PIPE POSITIONING
# ============================================================
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

# ============================================================
# LOAD CALCULATION (MODULE)
# ============================================================
pipe_weight_kg = sum(
    PIPE_WEIGHTS[dn] * MODULE_LENGTH_M
    for dn in pipe_sizes
)

frame_weight_kg = FRAME_WEIGHT_PER_M * MODULE_LENGTH_M
tray_weight_kg = tray_levels * TRAY_WEIGHT_PER_M * MODULE_LENGTH_M

total_weight_kg = pipe_weight_kg + frame_weight_kg + tray_weight_kg
total_load_kn = total_weight_kg * G / 1000
load_per_m_kn = total_load_kn / MODULE_LENGTH_M

# ============================================================
# HANGER LOAD CALCULATION
# ============================================================
hanger_count = math.ceil(MODULE_LENGTH_M / hanger_spacing) + 1
hanger_load_kn = total_load_kn / hanger_count

# ============================================================
# DRAWING
# ============================================================
def draw_trunk(width, height, pipes, tiers, trays):
    fig, ax = plt.subplots(figsize=(14, 4))

    ax.add_patch(
        plt.Rectangle((0, 0), width, height, fill=False, linewidth=2)
    )

    for i in range(1, tiers):
        y_line = 200 + i * tier_height
        ax.plot([0, width], [y_line, y_line], linestyle="--", linewidth=0.6)

    for i in range(trays):
        y_tray = height - (i + 1) * 80
        ax.plot([0, width], [y_tray, y_tray], linewidth=3)
        ax.text(10, y_tray + 5, f"Cable tray {i+1}", fontsize=8)

    for p in pipes:
        r = p["dn"] / 2
        ax.add_patch(plt.Circle((p["x"], p["y"]), r, fill=False))
        ax.text(p["x"], p["y"], f"DN{p['dn']}", ha="center", va="center")

    ax.set_aspect("equal")
    ax.set_xlim(-150, width + 150)
    ax.set_ylim(-150, height + 150)
    ax.axis("off")

    return fig

# ============================================================
# BOM (DATAFRAME)
# ============================================================
bom_rows = []

for dn in pipe_sizes:
    bom_rows.append({
        "Item": "Pipe",
        "Specification": f"DN{dn}",
        "Length (m)": MODULE_LENGTH_M,
        "Weight (kg)": PIPE_WEIGHTS[dn] * MODULE_LENGTH_M
    })

bom_rows.append({
    "Item": "Frame",
    "Specification": "Steel frame",
    "Length (m)": MODULE_LENGTH_M,
    "Weight (kg)": frame_weight_kg
})

if tray_levels > 0:
    bom_rows.append({
        "Item": "Cable trays",
        "Specification": f"{tray_levels} levels",
        "Length (m)": MODULE_LENGTH_M,
        "Weight (kg)": tray_weight_kg
    })

bom_df = pd.DataFrame(bom_rows)

# ============================================================
# OUTPUT LAYOUT
# ============================================================
left, right = st.columns([3, 1])

with left:
    fig = draw_trunk(module_width, module_height, pipes, tiers, tray_levels)
    st.pyplot(fig)

with right:
    st.subheader("Module Load Summary")
    st.write(f"Pipe weight: {pipe_weight_kg:.0f} kg")
    st.write(f"Frame weight: {frame_weight_kg:.0f} kg")
    st.write(f"Tray weight: {tray_weight_kg:.0f} kg")
    st.markdown("---")
    st.write(f"Total weight: {total_weight_kg:.0f} kg")
    st.write(f"Total load: {total_load_kn:.2f} kN")
    st.write(f"Load per meter: {load_per_m_kn:.2f} kN/m")
    st.markdown("---")
    st.subheader("Hanger Loads")
    st.write(f"Hanger spacing: {hanger_spacing:.2f} m")
    st.write(f"Number of hangers: {hanger_count}")
    st.write(f"Load per hanger: {hanger_load_kn:.2f} kN")

# ============================================================
# BOM DOWNLOAD
# ============================================================
st.subheader("Bill of Materials")

st.dataframe(bom_df)

output = BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    bom_df.to_excel(writer, index=False, sheet_name="BOM")
output.seek(0)

st.download_button(
    label="Download BOM (Excel)",
    data=output,
    file_name="service_trunk_BOM.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
