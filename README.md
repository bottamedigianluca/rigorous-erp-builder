# 🏛️ Rigorous ERP Builder — AI Agent Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Skill-orange)](https://github.com/bottamedigianluca/rigorous-erp-builder)
[![Category: Enterprise AI](https://img.shields.io/badge/Domain-ERP%20%26%20Accounting-purple)](#)
[![Zero Float](https://img.shields.io/badge/Math-Zero--Float%20Decimal-green)](#)

> **"Stop letting LLMs hallucinate tax laws. Build mission-critical ERPs, accounting engines, and billing systems with zero-hallucination mathematical rigor, regulatory schema ingestion (XSD/JSON/EDI), legacy oracle verification, and keyboard-first UI."**

---

## The "Vibecoding Trap" in Accounting Software

When you ask an AI coding agent to *"build an invoicing app"* or *"create an ERP"*, it almost always falls into fatal traps:
1. **IEEE 754 Floating-Point Corruption:** It uses `float` or JS `number` where `0.1 + 0.2 = 0.30000000000000004`, leading to silent penny drift and ledger imbalance.
2. **Hallucinated Tax Rules:** It guesses VAT rates, reverse-charge codes, withholding taxes, and exemptions from memory instead of authoritative government specifications.
3. **Numbering Holes:** It allows deleting documents or fails to guarantee gapless sequential numbering, violating fiscal auditing laws.
4. **Clumsy Mouse-First UIs:** It builds slow web forms with modal popups that take 45 seconds per document instead of high-speed keyboard grids capable of 3-second data entry.
5. **No Verification Oracle:** It never verifies calculated amounts against historical production databases or official test validators.

**Rigorous ERP Builder** is a formal skill protocol for AI agents (Antigravity, Claude Code, Cursor, Codex, Windsurf) that eliminates these failures.

---

## 🏛️ The 6 Iron Pillars

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   THE 6 PILLARS OF MISSION-CRITICAL ERP                │
  ├────────────────────────────────────────────────────────────────────────┤
  │ 1. REGULATORY GROUND TRUTH    Official government XSD / legal specs    │
  │ 2. FIXED-POINT FINANCIAL MATH Zero floating-point arithmetic           │
  │ 3. NUMBERING & IMMUTABILITY   Zero gaps, audit logs, append-only       │
  │ 4. ORACLE & MUTATION TESTING  0-diff historical replay & schema fuzzing│
  │ 5. KEYBOARD-FIRST REALITY     High-speed POS/warehouse data entry     │
  │ 6. DURABLE STORAGE & 3-2-1 BK SQLite WAL / Postgres + encrypted cloud  │
  └────────────────────────────────────────────────────────────────────────┘
```

### 1. Regulatory Ground Truth (Official Schemas First)
The agent is forbidden from guessing national tax rules. It must locate and ingest primary machine-readable artifacts:
- **Italy:** Agenzia delle Entrate / Sogei (`Schema_VFPR12.xsd`, `Schema_VFSM10.xsd`, TD01–TD28).
- **Pan-European / International:** Peppol BIS Billing 3.0 (EN 16931, UBL 2.1, Schematron).
- **France:** Chorus Pro / Factur-X (CII / ZUGFeRD PDF/A-3).
- **Spain:** TicketBAI / SII (AEAT XML with cryptographic chaining).
- **Germany:** XRechnung / ZUGFeRD 2.0+.
- **Poland:** KSeF (Krajowy System e-Faktur).
- **Latin America:** Mexico (CFDI 4.0), Brazil (NF-e).
- **Middle East:** Saudi Arabia ZATCA Phase 2 (UBL 2.1 + ECDSA signatures).

### 2. Zero-Float Financial Math
- Strict ban on floating-point primitives.
- Mandatory 128-bit fixed-point decimal math (`rust_decimal::Decimal`, `shopspring/decimal`, `BigDecimal`).
- Banker's Rounding (*Half-Even*) vs Commercial (*Half-Up*).
- Line vs Document VAT balancing with explicit **Residual Penny-Balancing** (`Arrotondamento`).

### 3. Numbering Integrity & State Machine
- Strict document lifecycle: `Draft` $\to$ `Committed` $\to$ `Sent` $\to$ `Reconciled / Reversal`.
- Absolute zero numbering holes per series. Deletion of committed invoices is forbidden (formal Credit Notes / Storni only).
- Outbox pattern for zero-lock, idempotent asynchronous external dispatch.

### 4. Oracle Verification & Mutation Testing
- **0-Difference Historical Replay:** Replaying thousands of real historical invoices from legacy systems (SAP, Arca, Dynamics, QuickBooks) and asserting $0$ cent differences across totals, tax groups, and payment terms.
- **Systematic Mutation Testing:** Fuzzing schema boundaries by generating 40,000+ intentionally mutated documents (missing mandatory tags, duplicate elements, inverted tag sequences, invalid calendar dates, out-of-range decimals) and proving 100% agreement with government validators.

### 5. Keyboard-First Warehouse & POS Ergonomics
- `Enter` advances focus and auto-selects text for instant overwriting.
- `F3`: Omnipresent rapid substring search (`contiene`, not prefix-only).
- `F8`: Multi-row picker for importing items from orders/delivery notes.
- Direct hardware spooler bypass (Win32 Spooler `winspool.drv`, CUPS, raw ESC/POS, ZPL) eliminating browser print dialogs.
- Anti-crash autosave with uncommitted draft recovery on cold startup.

### 6. Durable Storage & Automated 3-2-1 Backups
- Lightweight ACID storage: SQLite WAL mode with sub-second zero-lock hot snapshots (`VACUUM INTO`).
- Grandfather-Father-Son retention (14 daily, 4 weekly, 12 monthly).
- Client-side AES-256-GCM encryption with automated mirroring across 2 independent cloud accounts.

---

## 🚀 How to Install & Use

### With Google Antigravity
Clone or copy this folder into your skills directory:
```bash
git clone https://github.com/bottamedigianluca/rigorous-erp-builder.git ~/.gemini/config/skills/rigorous-erp-builder
```
Then simply instruct your agent:
> *"Use the `rigorous-erp-builder` skill to design and implement an e-invoicing and accounting engine for [Jurisdiction / Country] adhering to all 6 pillars."*

### With Claude Code / Codex / Cursor / Windsurf
Add `SKILL.md` to your project instructions or system prompt (`.claude.md`, `.cursorrules`, or `AGENTS.md`).

---

## 📂 Repository Structure

```
rigorous-erp-builder/
├── SKILL.md                                 # Master protocol & execution guide
├── README.md                                # Documentation & overview
├── LICENSE                                  # MIT License
└── references/
    ├── jurisdiction-discovery.md            # Tax authority discovery table & rules
    ├── financial-math-and-rounding.md       # Fixed-point math, rounding, VAT balancing
    └── keyboard-first-ux.md                 # Ergonomics, keybindings, spooler printing
```

---

## 📄 License
MIT © [Gianluca Bottamedi](https://github.com/bottamedigianluca)
