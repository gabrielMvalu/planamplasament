from fpdf import FPDF

def generate_pdf(legend_text, image_path, output_path):
    pdf = FPDF()
    pdf.add_page()

    # Add plot image to PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Graficul Terenului cu Utilaje', 0, 1, 'C')
    pdf.image(image_path, x=10, y=30, w=190)

    # Add legend to PDF
    image_height = 190 * 0.75  # Assuming the aspect ratio of the image is 4:3
    legend_y = 30 + image_height + 10  # Adjust the starting y position for the legend
    pdf.set_y(legend_y)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Legenda', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, legend_text)

    # Save PDF
    pdf.output(output_path)
