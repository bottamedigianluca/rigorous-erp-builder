---
name: rigorous-erp-builder
description: Architect, design, ground, and implement mission-critical ERPs, accounting engines, billing systems, and fiscal software with zero-hallucination mathematical rigor, regulatory schema ingestion (XSD/JSON/EDI), legacy oracle verification, keyboard-first high-speed UI, and bulletproof offline-first storage.
metadata:
  version: "2.0.0"
  author: "Gianluca Bottamedi & Antigravity Engineering"
---

# Rigorous ERP & Financial Engine Builder

This skill provides the end-to-end engineering protocol to design, build, verify, and deploy **mission-critical Enterprise Resource Planning (ERP), invoicing, and accounting software**. 

It enforces the **Zero-Hallucination Doctrine**: financial software cannot be built by guessing business logic or asking an AI to "vibecode" accounting rules. It must be mathematically grounded in **primary legal sources, official government schemas (XSD/UBL/EDIFACT), strict fixed-point arithmetic, double-entry ledger invariants, oracle verification against real ledgers, and keyboard-first operational ergonomics**.

---

## The 7 Gate-Checked Build Pipeline

Every ERP implementation undertaken with this skill **must execute strictly in this sequential order**. Do NOT skip ahead to the UI or invoice generator before the underlying gates pass.

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   THE 7 GATES OF RIGOROUS ERP BUILDING                 │
  ├────────────────────────────────────────────────────────────────────────┤
  │ GATE 0: REGULATORY DISCOVERY   Official government schemas (XSD/UBL)   │
  │ GATE 1: RELATIONAL DATA ENGINE Strict schemas, Outbox, Sequential IDs   │
  │ GATE 2: FINANCIAL KERNEL       Zero-float math, Compound discounts     │
  │ GATE 3: GENERAL LEDGER (GL)    Double-entry invariants (Debit == Credit)│
  │ GATE 4: DOCUMENT LIFECYCLE     Fulfillment lineage (Order->DDT->Invoice)│
  │ GATE 5: SERIALIZATION & XSD    Streaming XML/JSON + Mutation Fuzzing    │
  │ GATE 6: KEYBOARD-FIRST UX      Zero-mouse grid, F3/F8, Spooler printing │
  │ GATE 7: 3-2-1 DISASTER RECOV   SQLite WAL hot snapshots + AES-256 cloud │
  └────────────────────────────────────────────────────────────────────────┘
```

---

## GATE 0: Jurisdiction & Regulatory Grounding

**Exit Criterion: Official schema files committed in `resources/schemas/` and validated.**

1. **Locate Authoritative Machine-Readable Artifacts:**
   - **Italy:** Agenzia delle Entrate / Sogei (`Schema_VFPR12.xsd`, `Schema_VFSM10.xsd`, TD01–TD28 document types, `FTE_WorkFlow` states).
   - **Pan-European / International:** Peppol BIS Billing 3.0 / EN 16931 (UBL 2.1 schemas + Schematron `.sch` rules).
   - **France:** Chorus Pro / Factur-X (CII hybrid PDF/A-3).
   - **Spain:** TicketBAI / SII (AEAT XML with cryptographic chaining).
   - **Germany:** XRechnung / ZUGFeRD 2.0+ (UBL/CII).
   - **US / OECD:** GAAP ledgers, OECD SAF-T schema.
   - **Latin America:** Mexico (CFDI 4.0), Brazil (NF-e).

2. **Schema Ingestion Checklist:**
   - Download the official `.xsd`, `.json`, or `.dtd` files directly into the repository.
   - Extract legal tax exemption regimes ($N1$–$N7$), reverse-charge triggers, withholding tax types (`RT01`–`RT06`), and social security fund codes.
   - Build an in-engine **native validator** (in Rust, Go, or C# AOT) with zero external runtime dependencies (no separate Java JVM or .NET CLR installation required at customer runtime).

---

## GATE 1: Relational Data Engine & Sequencing

**Exit Criterion: Database migrations committed with ACID durability, outbox tables, and gapless numbering.**

1. **Storage Engine Choice:**
   - **On-Premise / LAN / Embedded:** SQLite with strict WAL mode:
     ```sql
     PRAGMA journal_mode = WAL;
     PRAGMA busy_timeout = 5000;
     PRAGMA foreign_keys = ON;
     PRAGMA synchronous = NORMAL;
     ```
   - **Distributed Cloud:** PostgreSQL with strict schema constraints and transactional outbox.

2. **Gapless Document Numbering:**
   - Tax auditors treat missing invoice numbers as potential tax fraud.
   - Never generate document numbers in memory (`SELECT MAX(num) + 1` is vulnerable to race conditions!).
   - Use an atomic sequence table with row-level locks:
     ```sql
     UPDATE sequenze_documenti 
     SET ultimo_numero = ultimo_numero + 1 
     WHERE anno = ? AND serie = ? AND tipo = ?
     RETURNING ultimo_numero;
     ```
   - If an internal numbering void occurs (e.g. power outage mid-transaction), record the event in `audit_buchi_numerazione` with operator ID, timestamp, and explanation.

3. **Transactional Outbox Pattern:**
   - Never perform dual-writes (e.g. commit invoice to DB and call government API in the same function).
   - Insert document + `outbox_events` in a single atomic transaction. An asynchronous worker dispatches events idempotently.

---

## GATE 2: Zero-Float Decimal Financial Kernel

**Exit Criterion: 100% of arithmetic runs on fixed-point decimals with zero penny drift.**

1. **Data Types:**
   - **Rust:** `rust_decimal::Decimal` (128-bit fixed point).
   - **Go:** `shopspring/decimal`.
   - **Python:** `decimal.Decimal`.
   - **SQL:** `DECIMAL(19, 4)` for unit prices, `DECIMAL(15, 2)` for currency totals.
   - **STRICT BAN:** `f32`, `f64`, `double`, native JS `number`.

2. **Compound Cascading Discounts (Sconti a Cascata):**
   - Commercial B2B contracts rarely use flat discounts. They use expressions like `20+10+5%` (or discount amount + percentage).
   - **The Mathematical Formula:**
     $$\text{PrezzoNetto} = \text{PrezzoBase} \times (1 - d_1) \times (1 - d_2) \times (1 - d_3) - \text{ScontoValore}$$
   - **Never sum percentages:** $20\% + 10\% + 5\% \neq 35\%$. (Compounded: $1 \times 0.8 \times 0.9 \times 0.95 = 0.684 \implies 31.60\%$).

3. **Tax Rounding & Residual Penny-Balancing:**
   - Enforce **Banker's Rounding** (`Half-Even`) to eliminate statistical inflation bias in ledgers.
   - **Horizontal (Line-by-Line) vs Vertical (Grouped Tax Base) Balancing:**
     $$\Delta = \text{DocumentTotalTax} - \sum \text{LineTax}_i$$
     Explicitly record $\Delta$ into the `Arrotondamento` residual field so the invoice balances to the exact cent.

4. **Special Tax Regimes:**
   - **Split Payment (PA):** Total invoice includes VAT, but Total Payable excludes VAT (the buyer pays VAT directly to the Treasury).
   - **Reverse Charge (Inversione Contabile):** Line VAT is 0%, reference note quotes applicable tax law article (e.g. art. 17 c. 6).
   - **Virtual Stamp Duty (Bollo Virtuale):** Applied automatically if exempt lines exceed the statutory threshold (e.g. €77.47 in Italy).

---

## GATE 3: Double-Entry General Ledger (Partita Doppia)

**Exit Criterion: Invariant $\sum \text{Debit} == \sum \text{Credit}$ enforced at database constraint level.**

1. **Accounting Invariant:**
   Every financial transaction must balance to zero:
   $$\sum \text{Dare (Debit)} - \sum \text{Avere (Credit)} = 0.00$$
2. **Standard Sales Invoice Journal Entry:**
   - **Debit:** Accounts Receivable (Crediti v/Clienti) = $\text{Total Document}$
   - **Credit:** Revenue (Merci c/Vendite) = $\text{Total Taxable Base}$
   - **Credit:** VAT Payable (IVA a Debito) = $\text{Total VAT}$
3. **Draft vs Final Commitment:**
   - Draft documents generate **zero** general ledger entries and **zero** warehouse stock movements.
   - Committing a document executes an atomic transaction writing the journal entry, payment schedule installments, and warehouse depletion.

---

## GATE 4: Document Lifecycle & Fulfillment Lineage

**Exit Criterion: Parent-child relationship tracking between Orders, Delivery Notes, and Invoices.**

1. **State Machine:**
   ```
   [DRAFT] ──> [COMMITTED] ──> [TRANSMITTED / SDI] ──> [RECONCILED]
      │             │
   (Delete)   (Credit Note)
      ▼             ▼
   [PURGED]   [OFFSET RECORD]
   ```
2. **Line Fulfillment (Prelievo Righe / Evasione):**
   - When Invoice `FT` pulls rows from Delivery Note `BO` (or Order `OC`), it must track line lineage:
     - `Id_DORig_Origine`: Foreign key to parent row.
     - `Quantita_Ordinata`
     - `Quantita_Consegnata`
     - `Quantita_Fatturata`
     - `Quantita_Residua` = $\text{Consegnata} - \text{Fatturata}$
   - A Delivery Note is automatically marked `Totalmente Evaso` only when all rows have $\text{Quantita\_Residua} == 0$.

---

## GATE 5: Serialization, XSD Validation & Mutation Fuzzing

**Exit Criterion: 100% agreement on rejection verdicts between internal validator and government oracle.**

1. **Streaming Serialization:**
   - Write XML/JSON using streaming writers (e.g. `quick-xml` in Rust, `XmlWriter` in C#) to ensure sub-millisecond generation and low memory footprint.
   - Enforce exact character encoding (UTF-8 without BOM or ISO-8859-1 as specified by local law).

2. **Systematic Mutation Fuzzing:**
   - Take real historical invoices.
   - Apply systematic mutations to every XML tag:
     - Tag removed (mandatory vs optional check).
     - Tag duplicated (`maxOccurs` check).
     - Order inverted (strict `xs:sequence` check).
     - Illegal boundary values: February 30th date, 25:00 hour, negative amounts, forbidden symbols (e.g. `€` in basic Latin fields), character length overflow.
   - Assert internal validator rejects **100%** of corrupted documents with human-readable error messages.

---

## GATE 6: Keyboard-First Warehouse & POS Ergonomics

**Exit Criterion: Operator can input a 20-line document using keyboard only, under 30 seconds.**

1. **Standard Keybinding Grid:**
   - `Enter`: Advance to next cell with text auto-selected (never use mouse to change inputs).
   - `Arrow Up / Down`: Navigate grid rows without opening dialogs.
   - `F3`: Omnipresent rapid substring search (`contiene`, not prefix-only).
   - `F8`: Row picker (pull unbilled delivery notes or quotes).
   - `Esc`: Cancel dropdown / revert active row / prompt close.
   - `Ctrl + Enter` (or `F10`): Instant commit and print.

2. **Direct Hardware Spooler Printing:**
   - Never show browser `window.print()` dialogs for warehouse delivery notes or cash register receipts.
   - Send raw bytes directly to OS spoolers:
     - **Windows:** Win32 `winspool.drv` (`OpenPrinter`, `StartDocPrinter`, `WritePrinter`).
     - **Linux / macOS:** CUPS raw queue.
     - **Thermal / Receipt:** Raw ESC/POS or ZPL over TCP/IP or COM port.

3. **Anti-Crash Autosave & Draft Recovery:**
   - Debounce document state to local storage every 500ms.
   - Intercept accidental tab close with `beforeunload`.
   - On startup: *"Unsaved draft from [Date Time] detected for Customer X (N items). Restore or Discard?"*

---

## GATE 7: Durable Local Storage & Automated 3-2-1 Backups

**Exit Criterion: Sub-second point-in-time snapshots and encrypted offsite mirroring.**

1. **Zero-Lock Hot Snapshots:**
   - With SQLite WAL, execute `VACUUM INTO 'backup.db'` while cashiers are actively issuing invoices. Zero downtime, zero table locking.
2. **3-2-1 Retention:**
   - 14 daily snapshots.
   - 4 weekly Friday snapshots.
   - 12 end-of-month annual snapshots.
3. **Encrypted Cloud Mirroring:**
   - Compress with `zstandard` / `gzip`.
   - Client-side AES-256-GCM encryption before offsite sync to 2 separate cloud providers (Google Drive, AWS S3, Cloudflare R2).

---

## The 10 Deadly ERP Anti-Patterns (Reject Immediately)

1. **Floating-point currency math** (`f64`, `float`, JS `number`).
2. **Linear addition of compounding discounts** (`20+10` calculated as `30%` instead of `31.6%`).
3. **Hard deleting an issued document** (`DELETE FROM invoices`).
4. **Dual-writes** (DB commit + external API call without Outbox pattern).
5. **In-memory sequence generation** (race conditions on invoice numbers).
6. **Ignoring line vs document tax rounding discrepancies** (penny-balancing omission).
7. **Mouse-dependent forms** lacking `Enter` cell-advance and auto-selection.
8. **Browser print dialogs** in high-volume warehouse pick & pack stations.
9. **External runtime dependencies** (.NET CLR / Java JVM) for core validation.
10. **Unchecked drafts** lost on browser refresh or power cut.

---

## References & Specialized Playbooks

- [Jurisdiction Discovery & Fiscal Schemas](references/jurisdiction-discovery.md)
- [Financial Math, Rounding & Penny Balancing](references/financial-math-and-rounding.md)
- [Keyboard-First UX & Spooler Printing](references/keyboard-first-ux.md)
