import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Definim coordonatele poligonului
polygon_coords = [
    (399485.06, 385140.713),
    (399483.58, 385140.062),
    (399477.304, 385124.575),
    (399484.305, 385122.896),
    (399492.273, 385120.567),
    (399496.347, 385138.383)
]

# Definim dimensiunile utilajelor (Lungime x Lățime)
machines = [
    ("Platforma pentru lucru la inaltime - tip foarfeca 1", 1.66, 0.76, 6),
    ("Platforma pentru lucru la inaltime - tip foarfeca 2", 2.26, 1.16, 2),
    ("Platforma pentru lucru la inaltime", 2.26, 0.81, 2),
    ("Platforma pentru lucru la inaltime - tip foarfeca 3", 2.26, 0.81, 2),
    ("Platforma pentru lucru la inaltime cu brat articulat 1", 1.83, 0.76, 2),
    ("Platforma pentru lucru la inaltime cu brat articulat 2", 1.42, 0.76, 2),
    ("Platforma pentru lucru la inaltime cu brat articulat 3", 1.12, 0.70, 2),
    ("Rampa mobila", 1.83, 0.72, 1),
    ("Stalpi de iluminat fotovoltaici mobili", 0.114, 0.114, 4),
    ("Toaleta ecologica", 2.20, 1.60, 1),
    ("Drujba", 0.90, 0.25, 1),
    ("Tocator resturi vegetale", 0.707, 0.388, 1),
    ("Buldoexcavator", 3.40, 1.41, 1),
    ("Container de tip birou", 6.058, 2.438, 1),
    ("Generator", 3.00, 1.50, 1)
]

# Funcție pentru plottarea poligonului și utilajelor
def plot_polygon_with_machines(polygon_coords, machines):
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
    start_x, start_y = min(x_coords), min(y_coords)
    offset_x, offset_y = 5, 5  # Offset pentru plasare
    for machine_name, length, width, quantity in machines:
        for _ in range(quantity):
            rect = patches.Rectangle((start_x + offset_x, start_y + offset_y), length, width, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            offset_x += length + 1  # Actualizăm offset-ul pentru următorul utilaj
            if offset_x + length > max(x_coords) - min(x_coords):
                offset_x = 5
                offset_y += width + 1

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Aranjarea automată a utilajelor pe plot')
    plt.grid(True)
    plt.show()

# Apelăm funcția pentru plottare
plot_polygon_with_machines(polygon_coords, machines)
