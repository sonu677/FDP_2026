import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = {"Region", "Product", "Sales"}

        if not required_columns.issubset(df.columns):
            st.error("CSV must contain Region, Product, and Sales columns")
            st.stop()

        st.subheader("Raw Data")
        st.dataframe(df, use_container_width=True)

        # Sidebar Filters
        st.sidebar.header("Filters")

        region_filter = st.sidebar.multiselect(
            "Select Region",
            options=df["Region"].dropna().unique(),
            default=df["Region"].dropna().unique()
        )

        product_filter = st.sidebar.multiselect(
            "Select Product",
            options=df["Product"].dropna().unique(),
            default=df["Product"].dropna().unique()
        )

        # Apply Filters
        filtered_df = df[
            (df["Region"].isin(region_filter)) &
            (df["Product"].isin(product_filter))
        ]

        st.subheader("Filtered Data")
        st.dataframe(filtered_df, use_container_width=True)

        col1, col2 = st.columns(2)

        # Sales by Region
        with col1:
            st.subheader("Sales by Region")
            region_sales = filtered_df.groupby("Region")["Sales"].sum()

            fig1, ax1 = plt.subplots()
            region_sales.plot(kind="bar", ax=ax1)
            ax1.set_ylabel("Total Sales")
            ax1.set_title("Region-wise Sales")
            st.pyplot(fig1)

        # Sales by Product
        with col2:
            st.subheader("Sales by Product")
            product_sales = filtered_df.groupby("Product")["Sales"].sum()

            fig2, ax2 = plt.subplots()
            product_sales.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
            ax2.set_ylabel("")
            ax2.set_title("Product-wise Sales Distribution")
            st.pyplot(fig2)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("Please upload a CSV file to continue.")