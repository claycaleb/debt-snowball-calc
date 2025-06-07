import pandas as pd
import streamlit as st
import math

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

st.header("Debt Snowball Calculator")

with st.container():
    st.text("Extra Monthly Payment")
    extra_payment_amt = st.slider("Extra Monthly Payment", 0, 1000, key="extraPaymentAmt", label_visibility="collapsed")

with st.container():

    # Initialize columns and text
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text("Account Name")
    with col2:
        st.text("Type of Debt")
    with col3:
        st.text("Current Balance")
    with col4:
        st.text("Minimum Payment")
    with col5:
        st.text("Interest Rate")

if "totalDebts" not in st.session_state:
    st.session_state.totalDebts = 1

def render_debt_row(index):
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

with st.container():
    ncol1, ncol2, ncol3 = st.columns([0.79, 0.09, 0.12])

    with ncol2:
        if st.button("Add Debt"):
            st.session_state.totalDebts += 1

    with ncol3:
        if st.button("Remove Debt"):
            if st.session_state.totalDebts > 1: 
                st.session_state.totalDebts -= 1

debts = []
for i in range(1, st.session_state.totalDebts + 1):
    debt_data = render_debt_row(i)
    debts.append(debt_data)

def calculate_monthly_interest(principal, annual_rate, monthly_payment):
    rate = annual_rate / 100 / 12

    if monthly_payment <= principal * rate:
        raise ValueError("Monthly payment is too low to ever pay off the loan.")

    numerator = monthly_payment / (monthly_payment - principal * rate)
    n = math.log(numerator) / math.log(1 + rate)
    total_paid = monthly_payment * n
    total_interest = total_paid - principal

    return {
        "months": round(n, 0),
        "total_interest": round(total_interest, 2),
        "total_paid": round(total_paid, 2)
    }

def simulate_daily_interest(principal, annual_rate, monthly_payment, max_months = 600):
    r_daily = annual_rate / 100 / 365
    balance = principal
    total_paid = 0.0
    total_interest = 0.0
    months = 0

    while balance > 0 and months < max_months:
        interest_this_month = 0.0

        for _ in range(30):
            interest_today = balance * r_daily
            balance += interest_today
            interest_this_month += interest_today

        payment = min(monthly_payment, balance)
        balance -= payment
        total_paid += payment
        total_interest += interest_this_month
        months += 1

        if payment <= interest_this_month:
            raise ValueError("Monthly payment too low to cover accrued interest.")

    return {
        "months": months,
        "total_interest": round(total_interest, 2),
        "total_paid": round(total_paid, 2)
    }

if "debtSnowballAmt" not in st.session_state:
    st.session_state.debtSnowballAmt = 0

if "totalMonths" not in st.session_state:
    st.session_state.totalMonths = 0

if "totalInterest" not in st.session_state:
    st.session_state.totalInterest = 0

if "totalPaid" not in st.session_state:
    st.session_state.totalPaid = 0

st.session_state.debtSnowballAmt = 0
st.session_state.totalMonths = 0
st.session_state.totalInterest = 0
st.session_state.totalPaid = 0

sorted_debts = sorted(debts, key=lambda x: x["balance"])

for i in range(len(sorted_debts)):
    balance = sorted_debts[i]["balance"]
    payment = sorted_debts[i]["min_payment"] + st.session_state.debtSnowballAmt + extra_payment_amt
    rate = sorted_debts[i]["interest_rate"]
    compounding = sorted_debts[i]["compounding"]
    if balance and payment and rate: 
        if compounding == "monthly":
            result = calculate_monthly_interest(balance, rate, payment)
        elif compounding == "daily":
            result = simulate_daily_interest(balance, rate, payment)
        st.write(sorted_debts[i])
        st.write(result)
        st.session_state.debtSnowballAmt += sorted_debts[i]["min_payment"]
        st.session_state.totalMonths += result["months"]
        st.session_state.totalInterest += result["total_interest"]
        st.session_state.totalPaid += result["total_paid"]

st.session_state.debtSnowballAmt
st.session_state.totalMonths
st.session_state.totalInterest
st.session_state.totalPaid


# reorder based on interest rate or balance checkbox/switch?
# needs to simulate payoff with extra payment amount + minimum payment from paid off debt