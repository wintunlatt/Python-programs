import streamlit as st
import random
import base64

# Simulated machine statuses
machine_status = {
    "machine1": random.choice(["Running", "Stopped", "Idle"]),
    "machine2": random.choice(["Running", "Stopped", "Idle"]),
    "machine3": random.choice(["Running", "Stopped", "Idle"]),
    "machine4": random.choice(["Running", "Stopped", "Idle"]),
}

# Status to color map
status_colors = {
    "Running": "green",
    "Stopped": "red",
    "Idle": "orange",
}

def get_image_data_uri(image_path):
    """Encodes an image file to a data URI."""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

def embed_image_in_svg(svg_text, image_filename="MillingMC.png"):
    """
    Replace all occurrences of MillingMC.png in the SVG text with its base64 data URI.
    """
    data_uri = get_image_data_uri(image_filename)
    return svg_text.replace("MillingMC.png", data_uri)

def modify_svg(svg_path, status_dict):
    with open(svg_path, "r") as f:
        svg = f.read()
    # Embed MillingMC.png directly into the SVG as base64 encoded data URI
    svg = embed_image_in_svg(svg, "MillingMC.png")
    
    # Apply overlays for each machine based on its status.
    for machine, status in status_dict.items():
        color = status_colors.get(status, "gray")
        # The positions must match your SVG's layout; adjust as necessary.
        x_pos = {
            "machine1": 50,
            "machine2": 200,
            "machine3": 350,
            "machine4": 500
        }.get(machine, 0)
        overlay = f"""<rect x="{x_pos}" y="50" width="100" height="75" fill="{color}" opacity="0.3"/>"""
        svg = svg.replace(f'<image id="{machine}"', overlay + f'\n  <image id="{machine}"')
    return svg

# --- Layout: Title and Logo ---
col1, col2 = st.columns([4, 1])
with col1:
    st.title("W1411 Machine Status")
with col2:
    st.image("SP_logo.png", width=100)

# Load, modify, and display the SVG with overlays
updated_svg = modify_svg("shopfloor_4machines.svg", machine_status)
st.components.v1.html(updated_svg, height=250)

# Display machine statuses with color coding
st.markdown("### Machine Statuses:")
for machine, status in machine_status.items():
    color = status_colors.get(status, "gray")
    st.markdown(f"<span style='color:{color}; font-weight:bold'>{machine}: {status}</span>", unsafe_allow_html=True)

# Show the status legend
st.markdown("### Status Legend:")
legend_html = """
<ul style='list-style: none; padding-left: 0;'>
    <li><span style='display: inline-block; width: 15px; height: 15px; background-color: green; margin-right: 10px;'></span>Running</li>
    <li><span style='display: inline-block; width: 15px; height: 15px; background-color: red; margin-right: 10px;'></span>Stopped</li>
    <li><span style='display: inline-block; width: 15px; height: 15px; background-color: orange; margin-right: 10px;'></span>Idle</li>
</ul>
"""
st.markdown(legend_html, unsafe_allow_html=True)
