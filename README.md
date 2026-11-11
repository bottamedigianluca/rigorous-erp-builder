# rigorous-erp-builder

An engineering guide and agent skill for building production ERPs, billing systems, and accounting engines that don't fall apart during a tax audit.

Most people asking LLMs to build accounting software end up with toy CRUD apps. Invoicing is not a blog post. If your engine has floating-point drift, drops document numbers, or guesses VAT rules instead of reading legal schemas, you're building a liability.

This repository codifies the rules we learned replacing legacy on-premise ERPs with modern native engines.

---

## The 6 Non-Negotiables

### 1. Ingest official government schemas (XSD / UBL / EDIFACT)
Never let an LLM guess tax law, reverse charges, or withholding rates from its training weights. 
Download the jurisdiction's authoritative machine-readable schema directly into your project:
* **Italy:** Agenzia delle Entrate / Sogei (`Schema_VFPR12.xsd`, `Schema_VFSM10.xsd`, TD01–TD28)
* **EU:** Peppol BIS Billing 3.0 / EN 16931 (UBL 2.1, Schematron)
* **France:** Factur-X / Chorus Pro (CII hybrid PDF/A-3)
* **Spain:** TicketBAI / SII (AEAT XML)
* **Germany:** XRechnung / ZUGFeRD 2.0+
* **US / Global:** GAAP ledgers, OECD SAF-T, local tax tables

### 2. Zero-float math (Fixed-point only)
IEEE 754 floats (`float`, `double`, JS `number`) will ruin your ledger (`0.1 + 0.2 != 0.3`).
* Use 128-bit fixed-point decimals (`rust_decimal::Decimal`, `shopspring/decimal`, `BigDecimal`).
* Explicitly enforce Banker's Rounding (*Half-Even*) to eliminate statistical drift.
* Implement residual penny-balancing (`Arrotondamento`) when line-by-line VAT doesn't equal vertical document-level tax summaries.

### 3. Numbering immutability & zero holes
Tax authorities treat missing invoice numbers as potential tax evasion.
* No `DELETE` queries on committed invoices. Storno / Credit Note only.
* Numbering (`Year / Series / Number`) must be strictly gapless.
* Use the Outbox pattern for asynchronous external transmission (SdI, Peppol, bank feeds). Never dual-write to DB and external APIs in the same transaction.

### 4. Oracle testing & mutation fuzzing
If you're replacing a legacy system (Arca, SAP, Dynamics, QuickBooks), prove zero regression:
* **Historical replay:** Re-run 10,000+ real archived invoices through your engine. Assert $0.00 difference across headers, VAT groups, and payment terms.
* **Mutation fuzzing:** Take valid invoices and systematically mutate tags (remove required nodes, duplicate fields, invert sequences, inject invalid calendar dates like Feb 30). Verify your validator agrees with the government/reference engine on every single rejection.

### 5. Keyboard-first UX
Cashiers and warehouse pickers hate mice. If an operator has to click through modals to log 50 line items, your software failed.
* `Enter` advances to the next cell with text auto-selected.
* `F3` opens rapid substring lookup (contains search, not prefix-only).
* `F8` multi-row picker from prior delivery notes or orders.
* Direct OS print spooler bypass (`winspool.drv`, CUPS, raw ESC/POS, ZPL) to skip browser print preview dialogs entirely.
* Local auto-save draft with recovery on crash or accidental browser tab close.

### 6. Durable local storage & automated 3-2-1 backups
Keep it self-contained:
* SQLite in WAL mode handles thousands of writes per second with sub-second zero-lock snapshots via `VACUUM INTO`.
* Local rotation: 14 daily, 4 weekly, 12 monthly.
* Client-side AES-256 encryption before offsite sync to 2 separate cloud accounts.

---

## Usage

### In Google Antigravity
Clone to your local skills directory:
```bash
git clone https://github.com/bottamedigianluca/rigorous-erp-builder.git ~/.gemini/config/skills/rigorous-erp-builder
```
Prompt:
> "Use the rigorous-erp-builder skill to architect the billing engine for [Country / Sector]."

### In Claude Code / Cursor / Windsurf / Codex
Add `SKILL.md` to your custom system instructions or repository rules (`.cursorrules`, `CLAUDE.md`, or `AGENTS.md`).

---

## Directory Layout

```
.
├── SKILL.md                                 # Core agent skill instructions
├── README.md
├── LICENSE                                  # MIT
├── scripts/
│   └── verify_financial_math.py             # Math invariants test suite
└── references/
    ├── jurisdiction-discovery.md            # Tax authority reference table
    ├── financial-math-and-rounding.md       # Rounding algorithms & VAT reconciliation
    └── keyboard-first-ux.md                 # POS/Warehouse data entry patterns
```

## License
MIT
