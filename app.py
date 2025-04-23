
import streamlit as st
import pandas as pd
import os
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder

# Page settings
st.set_page_config(page_title="FC Naples Scouting Dashboard", layout="wide")

# Load and display FC Naples logo
logo = Image.open("FC_Naples_Logo.png")
st.image(logo, width=120)

# Title
st.title("FC Naples Scouting Dashboard")

# Custom CSS for bold headers
st.markdown(
    """
    <style>
    .bold-header .ag-header-cell-label {
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load Excel files from current directory (for Streamlit Cloud)
leagues_folder = "."
excel_files = [
    f for f in os.listdir(leagues_folder)
    if f.endswith(".xlsx") and not f.startswith(("~$", "."))
]

# Select season/tournament (file)
selected_file = st.selectbox("Select Season / Tournament", sorted(excel_files))

if selected_file:
    file_path = os.path.join(leagues_folder, selected_file)

    # Load Excel file and get sheet names
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    # Select position (sheet)
    position = st.selectbox("Select Position (Sheet)", sheet_names)

    # Load sheet, skipping first 5 rows and using 6th as header
    df = pd.read_excel(xls, sheet_name=position, header=5)

    # Columns to hide per position
    columns_to_drop = {
        "GK": ["Unnamed: 0", df.columns[15] if len(df.columns) > 15 else None],  # A, P
        "CB": ["Unnamed: 0", "AC", "AL", "BC"],
        "FB": ["Unnamed: 0", "AC", "AL", "BC"],
        "CM": ["Unnamed: 0", "AC", "AL", "BC"],
        "W":  ["Unnamed: 0", "AC", "AL", "BC"],
        "CF": ["Unnamed: 0", "AC", "AL", "BC"],
        "DM": ["Unnamed: 0", "AB", "AK", "BB"]
    }

    # Drop columns safely
    drop_cols = columns_to_drop.get(position, [])
    drop_cols = [col for col in drop_cols if col in df.columns]
    df = df.drop(columns=drop_cols)

    # Capitalize and clean column headers
    df.columns = [str(col).strip().title() for col in df.columns]

    # Configure AG Grid with frozen columns and bold headers
    gb = GridOptionsBuilder.from_dataframe(df)

    for col in ["Name", "Team"]:
        if col in df.columns:
            gb.configure_column(col, pinned='left')

    gb.configure_grid_options(headerHeight=40)
    gb.configure_default_column(headerClass='bold-header')

    grid_options = gb.build()

    # Show the table
    st.subheader(f"Data for: {selected_file} → Position: {position}")
    AgGrid(
        df,
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        height=600,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False
    )
