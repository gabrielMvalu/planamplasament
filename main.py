import streamlit as st
import tempfile
from plotting import plot_polygon, plot_polygon_with_machines
from pdf_generation import generate_pdf
from utils import is_rect_inside_polygon, is_rect_overlap

def main():
    st.title("Generare Document Word pentru Utilaje")

    # Selectare mod de generare
    mode = st.sidebar.radio("Selectează modul de generare a documentului Word:", ("Manual", "Automat"))

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
            legend_text = ""
            for i in range(num_machines):
                st.subheader(f"Utilaj {chr(65 + i)}")  # Identificator: A, B, C, etc.
                name = st.text_input(f"Nume utilaj {chr(65 + i)}:")
                count = st.number_input(f"Număr bucăți {chr(65 + i)}:", min_value=1, step=1)
                length = st.number_input(f"Lungime {chr(65 + i)} (m):", format="%.3f")
                width = st.number_input(f"Lățime {chr(65 + i)} (m):", format="%.3f")
                machines.append((chr(65 + i), length, width, count))
                legend_text += f"{chr(65 + i)}: {name} - {count} buc - {length} x {width} m\n"

            if st.button("Plotează Graficul cu Utilaje"):
                if coords and machines:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        image_path = tmpfile.name
                    success = plot_polygon_with_machines(coords, machines, save_path=image_path)
                    if success:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
                            pdf_output_path = tmpfile.name
                        generate_pdf(legend_text, image_path, pdf_output_path)
                        st.success('PDF generat cu succes!')
                        st.download_button(
                            label="Descarcă PDF",
                            data=open(pdf_output_path, "rb").read(),
                            file_name="plot_with_legend.pdf",
                            mime="application/pdf"
                        )

if __name__ == "__main__":
    main()




