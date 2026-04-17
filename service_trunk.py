import streamlit as st
import matplotlib.pyplot as plt

st.title("6 m Modular Service Trunk – Parametric Design")

MODULE_LENGTH = 6000
MODULE_HEIGHT = 800
MODULE_WIDTH = 2800

pipes = [
    {"dn": 150, "x": 700,  "y": 500},
    {"dn": 100, "x": 1400, "y": 500},
    {"dn": 100, "x": 1400, "y": 300},
    {"dn": 50,  "x": 1900, "y": 500},
    {"dn": 50,  "x": 1900, "y": 300},
    {"dn": 50,  "x": 2200, "y": 300},
    {"dn": 50,  "x": 2500, "y": 300},
]

def draw_service_trunk(width, height, pipes):
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.add_patch(
        plt.Rectangle((0, 0), width, height, fill=False, linewidth=2)
    )

    ax.plot([0, width], [400, 400], linestyle="--")
    ax.plot([0, width], [200, 200], linestyle="--")

    for p in pipes:
        r = p["dn"] / 2
        ax.add_patch(
            plt.Circle((p["x"], p["y"]), r, fill=False)
        )
        ax.text(p["x"], p["y"], f"DN{p['dn']}", ha="center", va="center")

    ax.set_aspect("equal")
    ax.axis("off")

    return fig

fig = draw_service_trunk(MODULE_WIDTH, MODULE_HEIGHT, pipes)
st.pyplot(fig)
