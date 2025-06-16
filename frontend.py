import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.title(" Legal Document Q&A Assistant")

st.write("Ask questions based on processed legal PDFs.")

question = st.text_input(" Enter your question:")

if st.button("Get Answer"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.success("Answer:")
                    st.write(answer)
                else:
                    st.error(f" Error: {response.status_code} {response.text}")
            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")

st.write("----")
st.write(" Status: Connected to FastAPI backend at `http://localhost:8000`")
