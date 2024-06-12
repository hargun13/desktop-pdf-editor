import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import random
from typing import Literal

# Importing pdf_viewer correctly
from streamlit_pdf_viewer import pdf_viewer

# Function to display PDF preview
def display_pdf_preview(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    st.write(f"### Previewing PDF ({num_pages} pages)")
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        st.image(page.extract_text())

def pdf_previewer(pdf: bytes, key: Literal["main", "other"] = "main") -> None:
    pdf_viewer(
        pdf,
        height=400 if key == "main" else 250,
        width=300,
        key=random.random(),  # Changed to random.random()
    )

# Function to remove selected pages
def remove_pages(pdf_file, pages_to_remove):
    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()
    num_pages = len(pdf_reader.pages)
    for page_num in range(num_pages):
        if page_num not in pages_to_remove:
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
    modified_pdf_bytes = BytesIO()
    pdf_writer.write(modified_pdf_bytes)
    pdf_writer.close()
    return modified_pdf_bytes.getvalue()

st.title("PDF Page Remover")

# Step 1: Upload a single PDF
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    # Step 2: Display PDF preview
    pdf_previewer(uploaded_pdf.read())  # Use uploaded_pdf.read() to get the bytes

    # Step 3: Allow user to input pages to remove
    pages_to_remove_str = st.text_input("Enter pages to remove (comma-separated, e.g., 1, 2, 3)")

    if pages_to_remove_str:
        try:
            # Convert input string to list of integers
            pages_to_remove = [int(page.strip()) - 1 for page in pages_to_remove_str.split(",") if page.strip().isdigit()]
            
            # Step 4: Remove selected pages and download modified PDF
            modified_pdf_bytes = remove_pages(uploaded_pdf, pages_to_remove)
            st.success("Pages removed successfully!")
            st.download_button("Download Modified PDF", modified_pdf_bytes, file_name="modified.pdf")
        except Exception as e:
            st.error(f"Error in removing pages: {e}")
