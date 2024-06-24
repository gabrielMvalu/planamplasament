import streamlit as st
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader
import io

def plot_polygon(points):
    x_coords, y_coords = zip(*points)
    x_coords = list(x_coords) + [x_coords[0]]
    y_coords = list(y_coords) + [y_coords[0]]
    plt.figure(figsize=(10, 8))
    plt.plot(x_coords, y_coords, marker='o')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    st.pyplot(plt)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text

st.title("Plotare Poligon")

option = st.radio("Selectează metoda:", ('Automat', 'Manual'))

if option == 'Automat':
    uploaded_file = st.file_uploader("Încarcă documentul PDF:", type="pdf")
    if uploaded_file is not None:
        # Extragem textul din PDF
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Text extras din PDF:", text, height=200)
        # Într-un pas ulterior, vom prelucra textul pentru a extrage coordonatele și numărul de colțuri

else:
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
