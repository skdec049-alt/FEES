import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="Fee Inquiry System")

st.title("💰 Fee Due Status Checker")
st.write("Enter the Serial Number below to check the pending balance.")

# Load the data from the CSV file
@st.cache_data
def load_data():
    return pd.read_csv('Fees.csv')

try:
    df = load_data()

    # Input field for Serial Number
    sl_input = st.number_input("Enter SL NO:", min_value=int(df['SL NO'].min()), step=1)

    if st.button("Check Due Amount"):
        # Filter the dataframe
        row = df[df['SL NO'] == sl_input]
        
        if not row.empty:
            due_amount = row['Due'].values[0]
            paid_amount = row['Paid'].values[0]
            total_fees = row['Fees'].values[0]
            
            # Display results in a nice format
            st.info(f"**Results for SL NO: {sl_input}**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Fees", f"₹{total_fees}")
            col2.metric("Paid", f"₹{paid_amount}")
            col3.metric("Due", f"₹{due_amount}", delta_color="inverse")
            
            if due_amount == 0:
                st.success("All fees are paid!")
            else:
                st.warning(f"Remaining balance to be paid: ₹{due_amount}")
        else:
            st.error(f"No record found for Serial Number {sl_input}.")

except FileNotFoundError:
    st.error("Error: 'Fees.csv' not found. Please ensure the file is in the same folder as this script.")
