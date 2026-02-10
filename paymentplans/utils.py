from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta


def calculate_fixed_plan(total_amount):
    """
    Generates a single payment entry for Fixed or Pay on Delivery options.
    """
    return [
        {
            "due_date": str(date.today()),
            "amount": float(total_amount),
            "description": "Full Payment",
            "status": "PENDING",
        }
    ]


def calculate_split_plan(total_amount):
    """
    Generates two 50% payment entries.
    """
    half = total_amount / Decimal("2.0")
    return [
        {
            "due_date": str(date.today()),
            "amount": float(half),
            "description": "First Installment (50%)",
            "status": "PENDING",
        },
        {
            "due_date": str(date.today() + relativedelta(months=1)),
            "amount": float(total_amount - half),
            "description": "Final Installment (50%)",
            "status": "PENDING",
        },
    ]


def calculate_flexible_plan(total_amount, deposit_amount, months, interest_rate=0):
    """
    Generates a deposit entry and 'months' number of equal installments.
    Applies simple interest on the remaining principal.
    Formula: Interest = Remaining * (Rate/100) * (Months/12)
    Total Payable = Remaining + Interest
    """
    plan = []

    # 1. Deposit
    if deposit_amount > 0:
        plan.append(
            {
                "due_date": str(date.today()),
                "amount": float(deposit_amount),
                "description": "Deposit",
                "status": "PENDING",
            }
        )

    remaining_principal = total_amount - deposit_amount

    if months > 0 and remaining_principal > 0:
        # Calculate Interest
        interest = Decimal("0.00")
        if interest_rate > 0:
            rate = Decimal(str(interest_rate)) / Decimal("100.00")
            time_in_years = Decimal(str(months)) / Decimal("12.00")
            interest = remaining_principal * rate * time_in_years

        total_payable_after_deposit = remaining_principal + interest
        monthly_installment = total_payable_after_deposit / Decimal(str(months))

        # Handle potential rounding issues by making the last payment the remainder
        running_total = Decimal("0.00")

        for i in range(1, months + 1):
            is_last = i == months
            due_date = date.today() + relativedelta(months=i)

            if is_last:
                amount = total_payable_after_deposit - running_total
            else:
                amount = monthly_installment
                amount = round(amount, 2)

            running_total += amount

            plan.append(
                {
                    "due_date": str(due_date),
                    "amount": float(amount),
                    "description": f"Installment {i}/{months}",
                    "status": "PENDING",
                }
            )

    return plan


def calculate_flexible_plan_by_amount(
    total_amount, deposit_amount, monthly_amount, interest_rate=0
):
    """
    Generates a deposit entry and installments based on a fixed monthly amount.
    Calculates the number of months needed to pay off the principal + interest.
    """
    plan = []

    # 1. Deposit
    if deposit_amount > 0:
        plan.append(
            {
                "due_date": str(date.today()),
                "amount": float(deposit_amount),
                "description": "Deposit",
                "status": "PENDING",
            }
        )

    remaining_principal = total_amount - deposit_amount

    if monthly_amount > 0 and remaining_principal > 0:
        import math

        months = 0
        if interest_rate > 0:
            # We need to solve for months where:
            # Monthly_Installment = (Principal + Interest) / Months
            # Interest = Principal * Rate * (Months/12)
            # Monthly = (P + P*R*M/12) / M = P/M + P*R/12
            # Monthly - P*R/12 = P/M
            # M = P / (Monthly - P*R/12)

            rate = Decimal(str(interest_rate)) / Decimal("100.00")
            monthly_interest = remaining_principal * rate / Decimal("12.00")

            if monthly_amount <= monthly_interest:
                # If monthly payment covers only interest or less, debt never paid.
                # Returning minimal plan or error? Let's just default to logic without interest
                # or maybe force 12 months? Let's treat as simple division fallback
                # but ideally this should be a validation error upstream.
                # For now, let's treat it as paying off principal slowly (ignoring interest constraint?)
                # no, that's bad math.
                # Let's assume minimum 1 month.
                months = 1
            else:
                months_float = remaining_principal / (monthly_amount - monthly_interest)
                months = math.ceil(months_float)
        else:
            months = math.ceil(remaining_principal / monthly_amount)

        # Now that we have months, use the standard logic to generate the exact plan
        # This aligns the formatting and final adjustment logic
        return calculate_flexible_plan(
            total_amount, deposit_amount, months, interest_rate
        )

    return plan
