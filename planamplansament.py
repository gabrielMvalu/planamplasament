import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon, box

def plot_polygon(polygon_coords):
    fig, ax = plt.subplots()
    polygon_coords.append(polygon_coords[0])  # Închide poligonul
    x_coords, y_coords = zip(*polygon_coords)
    ax.plot(x_coords, y_coords, marker='o')

    # Adăugăm numerele pentru fiecare punct
    for i, (x, y) in enumerate(polygon_coords[:-1]):
        ax.text(x, y, str(i + 1), fontsize=12, ha='right')

    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graficul terenului')
    st.pyplot(fig)
    polygon_coords.pop()  # Elimină punctul adăugat pentru închidere

def is_rect_inside_polygon(rect, polygon):
    rect_box = box(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    return polygon.contains(rect_box)

def plot_polygon_with_machines(polygon_coords, machines):
    fig, ax = plt.subplots()
    polygon_coords.append(polygon_coords[0])  # Închide poligonul
    x_coords, y_coords = zip(*polygon_coords)
    ax.plot(x_coords, y_coords, marker='o')

    # Plotează poligonul
    poly = patches.Polygon(polygon_coords, closed=True, fill=None, edgecolor='r')
    ax.add_patch(poly)
    
    # Adaugă numere pentru fiecare punct
    for i, (x, y) in enumerate(polygon_coords[:-1]):
        ax.text(x, y, str(i + 1), fontsize=12, ha='right')

    # Definește poligonul pentru verificarea plasării
    poly_shape = Polygon(polygon_coords)
    
    # Plasarea utilajelor în interiorul poligonului
    start_x, start_y = min(x_coords), min(y_coords)  # Poziția de început în interiorul poligonului
    spacing_x, spacing_y = 0.5, 0.5  # Spațiul între elemente
    current_x, current_y = start_x, start_y
    
    for machine in machines:
        name, length, width, quantity = machine
        for _ in range(quantity):
            placed = False
            while not placed:
                rect = (current_x, current_y, length, width)
                if is_rect_inside_polygon(rect, poly_shape):
                    rect_patch = patches.Rectangle((current_x, current_y), length, width, linewidth=1, edgecolor='b', facecolor='none')
                    ax.add_patch(rect_patch)
                    ax.text(current_x + length / 2, current_y + width / 2, name, fontsize=8, ha='center')
                    current_y += width + spacing_y
                    if current_y + width > max(y_coords):
                        current_y = start_y
                        current_x += length + spacing_x
                    placed = True
                else:
                    current_y += width + spacing_y
                    if current_y + width > max(y_coords):
                        current_y = start_y
                        current_x += length + spacing_x

    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graficul terenului cu utilaje')
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
                x = st.number_input(f"Coordonata X pentru punctul {i + 1}:", format="%.3f", key=f"x_{i}")
            with col2:
                y = st.number_input(f"Coordonata Y pentru punctul {i + 1}:", format="%.3f", key=f"y_{i}")
            coords.append((x, y))

        if st.button("Plotează Graficul"):
            plot_polygon(coords)
            
    st.header("Introducerea Dimensiunilor Utilajelor")

    machines_input = st.text_area("Introdu lista de utilaje și dimensiunile acestora, în formatul dat:")

    if st.button("Plotează Graficul cu Utilaje"):
        if machines_input:
            machines_lines = machines_input.split('\n')
            machines = []
            for line in machines_lines:
                parts = line.split('-')
                if len(parts) == 4:
                    name, count, length, width = parts
                    name = name.strip()
                    count = int(count.strip().split()[0])
                    length, width = map(float, length.strip().split('x'))
                    machines.append((name, length, width, count))

            if coords and machines:
                plot_polygon_with_machines(coords, machines)
