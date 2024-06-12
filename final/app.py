import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
import random
from typing import Literal

# Importing pdf_viewer correctly
from streamlit_pdf_viewer import pdf_viewer

# Function to display PDFs in the streamlit app
def display_pdfs(pdf_files):
    for i, pdf_file in enumerate(pdf_files):
        st.write(f"###### PDF {i+1}: ", pdf_file.name)

# Function to merge PDFs
def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merged_pdf_bytes = BytesIO()
    merger.write(merged_pdf_bytes)
    merger.close()
    return merged_pdf_bytes.getvalue()

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

# Function to add password to a PDF
def add_password(pdf_file, password):
    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    pdf_writer.encrypt(password)
    protected_pdf_bytes = BytesIO()
    pdf_writer.write(protected_pdf_bytes)
    pdf_writer.close()
    return protected_pdf_bytes.getvalue()

# Function to remove password from a PDF
def remove_password(pdf_file, password):
    pdf_reader = PdfReader(pdf_file)
    if pdf_reader.is_encrypted:
        pdf_reader.decrypt(password)
    pdf_writer = PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    unprotected_pdf_bytes = BytesIO()
    pdf_writer.write(unprotected_pdf_bytes)
    pdf_writer.close()
    return unprotected_pdf_bytes.getvalue()

# Main application
st.title("PDF Tools Application")

# Step 1: Provide options to choose between different PDF tools
option = st.sidebar.selectbox(
    "Choose an option",
    ("PDF Merger", "PDF Page Remover", "PDF Password Manager")
)

if option == "PDF Merger":
    st.header("PDF Merger Application")

    # Step 1: Upload multiple PDFs
    uploaded_pdfs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

    if uploaded_pdfs:
        # Step 2: Display uploaded PDFs
        st.write("### Uploaded PDFs")
        display_pdfs(uploaded_pdfs)

        # Step 3: Allow users to change the order of PDFs
        st.write("### Reorder PDFs")
        order = st.text_input("Enter the new order of PDFs (comma-separated indices, starting from 1)",
                              value=",".join(map(str, range(1, len(uploaded_pdfs) + 1))))

        try:
            new_order = [int(i) - 1 for i in order.split(",")]
            reordered_pdfs = [uploaded_pdfs[i] for i in new_order]

            # Step 4: Display reordered PDFs
            st.write("### Reordered PDFs")
            display_pdfs(reordered_pdfs)

            # Step 5: Combine PDFs
            if st.button("Combine PDFs"):
                combined_pdf_bytes = merge_pdfs(reordered_pdfs)
                st.success("PDFs combined successfully!")
                st.download_button("Download Combined PDF", combined_pdf_bytes, file_name="combined.pdf")
        except Exception as e:
            st.error(f"Error in reordering PDFs: {e}")

elif option == "PDF Page Remover":
    st.header("PDF Page Remover")

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

elif option == "PDF Password Manager":
    st.header("PDF Password Manager")

    # Step 1: Upload a single PDF
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_pdf:
        pdf_reader = PdfReader(uploaded_pdf)
        if pdf_reader.is_encrypted:
            password = st.text_input("Enter the PDF password", type="password")
            try:
                pdf_reader.decrypt(password)
                st.success("Password accepted")
                action = st.selectbox("Choose an action", ("Add Password", "Remove Password"))
                if action == "Add Password":
                    new_password = st.text_input("Enter new password", type="password")
                    if st.button("Add Password"):
                        protected_pdf_bytes = add_password(uploaded_pdf, new_password)
                        st.success("Password added successfully!")
                        st.download_button("Download Protected PDF", protected_pdf_bytes, file_name="protected.pdf")
                elif action == "Remove Password":
                    if st.button("Remove Password"):
                        unprotected_pdf_bytes = remove_password(uploaded_pdf, password)
                        st.success("Password removed successfully!")
                        st.download_button("Download Unprotected PDF", unprotected_pdf_bytes, file_name="unprotected.pdf")
            except Exception as e:
                st.error(f"Incorrect password: {e}")
        else:
            st.success("PDF is not password protected")
            action = st.selectbox("Choose an action", ("Add Password",))
            if action == "Add Password":
                new_password = st.text_input("Enter new password", type="password")
                if st.button("Add Password"):
                    protected_pdf_bytes = add_password(uploaded_pdf, new_password)
                    st.success("Password added successfully!")
                    st.download_button("Download Protected PDF", protected_pdf_bytes, file_name="protected.pdf")