import streamlit as st

try:
    import os
    import sys
    import traceback
    from io import BytesIO

    from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
    from pypdf.errors import FileNotDecryptedError
    # from st_social_media_links import SocialMediaIcons
    from streamlit import session_state
    from streamlit_pdf_viewer import pdf_viewer

    import utils


    PAGE_STR_HELP = """
    Format
    ------
    **all:** all pages  
    **2:** 2nd page  
    **1-3:** pages 1 to 3  
    **2,4:** pages 2 and 4  
    **1-3,5:** pages 1 to 3 and 5"""


    # ---------- HEADER ----------
    st.title("📄 Welcome to PDF WorkDesk!")

    # ---------- INIT SESSION STATES ----------
    session_state["decrypted_filename"] = (
        None
        if "decrypted_filename" not in session_state
        else session_state["decrypted_filename"]
    )
    session_state["password"] = (
        "" if "password" not in session_state else session_state["password"]
    )
    session_state["is_encrypted"] = (
        False if "is_encrypted" not in session_state else session_state["is_encrypted"]
    )
    # ---------- SIDEBAR ----------
    with st.sidebar:
        with st.expander("✅ Supported operations"):
            st.info(
                "* Upload from disk/URL\n"
                "* Preview content/metadata\n"
                "* Extract text/images\n"
                "* Add/remove password\n"
                "* Rotate/resize PDF\n"
                "* Merge PDFs\n"
                "* Reduce PDF size\n"
            )

        try:
            pdf, reader, session_state["password"], session_state["is_encrypted"] = (
                utils.load_pdf(key="main")
            )

        except FileNotDecryptedError:
            pdf = "password_required"

    # ---------- OPERATIONS ----------
    # TODO: Extract attachments (https://pypdf.readthedocs.io/en/stable/user/extract-attachments.html)
    # TODO: Undo last operation
    # TODO: Update metadata (https://pypdf.readthedocs.io/en/stable/user/metadata.html)

    if pdf == "password_required":
        st.error("PDF is password protected. Please enter the password to proceed.")
    elif pdf:
        lcol, rcol = st.columns(2)

        with lcol.expander(
            f"🔐 {'Change' if session_state['is_encrypted'] else 'Add'} password"
        ):
            new_password = st.text_input(
                "Enter password",
                type="password",
            )

            algorithm = st.selectbox(
                "Algorithm",
                options=["RC4-40", "RC4-128", "AES-128", "AES-256-R5", "AES-256"],
                index=3,
                help="Use `RC4` for compatibility and `AES` for security",
            )

            filename = f"protected_{session_state['name']}"

            if st.button(
                "🔒 Submit",
                use_container_width=True,
                disabled=(len(new_password) == 0),
            ):
                with PdfWriter() as writer:
                    # Add all pages to the writer
                    for page in reader.pages:
                        writer.add_page(page)

                    # Add a password to the new PDF
                    writer.encrypt(new_password, algorithm=algorithm)

                    # Save the new PDF to a file
                    with open(filename, "wb") as f:
                        writer.write(f)

            if os.path.exists(filename):
                st.download_button(
                    "⬇️ Download protected PDF",
                    data=open(filename, "rb"),
                    mime="application/pdf",
                    file_name=filename,
                    use_container_width=True,
                )

        with rcol.expander("🔓 Remove password"):
            if reader.is_encrypted:
                st.download_button(
                    "⬇️ Download unprotected PDF",
                    data=open(session_state["decrypted_filename"], "rb"),
                    mime="application/pdf",
                    file_name=session_state["decrypted_filename"],
                    use_container_width=True,
                )
            else:
                st.info("PDF does not have a password")

        with st.expander("🔃 Rotate PDF"):
            # TODO: Add password back to converted PDF if original was protected
            st.caption("Will remove password if present")
            angle = st.slider(
                "Clockwise angle",
                min_value=0,
                max_value=360,
                step=90,
                format="%d°",
            )

            with PdfWriter() as writer:
                for page in reader.pages:
                    writer.add_page(page)
                    writer.pages[-1].rotate(angle)

                # TODO: Write to byte_stream
                writer.write("rotated.pdf")

                with open("rotated.pdf", "rb") as f:
                    pdf_viewer(f.read(), height=250, width=300)
                    st.download_button(
                        "⬇️ Download rotated PDF",
                        data=f,
                        mime="application/pdf",
                        file_name=f"{session_state['name'].rsplit('.')[0]}_rotated_{angle}.pdf",
                        use_container_width=True,
                    )


        with st.expander("➕ Merge PDFs"):
            # TODO: Add password back to converted PDF if original was protected
            st.caption(
                "Second PDF will be appended to the first. Passwords will be removed from both."
            )
            # TODO: Add more merge options (https://pypdf.readthedocs.io/en/stable/user/merging-pdfs.html#showing-more-merging-options)
            pdf_to_merge, reader_to_merge, *_ = utils.load_pdf(key="merge")

            col1, col2 = st.columns(2)

            if col1.button(
                "➕ Merge PDFs", disabled=(not pdf_to_merge), use_container_width=True
            ):
                with PdfWriter() as merger:
                    for file in (reader, reader_to_merge):
                        merger.append(file)

                    # TODO: Write to byte_stream
                    merger.write("merged.pdf")

                    with col2:
                        pdf_viewer(
                            open("merged.pdf", "rb").read(),
                            height=250,
                            width=300,
                        )
                    st.download_button(
                        "⬇️ Download merged PDF",
                        data=open("merged.pdf", "rb"),
                        mime="application/pdf",
                        file_name="merged.pdf",
                        use_container_width=True,
                    )
       
        # with st.expander("➕ Merge PDFs"):
        #     st.caption("Select multiple PDFs to merge. Passwords will be removed from all.")
        #     pdfs_and_readers = utils.load_pdf(key="merge")

        #     col1, col2 = st.columns(2)

        #     if col1.button("➕ Merge PDFs", disabled=(not pdfs_and_readers), use_container_width=True):
        #         if pdfs_and_readers:
        #             with PdfWriter() as merger:
        #                 for _, reader in pdfs_and_readers:
        #                     merger.append(reader)

        #                 # TODO: Write to byte_stream
        #                 merger.write("merged.pdf")

        #                 with col2:
        #                     pdf_viewer(
        #                         open("merged.pdf", "rb").read(),
        #                         height=250,
        #                         width=300,
        #                     )
        #                 st.download_button(
        #                     "⬇️ Download merged PDF",
        #                     data=open("merged.pdf", "rb"),
        #                     mime="application/pdf",
        #                     file_name="merged.pdf",
        #                     use_container_width=True,
        #                 )
        #         else:
        #             st.error("No PDFs to merge.", icon="❌")

        with st.expander("🤏 Reduce PDF size"):
            # TODO: Add password back to converted PDF if original was protected
            st.caption("Will remove password if present")

            pdf_small = pdf

            lcol, mcol, rcol = st.columns(3)

            with lcol:
                remove_duplication = st.checkbox(
                    "Remove duplication",
                    help="""
                    Some PDF documents contain the same object multiple times.  
                    For example, if an image appears three times in a PDF it could be embedded three times. 
                    Or it can be embedded once and referenced twice.  
                    **Note:** This option will not remove objects, rather it will use a reference to the original object for subsequent uses.
                    """,
                )

                remove_images = st.checkbox(
                    "Remove images",
                    help="Remove images from the PDF. Will also remove duplication.",
                )

                if remove_images or remove_duplication:
                    pdf_small = utils.remove_images(
                        pdf,
                        remove_images=remove_images,
                        password=session_state.password,
                    )

                if st.checkbox(
                    "Reduce image quality",
                    help="""
                    Reduce the quality of images in the PDF. Will also remove duplication.  
                    May not work for all cases.
                    """,
                    disabled=remove_images,
                ):
                    quality = st.slider(
                        "Quality",
                        min_value=0,
                        max_value=100,
                        value=50,
                        disabled=remove_images,
                    )
                    pdf_small = utils.reduce_image_quality(
                        pdf_small,
                        quality,
                        password=session_state.password,
                    )

                if st.checkbox(
                    "Lossless compression",
                    help="Compress PDF without losing quality",
                ):
                    pdf_small = utils.compress_pdf(
                        pdf_small, password=session_state.password
                    )

                original_size = sys.getsizeof(pdf)
                reduced_size = sys.getsizeof(pdf_small)
                st.caption(
                    f"Reduction: {100 - (reduced_size / original_size) * 100:.2f}%"
                )

            with mcol:
                st.caption(f"Original size: {original_size / 1024:.2f} KB")
                utils.preview_pdf(
                    reader,
                    pdf,
                    key="other",
                    password=session_state.password,
                )
            with rcol:
                st.caption(f"Reduced size: {reduced_size / 1024:.2f} KB")
                utils.preview_pdf(
                    PdfReader(BytesIO(pdf_small)),
                    pdf_small,
                    key="other",
                    password=session_state.password,
                )
            st.download_button(
                "⬇️ Download smaller PDF",
                data=pdf_small,
                mime="application/pdf",
                file_name=f"{filename}_reduced.pdf",
                use_container_width=True,
            )
    else:
        st.info("👈 Upload a PDF to start")

except Exception as e:
    st.error(
        f"""The app has encountered an error:  
        `{e}` """,
        icon="🥺",
    )
    st.code(traceback.format_exc())

