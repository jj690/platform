import requests
import streamlit as st
import pandas as pd
from datahandler import DataHandler

data_handler = DataHandler()

with st.sidebar:
    st.text_input("Search by Company Name", key="search_company")
    st.text_input("Search by Update", key="update_type")
    edit = st.checkbox("Edit Mode")
    if edit:
        age = None  # Disable age filter in edit mode
    else:
        age = st.slider("Maximum age of emails (days)", min_value=0, max_value=365, value=30, key="max_age")

st.title("Email Database")

df = data_handler.fetch_database(search_company=st.session_state.get("search_company"), update_type=st.session_state.get("update_type"), max_age=age)


if edit:    
    st.write("Edit mode is enabled. You can modify the database entries.")
    file = st.file_uploader("Upload CSV", type=["csv"], key="csv_upload")
    if file is not None:
        df = pd.read_csv(file,index_col=0)

    df = st.data_editor(df, num_rows="dynamic")

    if st.button("Save Changes"):
        data_handler.save_changes(df)
else:
    st.write("Edit mode is disabled. You can only view the database entries.")
    st.dataframe(df)

if st.button("Refresh"):
    st.rerun()
st.write("Total Emails:", len(df))

fig = data_handler.create_scatter_plot(df)
st.plotly_chart(fig, width="stretch")

# metrics
cols = st.columns(2)
cols[0].metric("Emails", f"{len(df)}",)
cols[1].metric("Companies", f"{len(df['company_name'].unique())}")

