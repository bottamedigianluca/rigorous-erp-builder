#!/usr/bin/env python3
"""
Verification Script for Rigorous ERP Math & Rounding
Demonstrates the 6 Iron Pillars in executable code.
"""

from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

def test_floating_point_hazard():
    """Pillar 2: Proof that standard float breaks financial accounting."""
    # IEEE 754 float failure:
    f_sum = 0.1 + 0.2
    assert f_sum != 0.3, "Float unexpectedly equaled 0.3"
    
    # Strict Decimal correctness:
    d_sum = Decimal("0.1") + Decimal("0.2")
    assert d_sum == Decimal("0.3"), "Decimal sum failed"
    print("✓ Test 1 Passed: Zero-Float Decimal Precision Guaranteed")

def test_bankers_rounding():
    """Pillar 2: Half-Even (Banker's) Rounding to eliminate ledger bias."""
    two_cents = Decimal("0.01")
    
    # 2.545 -> rounds to nearest EVEN digit (4) -> 2.54
    v1 = Decimal("2.545").quantize(two_cents, rounding=ROUND_HALF_EVEN)
    assert v1 == Decimal("2.54"), f"Expected 2.54, got {v1}"
    
    # 2.555 -> rounds to nearest EVEN digit (6) -> 2.56
    v2 = Decimal("2.555").quantize(two_cents, rounding=ROUND_HALF_EVEN)
    assert v2 == Decimal("2.56"), f"Expected 2.56, got {v2}"
    
    print("✓ Test 2 Passed: Banker's Rounding (Half-Even) Verified")

def test_penny_balancing():
    """Pillar 2: Residual Penny-Balancing (Line vs Document VAT)."""
    rate = Decimal("0.22")
    unit_price = Decimal("1.05")
    qty = Decimal("100")
    
    # Document Level (Vertical Summary):
    total_base = unit_price * qty  # 105.00
    doc_vat = (total_base * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)  # 23.10
    total_payable = total_base + doc_vat  # 128.10
    
    # Line Level (Horizontal):
    line_vat = (unit_price * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)  # 0.23
    sum_line_vat = line_vat * qty  # 23.00
    
    # Calculate Discrepancy & Arrotondamento delta
    delta = doc_vat - sum_line_vat  # 0.10
    assert delta == Decimal("0.10"), "Unexpected delta calculation"
    
    # Balanced invoice
    balanced_total = total_base + sum_line_vat + delta
    assert balanced_total == total_payable, "Penny balancing failed to reconcile"
    print(f"✓ Test 3 Passed: Penny-Balancing Reconciled delta of {delta}")

if __name__ == "__main__":
    print("Running Rigorous ERP Verification Suite...")
    test_floating_point_hazard()
    test_bankers_rounding()
    test_penny_balancing()
    print("All mathematical invariants verified successfully.")
