import streamlit as st
import pandas as pd
import os
from PIL import Image

# Page settings
st.set_page_config(page_title="FC Naples Scouting Dashboard", layout="wide")

# Load and display FC Naples logo
logo = Image.open("FC_Naples_Logo.png")
st.image(logo, width=120)

# Title
st.title("FC Naples Scouting Dashboard")

# Load Excel files from current directory
leagues_folder = "."
excel_files = [
    f for f in os.listdir(leagues_folder)
    if f.endswith(".xlsx") and not f.startswith(("~$", "."))
]

# Select season/tournament
selected_file = st.selectbox("Select Season / Tournament", sorted(excel_files))

if selected_file:
    file_path = os.path.join(leagues_folder, selected_file)
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    # Select position
    position = st.selectbox("Select Position (Sheet)", sheet_names)
    df = pd.read_excel(xls, sheet_name=position, header=5)

    # Columns to drop per position
    columns_to_drop = {
        "GK": ["Unnamed: 0", df.columns[15] if len(df.columns) > 15 else None],  # A, P
        "CB": ["Unnamed: 0", "AC", "AL", "BC"],
        "FB": ["Unnamed: 0", "AC", "AL", "BC"],
        "CM": ["Unnamed: 0", "AC", "AL", "BC"],
        "W":  ["Unnamed: 0", "AC", "AL", "BC"],
        "CF": ["Unnamed: 0", "AC", "AL", "BC"],
        "DM": ["Unnamed: 0", "AB", "AK", "BB"]
    }

    # Drop the columns if they exist
    drop_cols = columns_to_drop.get(position, [])
    drop_cols = [col for col in drop_cols if col in df.columns]
    df = df.drop(columns=drop_cols)

    # Capitalize headers
    df.columns = [str(col).strip().title() for col in df.columns]

    # Safe conditional formatting from 'R. Global' onward
    if "R. Global" in df.columns:
        try:
            r_index = df.columns.get_loc("R. Global")

            # Filter only numeric and valid columns
            numeric_cols = []
            for col in df.columns[r_index:]:
                if (
                    isinstance(col, str)
                    and col.strip() != ""
                    and pd.api.types.is_numeric_dtype(df[col])
                ):
                    numeric_cols.append(col)

            # If we found any numeric columns, apply formatting
            if numeric_cols:
                styled_df = df.style \
                    .format("{:.0f}", subset=numeric_cols) \
                    .background_gradient(
                        axis=0,
                        subset=numeric_cols,
                        cmap="RdYlGn",
                        vmin=0,
                        vmax=100
                    )
                st.subheader(f"Data for: {selected_file} → Position: {position}")
                st.dataframe(styled_df, use_container_width=True)
            else:
                st.subheader(f"Data for: {selected_file} → Position: {position}")
                st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.warning(f"Could not format some columns due to unexpected data: {e}")
            st.dataframe(df, use_container_width=True)

    else:
        st.subheader(f"Data for: {selected_file} → Position: {position}")
        st.dataframe(df, use_container_width=True)
