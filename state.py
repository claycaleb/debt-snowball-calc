import streamlit as st

DEFAULTS = {
    "totalDebts": 1,
    "totalMonths": 0,
    "totalInterest": 0.0,
    "totalPaid": 0.0,
    "debtSnowballAmt": 0.0
}

def init_session_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_session_state_values():
    st.session_state.totalMonths = 0
    st.session_state.totalInterest = 0
    st.session_state.totalPaid = 0
    st.session_state.debtSnowballAmt = 0