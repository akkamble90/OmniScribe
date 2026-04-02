from fpdf import FPDF
import datetime

def generate_pdf(content, title="OmniScribe Analysis Report"):
    # 1. CLEANING THE TEXT (Keep this to prevent the previous latin-1 error)
    clean_content = content.replace('\u2013', '-')
    clean_content = clean_content.replace('\u2014', '-')
    clean_content = clean_content.replace('\u2018', "'")
    clean_content = clean_content.replace('\u2019', "'")
    clean_content = clean_content.replace('\u201c', '"')
    clean_content = clean_content.replace('\u201d', '"')
    clean_content = clean_content.replace('\u2022', '*')
    
    # Force to latin-1 compatibility
    clean_content = clean_content.encode('latin-1', 'ignore').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()
    
    # 2. Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    
    # 3. Date info
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')
    pdf.ln(10)
    
    # 4. Content body
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, clean_content)
    
    # 5. Footer
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 5, "Disclaimer: AI-generated report. Consult professionals for final decisions.")
    
    # THE FIX: Just return the output. dest='S' returns the byte string/bytearray we need.
    pdf_output = pdf.output(dest='S')
    return bytes(pdf_output)