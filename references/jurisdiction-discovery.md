# Jurisdiction Discovery & Regulatory Grounding

When building an ERP or accounting system for a specific country or economic area, follow this discovery protocol to ensure 100% legal compliance.

---

## 1. Primary Authority & Machine-Readable Artifacts

Never rely on secondary blog posts or LLM pre-training memory for tax rules. Always fetch primary legal texts and machine-readable schemas.

| Jurisdiction | Primary Authority | Technical Formats | Canonical Schemas & Document Types |
| :--- | :--- | :--- | :--- |
| **Italy** | Agenzia delle Entrate (AdE) / Sogei | XML (FatturaPA 1.2.x), XSD, WSDL | `Schema_VFPR12.xsd` (B2B), `Schema_VFSM10.xsd` (Semplificata), Document types `TD01` to `TD28`, Nature codes `N1`–`N7`, Regimes `RF01`–`RF19`. |
| **European Union (B2G/B2B)** | European Committee for Standardization (CEN) | UBL 2.1, CII, Schematron | **EN 16931**, Peppol BIS Billing 3.0, Validation via Schematron (`.sch`) & XSLT. |
| **France** | Direction Générale des Finances Publiques (DGFiP) | Factur-X, UBL, CII | Factur-X (Hybrid PDF/A-3 with embedded XML), Chorus Pro API. |
| **Spain** | Agencia Tributaria (AEAT) / Foral Treasuries | XML, TicketBAI, SII | Suministro Inmediato de Información (SII), TicketBAI XML with cryptographic chaining & QR codes. |
| **Germany** | Koordinierungsstelle für IT-Standards (KoSIT) | XML (XRechnung), Factur-X / ZUGFeRD | XRechnung standard (UBL/CII), ZUGFeRD 2.2+. |
| **Poland** | Ministerstwo Finansów | XML (FA_VAT) | KSeF (Krajowy System e-Faktur) logical schema `FA(2)`. |
| **United States** | IRS / State Departments of Revenue | GAAP Ledgers, Tax Tables | Sales tax boundary lookup (by 9-digit ZIP / address lat-long), Resale certificates, 1099 reporting. |
| **OECD Members** | National Tax Authorities | XML (SAF-T) | Standard Audit File for Tax (SAF-T / OECD schema version 2.0). |
| **Latin America** | SAT (Mexico), Receita Federal (Brazil), SII (Chile) | XML, PAC Stamping, PDF CBB | Mexico CFDI 4.0 (Anexo 20), Brazil NF-e (Modelo 55), Digital seals (`Sello Digital`). |
| **Saudi Arabia** | ZATCA (Fatoora) | UBL 2.1 with XML-DSig & QR | Phase 2 Integration: ECDSA secp256k1 cryptographic stamping, Cryptographic Stamp Identifier (CSID). |

---

## 2. The Verification Protocol for New Jurisdictions

When initializing a new jurisdiction in the ERP:

1. **Schema Retrieval:**
   - Locate the official government development portal (e.g. `agenziaentrate.gov.it`, `peppol.eu`, `sat.gob.mx`).
   - Download the official `.xsd` (XML Schema Definition) or `.json` schema into the project.
   - Commit the schema directly into the repository version control so builds are reproducible offline without relying on external CDNs.

2. **Entity & Tax Code Modeling:**
   - **Company Fiscal Identity:** Tax ID, VAT ID (with country prefix, e.g. VIES format), Legal name, Registration office, Share capital, Fiscal regime.
   - **Customer/Vendor Classification:** Domestic business (B2B), Public administration (B2G), Private consumer (B2C), Foreign/Extra-EU customer.
   - **Tax Rates & Exemptions:** Standard rates, reduced rates, super-reduced rates, exempt articles with legal citations.

3. **Transmission & Receipt State Machine:**
   - Map all lifecycle states:
     - `000` (Created / Draft)
     - `IN_TRANSIT` (Signed and queued for dispatch)
     - `DELIVERED` (Accepted by government gateway)
     - `REJECTED` (Validation error from government gateway, with specific error codes)
     - `NOT_DELIVERABLE` (Valid invoice, but recipient mailbox/address unavailable)
     - `FINAL_ACCEPTANCE` (Explicit acceptance by public administration)
