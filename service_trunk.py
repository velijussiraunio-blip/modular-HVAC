import matplotlib.pyplot as plt

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
    ax.add_patch(plt.Rectangle((0, 0), width, height, fill=False, linewidth=2))
    ax.plot([0, width], [400, 400], linestyle='--')
    ax.plot([0, width], [200, 200], linestyle='--')

    for p in pipes:
        r = p['dn'] / 2
        ax.add_patch(plt.Circle((p['x'], p['y']), r, fill=False))
        ax.text(p['x'], p['y'], f"DN{p['dn']}", ha='center', va='center')

    ax.text(width / 2, height + 40, f"{width} mm", ha='center')
    ax.text(-80, height / 2, f"{height} mm", rotation=90, va='center')
    ax.text(width / 2, -80, f"MODULE LENGTH = {MODULE_LENGTH} mm", ha='center')

    ax.set_aspect('equal')
    ax.set_xlim(-150, width + 150)
    ax.set_ylim(-150, height + 150)
    ax.axis('off')
    plt.title("6 m Modular Service Trunk – Parametric Layout")
    plt.show()


draw_service_trunk(MODULE_WIDTH, MODULE_HEIGHT, pipes)
