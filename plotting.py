import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon
import streamlit as st

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

def plot_polygon_with_machines(polygon_coords, machines, save_path=None):
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
            iteration_count = 0  # Adăugăm un contor de iterații pentru a preveni buclele infinite
            max_iterations = 1000  # Stabilim un număr maxim de iterații pentru a opri bucla dacă devine infinită
            while not placed:
                iteration_count += 1
                if iteration_count > max_iterations:
                    st.error("Utilajele nu pot fi amplasate pe terenul specificat. Verificați dimensiunile și suprafața totală.")
                    return False
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
                    return False

    if total_area > polygon_area:
        st.error("Suprafața totală a utilajelor depășește suprafața terenului. Verificați dimensiunile și numărul de utilaje.")
        return False

    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Graficul terenului cu utilaje')
    
    if save_path:
        plt.savefig(save_path)
    
    st.pyplot(fig)
    polygon_coords.pop()  # Elimină punctul adăugat pentru închidere
    return True
