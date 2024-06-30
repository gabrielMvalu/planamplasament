import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Initialize session state
if 'equipment' not in st.session_state:
    st.session_state.equipment = None
if 'selected_equipment' not in st.session_state:
    st.session_state.selected_equipment = None

# Define the polygon coordinates
polygon_coords = [
    (399485.06, 385140.713),
    (399483.58, 385140.062),
    (399477.304, 385124.575),
    (399484.305, 385122.896),
    (399492.273, 385120.567),
    (399496.347, 385138.383),
    (399485.06, 385140.713)  # Closing the polygon
]

# Define equipment data
equipment_data = [
    {"name": "Platforma tip foarfeca 1", "count": 6, "width": 1.66, "height": 0.76},
    {"name": "Platforma tip foarfeca 2", "count": 2, "width": 2.26, "height": 1.16},
    {"name": "Platforma pentru lucru la inaltime", "count": 2, "width": 2.26, "height": 0.81},
    {"name": "Platforma tip foarfeca 3", "count": 2, "width": 2.26, "height": 0.81},
    {"name": "Platforma cu brat articulat 1", "count": 2, "width": 1.83, "height": 0.76},
    {"name": "Platforma cu brat articulat 2", "count": 2, "width": 1.42, "height": 0.76},
    {"name": "Platforma cu brat articulat 3", "count": 2, "width": 1.12, "height": 0.70},
    {"name": "Rampa mobila", "count": 1, "width": 1.83, "height": 0.72},
    {"name": "Stalpi de iluminat fotovoltaici", "count": 4, "width": 0.114, "height": 0.114},
    {"name": "Toaleta ecologica", "count": 1, "width": 2.20, "height": 1.60},
    {"name": "Drujba", "count": 1, "width": 0.90, "height": 0.25},
    {"name": "Tocator resturi vegetale", "count": 1, "width": 0.707, "height": 0.388},
    {"name": "Buldoexcavator", "count": 1, "width": 3.40, "height": 1.41},
    {"name": "Container de tip birou", "count": 1, "width": 6.058, "height": 2.438},
    {"name": "Generator", "count": 1, "width": 3, "height": 1.5},
]

def initialize_equipment():
    equipment = []
    for i, item in enumerate(equipment_data):
        for j in range(item['count']):
            equipment.append({
                'id': f"{i}-{j}",
                'name': item['name'],
                'width': item['width'],
                'height': item['height'],
                'x': 399480 + (i * 2),
                'y': 385125 + (j * 2)
            })
    return pd.DataFrame(equipment)

def create_plot(df):
    fig = go.Figure()

    # Add the polygon
    fig.add_trace(go.Scatter(
        x=[coord[0] for coord in polygon_coords],
        y=[coord[1] for coord in polygon_coords],
        fill="toself",
        fillcolor="lightblue",
        line=dict(color="blue"),
        name="Land Parcel"
    ))

    # Add equipment rectangles
    for _, equip in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[equip['x'], equip['x']+equip['width'], equip['x']+equip['width'], equip['x'], equip['x']],
            y=[equip['y'], equip['y'], equip['y']+equip['height'], equip['y']+equip['height'], equip['y']],
            fill="toself",
            fillcolor="rgba(255, 0, 0, 0.5)",
            line=dict(color="red"),
            name=equip['name'],
            customdata=[equip['id']],
            hoverinfo="name"
        ))

    fig.update_layout(
        dragmode="pan",
        hovermode="closest",
        width=800,
        height=600
    )

    return fig

def main():
    st.title("Interactive Equipment Layout")

    if st.session_state.equipment is None:
        st.session_state.equipment = initialize_equipment()

    fig = create_plot(st.session_state.equipment)
    st.plotly_chart(fig)
    
    # Equipment selection and movement
    equipment_names = st.session_state.equipment['name'].unique()
    selected_equipment = st.selectbox("Select equipment to move:", equipment_names)
    
    col1, col2 = st.columns(2)
    with col1:
        new_x = st.number_input("New X coordinate:", value=float(st.session_state.equipment[st.session_state.equipment['name'] == selected_equipment]['x'].iloc[0]))
    with col2:
        new_y = st.number_input("New Y coordinate:", value=float(st.session_state.equipment[st.session_state.equipment['name'] == selected_equipment]['y'].iloc[0]))
    
    if st.button("Move Equipment"):
        mask = st.session_state.equipment['name'] == selected_equipment
        st.session_state.equipment.loc[mask, 'x'] = new_x
        st.session_state.equipment.loc[mask, 'y'] = new_y
        st.experimental_rerun()

    st.subheader("Equipment List:")
    for item in equipment_data:
        st.write(f"{item['name']} - {item['count']} buc, {item['width']}m x {item['height']}m")

if __name__ == "__main__":
    main()
