import pandas as pd
import streamlit as st
from pandasql import sqldf

st.title("Run SQL Query on Dataset")

option = st.radio("Select Data Source:", ["Upload File", "From Google Sheet"])

DataTable = None


if option == "Upload File":
    uploaded_file = st.file_uploader("Upload CSV / Excel / JSON", type=["csv", "xlsx", "json"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith("csv"):
                DataTable = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith("xlsx"):
                DataTable = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith("json"):
                DataTable = pd.read_json(uploaded_file)

        except Exception as e:
            st.error(f"Error loading file: {e}")

elif option == "From Google Sheet":
    fileID = st.text_input("Enter fileID (Google Sheets)")
    url=(f"https://docs.google.com/spreadsheets/d/{fileID}/export?format=csv&gid=0")

    if url is not None:
        try:
            DataTable = pd.read_csv(url)

        except Exception as e:
            st.error(f"Error loading URL: {e}")

if DataTable is not None:
    st.subheader("Preview Data")
    st.dataframe(DataTable.head())

    query = st.text_input("Enter SQL query")

    if query:
        try:
            result = sqldf(query)
            st.subheader("Result")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Query error: {e}")
