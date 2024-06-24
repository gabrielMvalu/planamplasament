import streamlit as st
import matplotlib.pyplot as plt

def plot_polygon(points):
    x_coords, y_coords = zip(*points)
    x_coords = list(x_coords) + [x_coords[0]]
    y_coords = list(y_coords) + [y_coords[0]]
    plt.figure(figsize=(10, 8))
    plt.plot(x_coords, y_coords, marker='o')
    plt.title('Poligon cu colțurile specificate')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    st.pyplot(plt)

st.title("Plotare Poligon")
num_points = st.number_input("Introdu numărul de colțuri ale poligonului:", min_value=3, step=1)

coords = []
for i in range(num_points):
    x = st.number_input(f"Introdu coordonata X pentru punctul {i+1}:", format="%.6f")
    y = st.number_input(f"Introdu coordonata Y pentru punctul {i+1}:", format="%.6f")
    coords.append((x, y))

if st.button("Plotează Poligonul"):
    if len(coords) == num_points:
        plot_polygon(coords)
    else:
        st.error("Te rog introdu toate coordonatele necesare.")

