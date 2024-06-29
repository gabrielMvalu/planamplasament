import streamlit as st
import tempfile
from plotting import plot_polygon, plot_polygon_with_machines
from pdf_generation import generate_pdf
from utils import is_rect_inside_polygon, is_rect_overlap
import requests

def main():
    st.title(':blue[Generare PDF Plan Amplasament cu legenda]')

    # Selectare mod de generare
    mode = st.sidebar.radio("Selectează modul de adaugare a datelor:", ("Manual", "Automat"))

    if mode == "Manual":
        manual_mode()
    elif mode == "Automat":
        automatic_mode()

def manual_mode():
    st.header("Adauga Coordonatele Poligonului")

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
    
    add_machines_section(coords)

def automatic_mode():
    st.header("Încarca PDF Extras de Carte Funciara")

    uploaded_file = st.file_uploader("Alege un PDF", type=["pdf"])

    coords = []
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
            tmpfile.write(uploaded_file.getbuffer())
            temp_pdf_path = tmpfile.name

        st.write("PDF încărcat cu succes. Coordonatele vor fi extrase automat.")

        # Aici vom adăuga codul pentru a trimite PDF-ul la API-ul OpenAI GPT Vision
        coordinates = extract_coordinates_from_pdf(temp_pdf_path)

        if coordinates:
            st.write("Coordonatele au fost extrase cu succes.")
            st.write(coordinates)
            coords = coordinates
            plot_polygon(coords)
        else:
            st.write("Nu s-au putut extrage coordonatele din PDF.")

    add_machines_section(coords)

def add_machines_section(coords):
    st.header("Adauga Dimensiunile Utilajelor")

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

def extract_coordinates_from_pdf(pdf_path):
    api_key = "YOUR_OPENAI_API_KEY"
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    response = requests.post(
        url,
        headers=headers,
        files={"file": pdf_data}
    )

    if response.status_code == 200:
        response_data = response.json()
        coordinates = parse_coordinates(response_data)
        return coordinates
    else:
        st.error("Eroare la extragerea coordonatelor din PDF.")
        return None

def parse_coordinates(response_data):
    # Implement your logic to parse coordinates from the response data
    # This might require custom logic based on the format of the response
    pass

if __name__ == "__main__":
    main()



