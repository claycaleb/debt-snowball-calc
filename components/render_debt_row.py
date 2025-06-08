import streamlit as st

def render_debt_row(index, col1, col2, col3, col4, col5):
    with st.container():

        with col1:
            account_name = st.text_input("Account Name", key=f"acctName{index}", label_visibility="collapsed")

        with col2:
            debt_type = st.selectbox("Type of Debt", ("Credit Card", "Auto Loan", "Personal Loan", "Student Loan", "Mortgage", "Line of Credit"), key=f"debtType{index}", label_visibility="collapsed")

        with col3:
            balance = st.number_input("Current Balance", format="%.2f", key=f"currentBal{index}", min_value=0.00, value=None, label_visibility="collapsed", placeholder="$")

        with col4:
            min_payment = st.number_input("Minimum Payment", format="%.2f", key=f"minPayment{index}", min_value=0.00, value=None, label_visibility="collapsed", placeholder="$")

        with col5:
            interest_rate = st.number_input("Interest Rate", format="%.2f", key=f"intRate{index}", min_value=0.00, value=None, label_visibility="collapsed", placeholder="%")

    compounding_lookup = {
        "Credit Card": "daily",
        "Line of Credit": "daily",
        "Student Loan": "daily",
        "Auto Loan": "monthly",
        "Personal Loan": "monthly",
        "Mortgage": "monthly"
    }

    return {
        "index": index,
        "account_name": account_name,
        "debt_type": debt_type,
        "compounding": compounding_lookup.get(debt_type, "monthly"),
        "balance": balance,
        "min_payment": min_payment,
        "interest_rate": interest_rate
    }