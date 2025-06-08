import pandas as pd
import streamlit as st
from components.render_debt_row import render_debt_row
from calculations import calculate_monthly_interest, simulate_daily_interest
from state import init_session_state

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

init_session_state

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

with st.container():

    if st.button("Add Debt"):
        st.session_state.totalDebts += 1

    if st.button("Remove Debt"):
        if st.session_state.totalDebts > 1: 
            st.session_state.totalDebts -= 1

debts = []
for i in range(1, st.session_state.totalDebts + 1):
    debt_data = render_debt_row(i, col1, col2, col3, col4, col5)
    debts.append(debt_data)

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