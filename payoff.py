import streamlit as st
from calculations import calculate_monthly_interest, simulate_daily_interest
from components.render_debt_row import render_debt_row

def prepare_debts(cols):
    debts = []
    for i in range(1, st.session_state.totalDebts + 1):
        debt_data = render_debt_row(i, cols)
        debts.append(debt_data)
    
    sorted_debts = sorted(debts, key=lambda x: x["balance"])
    return sorted_debts

def process_debts(sorted_debts, extra_payment_amt):
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