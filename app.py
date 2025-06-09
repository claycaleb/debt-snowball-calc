import pandas as pd
import streamlit as st
from state import init_session_state, reset_session_state_values
from payoff import prepare_debts, process_debts

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

sorted_debts = prepare_debts(cols)

reset_session_state_values()

# CALCULATE BUTTON
with st.container():
    if st.button("Calculate"):
        process_debts(sorted_debts, extra_payment_amt)