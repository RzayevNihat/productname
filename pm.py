import streamlit as st
import pandas as pd

# Load the CSV data
data_path = "products.csv"  # Replace with your actual CSV file path
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error(f"Error: CSV file '{data_path}' not found. Please create it or update the path.")
    df = pd.DataFrame(columns=["Product Name", "Product Category", "Price", "Count"])

# Function to update the product data
def update_product_data(product_name, product_category, price, count):
    global df  # Access the global DataFrame for modification

    if "Product Name" in df.columns and product_name in df["Product Name"].values:
        index = df.index[df["Product Name"] == product_name].tolist()[0]
        df.loc[index] = [product_name, product_category, price, count]
        st.success(f"Product '{product_name}' successfully updated.")
    else:
        new_product = pd.DataFrame(
            [[product_name, product_category, price, count]],
            columns=["Product Name", "Product Category", "Price", "Count"]
        )
        df = pd.concat([df, new_product], ignore_index=True)
        st.success(f"Product '{product_name}' added successfully.")

# Streamlit app layout and functionality
st.title("Product Management App")

# Add new product section
st.header("Add New Product")

# Split the layout into two columns
col1, col2 = st.columns(2)

# Add input elements to the first column
with col1:
    new_product_name = st.text_input("Product Name")

# Add input elements to the second column
with col2:
    new_product_category = st.text_input("Product Category")

# Split the layout into two columns
col3, col4 = st.columns(2)

# Add input elements to the third column
with col3:
    new_product_price = st.number_input("Price", min_value=0.0)

# Add input elements to the fourth column
with col4:
    new_product_count = st.number_input("Count", min_value=0)

if st.button("Add Product"):
    update_product_data(new_product_name, new_product_category, new_product_price, new_product_count)
    # Save the updated data back to the CSV file
    df.to_csv(data_path, index=False)

# Sidebar for displaying product data
st.sidebar.header("Product Data")
table_placeholder = st.sidebar.empty()
table_placeholder.table(df)

# Edit/Delete product section (optional)
selected_product = st.selectbox("Select Product", df["Product Name"] if "Product Name" in df.columns else [])

if selected_product:
    selected_product_data = df[df["Product Name"] == selected_product]
    st.header(f"Edit Product: {selected_product}")
    
    # Split the layout into two columns
    col1, col2 = st.columns(2)

    # Add input elements to the first column
    with col1:
        edit_product_name = st.text_input("Product Name", selected_product_data["Product Name"].values[0])

    # Add input elements to the second column
    with col2:
        edit_product_category = st.selectbox(
            "Product Category", df["Product Category"].unique(), 
            index=list(df["Product Category"].unique()).index(selected_product_data["Product Category"].values[0])
        )

    # Split the layout into two columns
    col3, col4 = st.columns(2)

    # Add input elements to the third column
    with col3:
        edit_product_price = st.number_input(
            "Price", min_value=0.0, value=selected_product_data["Price"].values[0]
        )

    # Add input elements to the fourth column
    with col4:
        edit_product_count = st.number_input(
            "Count", min_value=0, value=selected_product_data["Count"].values[0]
        )
    
    if st.button("Update Product"):
        update
