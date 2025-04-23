import streamlit as st
import pandas as pd
import os

# Page settings
st.set_page_config(page_title="Soccer Scouting Dashboard", layout="wide")
st.title("📊 Soccer Scouting Dashboard")

# Step 1: Get all Excel files in the Leagues folder
leagues_folder = os.path.expanduser("~/Documents/Leagues")
excel_files = [f for f in os.listdir(leagues_folder) if f.endswith(".xlsx")]

# Step 2: Let user pick a season/tournament (file)
selected_file = st.selectbox("Select Season / Tournament", excel_files)

if selected_file:
    file_path = os.path.join(leagues_folder, selected_file)

    # Step 3: Load the Excel file
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    # Step 4: Let user pick position (sheet)
    position = st.selectbox("Select Position (Sheet)", sheet_names)

    # Step 5: Load data, skipping first 5 rows and using 6th as header
    df = pd.read_excel(xls, sheet_name=position, header=5)

    # Display the data
    st.subheader(f"📋 Data for: {selected_file} → Position: {position}")
    st.dataframe(df, use_container_width=True)

