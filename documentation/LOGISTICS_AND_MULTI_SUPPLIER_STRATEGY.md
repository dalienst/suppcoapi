# Architectural Advisory: Multi-Supplier Checkout vs. Logistics Delivery Zones

This document provides a technical and operational analysis of checkout models in the SUPPCO B2B supply chain marketplace. It details how the platform should handle material purchases when a contractor's cart contains items from **multiple distinct suppliers**, especially given that each supplier configures their own bespoke `DeliveryZone` rates.

---

## 1. The Core Challenge
In bulk industrial B2B procurement, shipping is not a flat-rate operation. Unlike consumer e-commerce (where small packages are consolidated by a single courier like DHL), industrial materials (e.g., 500 bags of cement, 2 tons of steel, 50 sheets of drywall) require heavy flatbeds, specialized logistics, and separate dispatch trucks.

If a contractor adds items from **Supplier A** (Mombasa) and **Supplier B** (Nairobi) to the same cart:
* **Fulfillment Paths:** The items must originate from two different warehouses.
* **Logistics Costs:** If the contractor chooses "Supplier Managed Delivery", two separate delivery fees must be calculated, collected, and paid out.
* **Escrow Splits:** The total payment collected from the contractor must be partitioned and reconciled separately upon PIN verification.

---

## 2. Strategic Options Analysed

| Metric | Option A: Single-Supplier Carts (Client's Choice) | Option B: Multi-Supplier Split-Shipping Carts | Option C: Platform-Standardized Shipping Zones |
| :--- | :--- | :--- | :--- |
| **User Experience (UX)** | ⚠️ **Medium:** Contractors must check out separate carts if buying from different suppliers. | 💎 **Excellent:** One-click checkout for all procurement needs. | 💎 **Excellent:** Simple flat-rate pricing. |
| **Logistics Accuracy** | 🎯 **100%:** Each supplier's rate is isolated and perfectly mapped to the cart. | 🎯 **100%:** Delivery rates are calculated independently per supplier. | ⚠️ **Poor:** Platform rates will inevitably under- or over-charge heavy bulk transport. |
| **Code Complexity** | 🟢 **Low:** Minimal validation in cart and checkout logic. | 🔴 **High:** Requires multi-tier splitting of orders, delivery zones, and payments. | 🟡 **Medium:** Platform administrators manage a unified shipping grid. |
| **Financial Reconciliation** | 🟢 **Simple:** One transaction = one supplier. Direct escrow mapping. | 🟡 **Complex:** Splitting Paystack disbursement queues per supplier order. | 🟡 **Complex:** Admin collects unified delivery fees and must disburse them to suppliers. |

---

### Option A: Restricting the Cart/Checkout to a Single Supplier
* **How it works:** When a contractor attempts to add a product from Supplier B to a cart that already has items from Supplier A, the frontend/backend warns the contractor: *“Your cart contains items from Supplier A. Checkout now or clear your cart to buy from Supplier B.”*
* **Pros:** 
  * Exceptionally clean codebase. 
  * Zero risk of complex escrow splits or multi-delivery miscalculations.
  * Operational simplicity.
* **Cons:** Larger procurement cycles require the contractor to go through checkout multiple times.

### Option B: Multi-Supplier Carts with Split Shipping
* **How it works:** The cart groups items by Supplier automatically. During checkout, we query the delivery zone rates for *each* supplier relative to the contractor's site. The checkout page displays a itemized receipt showing the breakdown:
  * Subtotal Supplier A + Shipping Supplier A
  * Subtotal Supplier B + Shipping Supplier B
  * **Total Cart Cost**
* **Pros:** The ultimate premium enterprise buyer experience. 
* **Cons:** High development overhead, and complex database transaction tracking.

### Option C: Platform-Standardized Logistics
* **How it works:** The platform administrators set up standard delivery zones (e.g., Nairobi to Mombasa = KES 15,000 flat) and suppliers must adhere to these unified platform shipping fees.
* **Pros:** Standardizes buyer checkout experience completely.
* **Cons:** Virtually impossible to run fairly because bulk weight metrics differ drastically (drywall vs. iron bars vs. aggregate cement).

---

## 3. Our Expert Recommendation

While **Option B** (Multi-Supplier Split Carts) offers the most futuristic, Amazon-like experience, **we strongly support the client’s current preference: Option A (One Supplier at a Time)**, especially for the **V1 launch** and payment integration phase.

### Why Option A is the Correct Strategic Path for V1:
1. **Escrow Safeguards:** Since payments are held in escrow and released upon delivery PIN verification, having a single supplier per order ensures that a dispute with *Supplier A* (e.g., late concrete dispatch) does not freeze the funds or delay fulfillment verification for *Supplier B* (who delivered the steel on time).
2. **Payment Gateway Limits:** Splitting payments across multiple sub-accounts during a single transaction requires highly complex gateway-level API calls (like Stripe Connect or Paystack split-payment features). Since the client has *not* paid for sub-account split gateway setups yet (as indicated in past directions), keeping checkouts strictly 1-to-1 with suppliers avoids manual bookkeeping nightmares.
3. **Cart-to-Quote Realities:** In B2B industrial procurement, contractors rarely buy cement and plumbing equipment in a single impulse click. They procure in distinct, planned project phases.

---

## 4. Transition Plan to Option A
To implement this limit smoothly:
1. **Cart Validation:** Modify the `CartItem` creation endpoint to reject requests if the product's supplier company does not match the supplier company of the items already present in the user's cart.
2. **Friendly UI Prompts:** When a contractor attempts to add a product from a different supplier, show a premium modal asking if they want to:
   * *View existing cart and check out first.*
   * *Clear current cart and start a new procurement with this supplier.*
