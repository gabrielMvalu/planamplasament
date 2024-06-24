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

def is_rect_overlap(rect1, rect2):
    rect1_box = box(rect1[0], rect1[1], rect1[0] + rect1[2], rect1[1] + rect1[3])
    rect2_box = box(rect2[0], rect2[1], rect2[0] + rect2[2], rect2[1] + rect2[3])
    return rect1_box.intersects(rect2_box)

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
    placed_rects = []  # Lista pentru dreptunghiurile plasate
    start_x, start_y = min(x_coords), min(y_coords)  # Poziția de început în interiorul poligonului
    spacing_x, spacing_y = 0.5, 0.5  # Spațiul între elemente
    current_x, current_y = start_x, start_y
    total_area = 0
    polygon_area = poly_shape.area
    
    for machine in machines:
        identifier, length, width, quantity = machine
        machine_area = length * width * quantity
        total_area += machine_area
        for _ in range(quantity):
            placed = False
            while not placed:
                rect = (current_x, current_y, length, width)
                if is_rect_inside_polygon(rect, poly_shape) and all(not is_rect_overlap(rect, placed_rect) for placed_rect in placed_rects):
                    rect_patch = patches.Rectangle((current_x, current_y), length, width, linewidth=1, edgecolor='b', facecolor='none')
                    ax.add_patch(rect_patch)
                    ax.text(current_x + length / 2, current_y + width / 2, identifier, fontsize=8, ha='center', va='center')
                    placed_rects.append(rect)
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
                if current_x + length > max(x_coords) and current_y + width > max(y_coords):
                    st.error("Utilajele nu pot fi amplasate pe terenul specificat. Verificați dimensiunile și suprafața totală.")
                    return

    if total_area > polygon_area:
        st.error("Suprafața totală a utilajelor depășește suprafața terenului. Verificați dimensiunile și numărul de utilaje.")
        return

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

    # Introducere număr de utilaje
    num_machines = st.number_input("Numărul de utilaje:", min_value=1, step=1)

    if num_machines:
        machines = []
        for i in range(num_machines):
            st.subheader(f"Utilaj {chr(65 + i)}")  # Identificator: A, B, C, etc.
            name = st.text_input(f"Nume utilaj {chr(65 + i)}:")
            count = st.number_input(f"Număr bucăți {chr(65 + i)}:", min_value=1, step=1)
            length = st.number_input(f"Lungime {chr(65 + i)} (m):", format="%.3f")
            width = st.number_input(f"Lățime {chr(65 + i)} (m):", format="%.3f")
            machines.append((chr(65 + i), length, width, count))

        if st.button("Plotează Graficul cu Utilaje"):
            if coords and machines:
                plot_polygon_with_machines(coords, machines)
