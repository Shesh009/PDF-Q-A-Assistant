import streamlit as st
import requests

st.set_page_config(page_title="PDF Q&A Assistant")
st.title("PDF Q&A Assiatant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

uploaded_file = st.file_uploader("Upload a PDF to begin chatting", type=["pdf", "txt"])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask something about the PDF...")

if query:
    if not st.session_state.pdf_uploaded and not uploaded_file:
        with st.chat_message("assistant"):
            st.error("Please upload a PDF before starting the conversation.")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                send_pdf = False
                if not st.session_state.pdf_uploaded and uploaded_file:
                    send_pdf = True
                    st.session_state.pdf_uploaded = True

                data = {
                    "query": query,
                    "reset_collection": str(send_pdf).lower()
                }

                files = {"file": uploaded_file} if send_pdf else None

                try:
                    response = requests.post(
                        "http://localhost:5001/upload-pdf",
                        data=data,
                        files=files
                    )
                    if response.status_code == 200:
                        result = response.json().get("result", "No result returned.")
                        st.markdown(result)
                        st.session_state.messages.append({"role": "assistant", "content": result})
                    else:
                        error_msg = response.json().get("error", "Unknown error occurred.")
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                except Exception as e:
                    error_msg = f"Connection failed: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
