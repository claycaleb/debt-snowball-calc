import pandas as pd
import streamlit as st
from components.render_debt_row import render_debt_row
from state import init_session_state, reset_session_state_values
from payoff import process_debts

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

init_session_state()

# HEADER
with st.container():
    st.header("Debt Snowball Calculator")

# SLIDER
with st.container():
    st.text("Extra Monthly Payment")
    extra_payment_amt = st.slider("Extra Monthly Payment", 0, 1000, key="extraPaymentAmt", label_visibility="collapsed")

# COLUMN HEADERS
with st.container():

    cols = st.columns(5)

    labels = ["Account Name", "Type of Debt", "Current Balance", "Minimum Payment", "Interest Rate"]

    for col, label in zip(cols, labels):
        with col:
            st.text(label)

# ADD/REMOVE DEBT BUTTONS
with st.container():

    if st.button("Add Debt"):
        st.session_state.totalDebts += 1

    if st.button("Remove Debt"):
        if st.session_state.totalDebts > 1: 
            st.session_state.totalDebts -= 1

debts = []
for i in range(1, st.session_state.totalDebts + 1):
    debt_data = render_debt_row(i, cols)
    debts.append(debt_data)

reset_session_state_values()

sorted_debts = sorted(debts, key=lambda x: x["balance"])

# CALCULATE BUTTON
with st.container():
    if st.button("Calculate"):
        process_debts(sorted_debts, extra_payment_amt)

st.session_state.debtSnowballAmt
st.session_state.totalMonths
st.session_state.totalInterest
st.session_state.totalPaid