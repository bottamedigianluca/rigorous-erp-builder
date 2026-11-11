---
name: rigorous-erp-builder
description: Architect, design, ground, and implement mission-critical ERPs, accounting engines, billing systems, and fiscal software with zero-hallucination mathematical rigor, regulatory schema ingestion (XSD/JSON/EDI), legacy oracle verification, keyboard-first high-speed UI, and bulletproof offline-first storage.
metadata:
  version: "1.0.0"
  author: "Antigravity Engineering"
---

# Rigorous ERP & Financial Engine Builder

This skill provides the end-to-end engineering protocol to design, build, verify, and deploy **mission-critical Enterprise Resource Planning (ERP), invoicing, and accounting software**. 

It enforces the **Zero-Hallucination Doctrine**: financial software cannot be built by guessing business logic or asking an AI to "vibecode" accounting rules. It must be mathematically grounded in **primary legal sources, official government schemas (XSD/UBL/EDIFACT), strict fixed-point arithmetic, oracle verification against real ledgers, and keyboard-first operational ergonomics**.

---

## The 6 Iron Pillars of the Architecture

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

---

## Phase 0: Jurisdiction & Regulatory Grounding

**Rule #1: Never guess tax law. Ingest primary machine-readable specifications.**

1. **Identify the Tax & Billing Authority:**
   - **Italy:** Agenzia delle Entrate / SdI (FatturaPA 1.2 `Schema_VFPR12.xsd`, `Schema_VFSM10.xsd`, TD01–TD28 document codes).
   - **Pan-European / International:** Peppol BIS Billing 3.0 (UBL 2.1, Schematron, EN 16931).
   - **France:** Chorus Pro / Factur-X (CII / ZUGFeRD hybrid PDF+XML).
   - **Spain:** TicketBAI / SII (AEAT XML schemas).
   - **Germany:** XRechnung / ZUGFeRD 2.0+.
   - **Poland:** KSeF (Krajowy System e-Faktur).
   - **US / Canada:** Sales tax jurisdiction rules, nexus thresholds, Avalara/TaxJar integration specs, strict GAAP ledgers.
   - **Latin America:** Mexico (CFDI 4.0), Brazil (NF-e), Chile (DTE).
   - **Middle East:** Saudi Arabia ZATCA Phase 2 (Cryptographic stamping, UBL 2.1).

2. **Schema Ingestion Protocol:**
   - Download the official `.xsd`, `.json`, `.dtd`, or Schematron rules directly into a `resources/schemas/` directory.
   - Build an in-engine **native validator** (or embed a standalone high-performance validator without relying on heavy external system runtimes like .NET CLR or Java JVM).
   - Catalog all official document types, tax exempt codes (e.g. EU VAT exemptions $N1$–$N7$), withholding taxes, and legal regimes.

---

## Phase 1: Zero-Float Decimal Financial Kernel

**Rule #2: Strict ban on IEEE 754 floating-point numbers (`f32`, `f64`, `double`, JS `number`).**

1. **Data Types:**
   - **Rust:** `rust_decimal::Decimal` (128-bit fixed point, 28-29 decimal digits).
   - **Go:** `shopspring/decimal`.
   - **Python:** `decimal.Decimal` with explicit `getcontext()`.
   - **C# / .NET:** `System.Decimal`.
   - **SQL:** `DECIMAL(19, 4)` or `NUMERIC(18, 5)` for unit prices, `DECIMAL(15, 2)` for currency totals.

2. **Rounding Specifications:**
   - Explicitly choose and document the rounding mode demanded by the local tax code:
     - **Half-Even (Banker's Rounding):** Standard for European accounting.
     - **Half-Up:** Standard for commercial invoicing in certain non-EU jurisdictions.
   - **VAT Rounding Granularity:**
     - *Line-by-line rounding* vs *Subtotal-by-tax-rate rounding* (document-level summary).
     - If line-by-line: enforce penny-balancing mechanisms (`Arrotondamento` / residual difference adjustment) so that $\sum (\text{Line Net} + \text{Line Tax}) == \text{Total Payable}$.

---

## Phase 2: Document Lifecycle, Immutability & Numbering

**Rule #3: Financial documents cannot disappear or have gaps in numbering.**

1. **State Machine:**
   ```
   [DRAFT / BOZZA] ──(Confirm/Issue)──> [COMMITTED / EMESSO] ──(Transmit)──> [SENT / SDI / PEPPOL]
         │                                      │                                 │
      (Delete)                           (Credit Note / NC)                 (Receipt / ESITO)
         ▼                                      ▼                                 ▼
    [DISCARDED]                         [OFFSET INVOICE]                  [ACCEPTED / REJECTED]
   ```
2. **Numbering Integrity:**
   - Document numbers (`Anno / Serie / Numero`) must be strictly sequential per series.
   - Deletion of an issued document is forbidden by tax authorities; it requires a formal **Reversal / Credit Note** (`Nota di Credito`, `Avoir`, `Storno`).
   - If an internal numbering hole occurs (e.g. crash during allocation), record the event in an audit table (`buchi_numerazione`) with operator timestamp and reason.

3. **Storage Engine:**
   - **SQLite with WAL Mode:** Perfect for zero-maintenance on-premise single-binary or LAN ERPs.
     - Pragmas: `journal_mode = WAL`, `busy_timeout = 5000`, `foreign_keys = ON`, `synchronous = NORMAL`.
     - Zero-lock point-in-time hot backups via `VACUUM INTO 'path/backup.db'`.
   - **Outbox Pattern:** Never perform dual-writes (e.g. database write + external API call in the same transaction). Write the document and an `outbox_events` record in a single atomic transaction. A background dispatcher processes events idempotently.

---

## Phase 3: The Oracle Verification & Mutation Testing Protocol

**Rule #4: If replacing or replicating a legacy system, prove 0 differences on real history.**

1. **0-Difference Historical Replay (The Oracle Test):**
   - Take the legacy database (e.g. Arca, SAP, Zucchetti, QuickBooks, Navision).
   - Re-run thousands of historical invoices, credit notes, and ledgers through the new engine.
   - Compare output bit-for-bit, cent-for-cent:
     - Header totals ($0$ diff).
     - Tax distribution breakdown ($0$ diff).
     - Payment installments / Scadenzario ($0$ diff).
     - Generated XML/EDI format ($0$ diff).

2. **Systematic Mutation Testing (Fuzzing the Schemas):**
   - Take a diverse sample of valid documents.
   - Systematically mutate every XML/JSON tag:
     - Element removed (tests mandatory vs optional enforcement).
     - Element duplicated (tests `maxOccurs` bounds).
     - Sibling order swapped (tests strict sequence enforcement).
     - Value edge cases: invalid calendar dates (e.g. Feb 30), negative numbers, illegal currency symbols, non-ASCII/invalid UTF-8 bytes, max-length overflow.
   - Run both the new engine and an authoritative reference validator (e.g. official government test API or .NET / Xerces validator) and assert **100% agreement on rejection verdicts**.

---

## Phase 4: Ergonomics & Keyboard-First High-Speed UX

**Rule #5: Warehouse and counter operators must never be forced to touch a mouse.**

1. **Standard Keybinding Grid:**
   - `Enter`: Advance to the next logical input field (auto-selecting existing text).
   - `Arrow Up / Down`: Navigate grid rows without opening dialogs.
   - `F3`: Rapid containing-text search (`contiene`, not just `inizia per`) across codes and descriptions.
   - `F8`: Row picker (import rows from previous quotes, orders, delivery notes, or price lists).
   - `Esc`: Cancel dropdown / discard current row / close modal.
   - `Ctrl + Enter` (or `F10`): Instant commit / save document.

2. **Direct Hardware Spooler Printing:**
   - Never rely on browser `window.print()` dialogs for high-volume logistics.
   - Provide direct native spooler routing (Windows Print Spooler `winspool.drv`, Linux CUPS, raw ESC/POS for receipt printers, ZPL for thermal barcode labelers).

3. **Anti-Crash Draft Protection:**
   - Debounced background autosave to persistent local storage on every keystroke.
   - `beforeunload` warning when an unsaved document has uncommitted modifications.
   - Cold startup recovery prompt: *"Unsaved draft from [Date Time] detected for Customer X (N items). Restore or Discard?"*

---

## Phase 5: Disaster Recovery & Automated 3-2-1 Backups

**Rule #6: Data safety is mathematically guaranteed, not left to user memory.**

1. **Local Rotating Backup:**
   - Daily scheduled atomic snapshots without locking live transactions.
   - Grandfather-Father-Son retention:
     - Last 14 daily snapshots.
     - Last 4 weekly Friday snapshots.
     - 12 end-of-month annual snapshots.
2. **Encrypted Cloud Mirroring (Multi-Account Offsite):**
   - Compress with high-performance algorithms (`zstandard` / `gzip`).
   - Client-side encryption with **AES-256-GCM** before leaving the local network.
   - Asynchronous offsite sync to 2 separate accounts/providers (e.g. Google Drive, AWS S3, Cloudflare R2, offsite NAS) implementing true **3-2-1 backup rules**.

---

## Detailed References

For specialized technical implementations, refer to the guides in `references/`:
- [Jurisdiction Discovery & Fiscal Sources](references/jurisdiction-discovery.md)
- [Financial Math & Rounding Engine](references/financial-math-and-rounding.md)
- [Keyboard-First UX & POS Design](references/keyboard-first-ux.md)
