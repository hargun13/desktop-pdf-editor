import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

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

st.title("PDF Merger Application")

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
