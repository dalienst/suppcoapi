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


def calculate_flexible_plan(total_amount, deposit_amount, months):
    """
    Generates a deposit entry and 'months' number of equal installments.
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

    remaining_amount = total_amount - deposit_amount

    if months > 0 and remaining_amount > 0:
        monthly_installment = remaining_amount / Decimal(str(months))
        # Handle potential rounding issues by making the last payment the remainder
        running_total = Decimal("0.00")

        for i in range(1, months + 1):
            is_last = i == months
            due_date = date.today() + relativedelta(months=i)

            if is_last:
                amount = remaining_amount - running_total
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


def calculate_flexible_plan_by_amount(total_amount, deposit_amount, monthly_amount):
    """
    Generates a deposit entry and installments based on a fixed monthly amount.
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

    remaining_amount = total_amount - deposit_amount

    if monthly_amount > 0 and remaining_amount > 0:
        # Calculate number of months needed
        import math

        months = math.ceil(remaining_amount / monthly_amount)

        running_total = Decimal("0.00")

        for i in range(1, months + 1):
            is_last = i == months
            due_date = date.today() + relativedelta(months=i)

            if is_last:
                amount = remaining_amount - running_total
            else:
                amount = monthly_amount

            # safeguard against overpayment in loop logic, though ceil handles count
            if amount <= 0:
                break

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
