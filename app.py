import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fee Management System")

st.title("💳 Fee Payment & Tracking System")

# Function to load data
def load_data():
    return pd.read_csv('Fees.csv')

# Function to save data
def save_data(dataframe):
    dataframe.to_csv('Fees.csv', index=False)

try:
    df = load_data()

    # --- SECTION 1: SEARCH ---
    st.header("1. Check Status")
    search_sl = st.number_input("Enter SL NO to search:", min_value=1, step=1, key="search")
    
    if st.button("Search"):
        record = df[df['SL NO'] == search_sl]
        if not record.empty:
            st.dataframe(record)
        else:
            st.error("Record not found.")

    st.divider()

    # --- SECTION 2: SUBMIT PAYMENT ---
    st.header("2. Submit New Payment")
    
    with st.form("payment_form"):
        update_sl = st.number_input("Enter SL NO for Payment:", min_value=1, step=1)
        new_payment = st.number_input("Enter Amount Paid Today:", min_value=0.0, step=100.0)
        submit_button = st.form_submit_button("Submit Payment & Update Database")

    if submit_button:
        # Check if record exists
        if update_sl in df['SL NO'].values:
            # Find the index of the row
            idx = df.index[df['SL NO'] == update_sl].tolist()[0]
            
            # Update values
            current_paid = df.at[idx, 'Paid']
            total_fees = df.at[idx, 'Fees']
            
            new_total_paid = current_paid + new_payment
            new_due = total_fees - new_total_paid
            
            if new_due < 0:
                st.error(f"Error: Payment exceeds total fees! Remaining due is only ₹{total_fees - current_paid}")
            else:
                # Apply changes to DataFrame
                df.at[idx, 'Paid'] = new_total_paid
                df.at[idx, 'Due'] = new_due
                
                # Save back to CSV
                save_data(df)
                
                st.success(f"Successfully updated SL NO: {update_sl}")
                st.balloons()
                
                # Show updated record
                st.write("**Updated Record:**")
                st.table(df[df['SL NO'] == update_sl])
        else:
            st.error("Invalid Serial Number. No record updated.")

    # --- SECTION 3: FULL DATABASE VIEW ---
    with st.expander("View Full Database"):
        st.write(df)

except FileNotFoundError:
    st.error("Please ensure 'Fees.csv' is in the same folder as this script.")
