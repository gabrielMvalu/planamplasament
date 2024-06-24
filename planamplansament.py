import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def plot_polygon(polygon_coords):
    fig, ax = plt.subplots()
    polygon_coords.append(polygon_coords[0])  # Închide poligonul
    x_coords, y_coords = zip(*polygon_coords)
    ax.plot(x_coords, y_coords, marker='o')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graficul terenului')
    st.pyplot(fig)
    polygon_coords.pop()  # Elimină punctul adăugat pentru închidere

st.title("Generare Document Word pentru Utilaje")

# Selectare mod de generare
mode = st.radio("Selectează modul de generare a documentului Word:", ("Manual", "Automat"))

if mode == "Manual":
    st.header("Introducerea Coordonatelor Poligonului")

    # Introducere număr de colțuri
    num_points = st.number_input("Numărul de colțuri ale poligonului:", min_value=3, step=1)

    if num_points:
        coords = []
        for i in range(num_points):
            col1, col2 = st.columns(2)
            with col1:
                x = st.number_input(f"Coordonata X pentru punctul {i + 1}:", key=f"x_{i}")
            with col2:
                y = st.number_input(f"Coordonata Y pentru punctul {i + 1}:", key=f"y_{i}")
            coords.append((x, y))

        if st.button("Plotează Graficul"):
            plot_polygon(coords)
