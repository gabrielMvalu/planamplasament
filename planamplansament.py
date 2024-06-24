import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon, box
import random
import pandas as pd
from io import BytesIO
from docx import Document
from docx.shared import Inches

# Funcție pentru plottarea poligonului și utilajelor
def plot_polygon_with_machines(polygon_coords, placements):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plotăm poligonul
    polygon_coords.append(polygon_coords[0])
    x_coords, y_coords = zip(*polygon_coords)
    ax.plot(x_coords, y_coords, marker='o')
    polygon_coords.pop()  # Eliminăm punctul adăugat pentru închidere

    # Setăm aspectul graficului
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Plasăm utilajele
    for (x, y, w, h, label) in placements:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha='center', va='center', fontsize=8, color='black')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Aranjarea automată a utilajelor pe plot')
    plt.grid(True)
    return fig

# Funcție pentru a verifica dacă dreptunghiul este în interiorul poligonului
def is_rect_inside_polygon(rect, polygon):
    rect_box = box(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])
    return polygon.contains(rect_box)

# Funcție pentru a verifica suprapunerea dintre două dreptunghiuri
def is_overlapping(rect1, rect2):
    r1 = box(rect1[0], rect1[1], rect1[0] + rect1[2], rect1[1] + rect1[3])
    r2 = box(rect2[0], rect2[1], rect2[0] + rect2[2], rect2[1] + rect2[3])
    return r1.intersects(r2)

# Funcție pentru a plasa automat dreptunghiurile în interiorul poligonului
def place_machines_in_polygon(machines, polygon):
    placements = []
    legend = []
    label = 'A'
    for name, length, width, quantity in machines:
        added_to_legend = False
        for _ in range(quantity):
            placed = False
            while not placed:
                minx, miny, maxx, maxy = polygon.bounds
                x = random.uniform(minx, maxx - length)
                y = random.uniform(miny, maxy - width)
                rect = (x, y, length, width)
                if is_rect_inside_polygon(rect, polygon) and all(not is_overlapping(rect, p) for p in placements):
                    placements.append((x, y, length, width, label))
                    if not added_to_legend:
                        legend.append((label, name, quantity, f"{length} x {width}"))
                        added_to_legend = True
                    placed = True
        label = chr(ord(label) + 1)  # Incrementăm labelul
    return placements, legend

# Funcție pentru a genera Word
def generate_word(fig, legend_df):
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image = buffer.read()

    doc = Document()
    doc.add_heading('Aranjarea automată a utilajelor pe plot', 0)

    # Adăugăm imaginea
    doc.add_picture(BytesIO(image), width=Inches(6))

    doc.add_heading('Legenda:', level=1)
    for _, row in legend_df.iterrows():
        doc.add_paragraph(f"{row['Identificator']}: {row['Denumire Utilaj']} - {row['Numar Bucati']} buc - {row['Dimensiune (L x l)']}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

st.title("Aranjarea utilajelor pe plot")

# Introducem coordonatele poligonului
st.header("Coordonatele poligonului")
polygon_input = st.text_area("Introduceți coordonatele poligonului (format: x1,y1 x2,y2 ...):")
polygon_coords = [tuple(map(float, coord.split(','))) for coord in polygon_input.split()]

# Introducem detaliile utilajelor
st.header("Detaliile utilajelor")
machines_data = st.text_area("Introduceți detaliile utilajelor (format: Nume,Lungime,Lățime,Număr Bucăți):")
machines = [tuple(line.split(',')) for line in machines_data.split('\n')]
machines = [(name, float(length), float(width), int(quantity)) for name, length, width, quantity in machines]

polygon = Polygon(polygon_coords)

# Plasăm automat utilajele în poligon
placements, legend = place_machines_in_polygon(machines, polygon)

# Plottăm poligonul și utilajele
fig = plot_polygon_with_machines(polygon_coords, placements)

# Creăm tabelul cu legenda
legend_df = pd.DataFrame(legend, columns=["Identificator", "Denumire Utilaj", "Numar Bucati", "Dimensiune (L x l)"])
st.table(legend_df)

# Adăugăm butonul pentru descărcare Word
if st.button("Descarcă Word"):
    word_data = generate_word(fig, legend_df)
    st.download_button(label="Descarcă Word", data=word_data, file_name="utilaje.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
