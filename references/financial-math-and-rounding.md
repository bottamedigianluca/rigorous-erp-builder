# Financial Math & Rounding Engine

Financial mathematics requires absolute precision. A single rounding discrepancy of one cent ($0.01) between line items and total payment can cause an electronic invoice to be rejected by tax authorities.

---

## 1. Absolute Ban on Floating-Point Math

```
  WRONG:  0.1 + 0.2  ==  0.30000000000000004  (IEEE 754 Float Bug)
  RIGHT:  Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
```

- **Never** use `float`, `f32`, `f64`, `double`, or native JavaScript `number` for prices, quantities, taxes, or currency balances.
- Use exact **128-bit fixed-point decimal arithmetic** with at least 4 fractional digits for unit prices and quantities, and 2 fractional digits for final monetary values.

---

## 2. Rounding Algorithms

Financial software must specify the exact rounding strategy demanded by law or commercial agreement:

### A. Banker's Rounding (`Half-Even`)
- If the fraction is exactly halfway between two numbers, it rounds to the nearest **even** number.
  - $2.555 \to 2.56$
  - $2.545 \to 2.54$ (4 is even)
  - $2.535 \to 2.54$ (4 is even)
- **Why:** Prevents statistical drift/bias in ledgers over millions of transactions. Required by many European accounting standards.

### B. Commercial Rounding (`Half-Up`)
- If the discarded fraction is $\ge 0.5$, it always rounds up (away from zero).
  - $2.545 \to 2.55$
  - $2.535 \to 2.54$

---

## 3. The Line vs Document VAT Discrepancy Problem

Invoicing systems encounter two methods for calculating total VAT:

### Method 1: Line-by-Line Rounding (Horizontal)
Calculate tax on each individual row, round it to 2 decimal places, then sum the rounded taxes:
$$\text{LineTax}_i = \text{round}(\text{Qty}_i \times \text{Price}_i \times \text{Rate})$$
$$\text{TotalTax} = \sum_{i=1}^n \text{LineTax}_i$$

### Method 2: Grouped Tax Base Rounding (Vertical)
Sum all line net amounts for a specific VAT rate, calculate the tax once on the aggregated sum, and round once:
$$\text{Base}_{\text{Rate}} = \sum \text{LineNet}_{i, \text{Rate}}$$
$$\text{Tax}_{\text{Rate}} = \text{round}(\text{Base}_{\text{Rate}} \times \text{Rate})$$

### The Discrepancy:
On an invoice with 100 items at \$1.05 with 22% VAT:
- Method 1: each line tax is $\text{round}(1.05 \times 0.22) = \text{round}(0.231) = 0.23$. Total tax $= 100 \times 0.23 = \$23.00$.
- Method 2: total base $= \$105.00$. Total tax $= \text{round}(105.00 \times 0.22) = \text{round}(23.10) = \$23.10$.
- **Discrepancy: \$0.10!**

### The Mathematical Solution:
1. Ground the engine in the specific tax jurisdiction's rules (e.g. Italian FatturaPA uses Grouped Tax Base in `DatiRiepilogo`).
2. Implement **Residual Penny-Balancing** (`Arrotondamento`):
   When line totals don't sum exactly to the grouped summary total, calculate the rounding delta:
   $$\Delta = \text{DocumentTotal} - \sum \text{LinePayable}$$
   Explicitly record $\Delta$ in the designated `Arrotondamento` field so the document mathematically balances to the exact cent.
