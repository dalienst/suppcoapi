# Frontend Developer Guide: Cart & Checkout

## Overview
Recent updates to the Cart and Checkout flow introduce new fields for better transparency on costs, interest, and payment flexibility.

## 1. Cart Item Structure
The `CartItem` object now distinguishes between the **Total Value** of the goods and what is **Payable Now**.

```json
{
    "product_name": "NRB Sand",
    "quantity": 100,
    "sub_total": 300000.00,       // (Price * Quantity) - The Cash Value of goods
    "payable_amount": 60000.00,   // The amount due NOW (Deposit for Flexible, Full for Fixed)
    "total_interest": 15000.00,   // The Cost of Credit (if Flexible). 0 for Fixed.
    "payment_option": "REF_123",  // Reference to selected option
    "deposit_amount": 60000.00,   // User/System defined deposit
    "duration_months": 6,         // Duration (if applicable)
    "monthly_amount": 42500.00,   // Monthly installment (calculated or defined)
    "payment_option_details": {   // Expanded details for UI
        "payment_type": "FLEXIBLE",
        "min_deposit_percentage": 20.00,
        "interest_rate": 10.00    // Annual Interest Rate %
    },
    "projections": [              // Installment Plan Preview
        { "due_date": "2026-02-10", "amount": 60000.00, "description": "Deposit", "status": "PENDING" },
        { "due_date": "2026-03-10", "amount": 42500.00, "description": "Installment 1/6", "status": "PENDING" }
    ]
}
```

### Key Fields to Display
1.  **Sub Total**: Display this as the "Item Value" or "Cash Price".
2.  **Payable Amount**: Display this as "Due Today" or "Checkout Price".
3.  **Total Interest**: Display this if > 0, labeled as "Interest" or "Credit Cost".

## 2. Cart Totals
The `Cart` object summarizes these values:

```json
{
    "total_amount": 500000.00,   // Sum of all Item Sub Totals (Total Cart Value)
    "total_payable": 120000.00   // Sum of all Payable Amounts (Total Due Now)
}
```
*   **Checkout Button** should reflect `total_payable`.

## 3. Flexible Payment Inputs
For Flexible Payment Options, the user can now specify **EITHER**:
1.  **Duration** (`duration_months`): "I want to pay over 6 months."
    *   System calculates `monthly_amount` based on interest.
2.  **Monthly Amount** (`monthly_amount`): "I can afford 50,000 per month."
    *   System calculates `duration_months` based on interest.

### Interest Calculation
*   Interest is calculated as **Simple Interest on the Remaining Principal**.
*   Formula: `Interest = (Principal - Deposit) * (Rate/100) * (Months/12)`
*   The `payment_option_details.interest_rate` field (default 0.00) drives this.

## 4. Checkout Payload
When submitting to `/api/v1/orders/checkout/`:

```json
{
    "items": [
        {
            "product": "PROD_REF",
            "quantity": 100,
            "payment_plan": {
                "payment_option": "OPT_REF",
                "deposit_amount": 60000,
                "duration_months": 6,       // Optional if monthly_amount is provided
                "monthly_amount": 42500     // Optional if duration_months is provided
            }
        }
    ]
}
```
*   **Note**: `duration_months` and `monthly_amount` are now mutually exclusive optional fields (though providing both is valid, one usually drives the other). The serializer handles `null` values gracefully.
