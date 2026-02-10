# Order Management Flow

## Overview
The Order Management system allows Contractors to purchase products from Suppliers. Each product in an order allows for a specific **Payment Plan**, ensuring flexibility even within a single transaction.

## Core Concepts

### 1. Order
The `Order` represents the transaction container. It tracks:
- **User**: The Contractor placing the order.
- **Total Amount**: usage sum of all items.
- **Status**: Lifecycle state (e.g., `DRAFT`, `PLACED`, `COMPLETED`).

### 2. Order Item
The `OrderItem` links a specific **Product** to an **Order**. It is the unit of fulfillment.
- **Status**: Each item has its own status (e.g., `PENDING`, `DISPATCHED`), allowing partial deliveries from different suppliers.

### 3. Payment Plan
A **Payment Plan** is created *specifically* for each `OrderItem` at the moment of purchase. This defines how the contractor will pay for that specific item (e.g., "Fixed", "Flexible with 20% deposit").

---

## Order Workflow

1.  **Selection**: Contractor selects Products.
2.  **Configuration**: For each Product, the Contractor chooses a **Payment Option** (provided by the Supplier) and configures a **Payment Plan** (e.g. setting terms for flexible payments).
3.  **Checkout**:
    - The client sends a **single POST request** to `/api/v1/orders/`.
    - This request contains the list of items.
    - Each item payload includes the `product` reference and the `payment_plan` configuration.
4.  **Creation**:
    - The system creates the `Order`.
    - It iterates through items, creating `PaymentPlan` records first, then `OrderItem` records linking everything together.
    - Total amount is calculated and saved.

5.  **Fulfillment (Supplier Side)**:
    -   Suppliers access `/api/v1/supplier-orders/` to see orders assigned to their company.
    -   Suppliers can update the status of the Order (e.g., to `DISPATCHED`).


---

## API Endpoints

### Orders
**Base URL**: `api/v1/orders/`

| Endpoint | Method | View | Description |
|----------|--------|------|-------------|
|`/` | GET | `OrderListCreateView` | List own orders |
|`/` | POST | `OrderListCreateView` | Create a new order with items |
|`/<reference>/`| GET | `OrderRetrieveUpdateDestroyView` | Get order details |
|`/<reference>/`| PATCH | `OrderRetrieveUpdateDestroyView` | Update order (e.g. cancel) |

#### Create Order Payload Example
```json
{
  "items": [
    {
      "product": "PROD_REF_123",
      "quantity": 10,
      "payment_plan": {
        "payment_option": "OPT_REF_456",
        "amount": 1000.00,
        "plan": {
          "notes": "Paying 50% now"
        }
      }
    }
  ]
}
```

### Order Items
**Base URL**: `api/v1/orderitems/`

| Endpoint | Method | View | Description |
|----------|--------|------|-------------|
|`/` | GET | `OrderItemListCreateView` | List items from own orders |
|`/<reference>/`| GET | `OrderItemRetrieveUpdateDestroyView` | Get details of a specific item |
