import math

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