def simulate_monthly_interest(principal, annual_rate, monthly_payment, max_months = 360):
    data = []
    r_monthly = annual_rate / 100 / 12
    balance = principal
    total_paid = 0.0
    total_interest = 0.0
    months = 0

    while balance > 0 and months < max_months:
        interest_this_month = balance * r_monthly
        balance += interest_this_month
        payment = min(monthly_payment, balance)
        balance -= payment
        total_paid += payment
        total_interest += interest_this_month
        months += 1

        if payment <= interest_this_month:
            raise ValueError("Monthly payment too low to cover accrued interest.")
        
        row = {
            "Month": months,
            "Payment": round(payment, 2),
            "Interest": round(interest_this_month, 2),
            "Principal": round(payment, 2) - round(interest_this_month, 2),
            "Balance": round(balance, 2)
        }

        data.append(row)

    return data

def simulate_daily_interest(principal, annual_rate, monthly_payment, max_months = 360):
    data = []
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

    row = {
        "Month": months,
        "Payment": round(payment, 2),
        "Interest": round(interest_this_month, 2),
        "Principal": round(payment, 2) - round(interest_this_month, 2),
        "Balance": round(balance, 2)
    }

    data.append(row)

    return data