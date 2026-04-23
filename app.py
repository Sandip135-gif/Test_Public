import pandas as pd
import streamlit as st
from pandasql import sqldf

st.title("Run SQL")

path = st.text_input("path:")

if "xlsx" in path:
    DataTable = pd.read_excel(path)
elif "csv" in path:
    DataTable = pd.read_csv(path)
elif "json" in path:
    DataTable = pd.read_json(path)
else:
    st.write("file format not supported.")

query = st.text_input("query:")
df = sqldf(query)

st.write(df)