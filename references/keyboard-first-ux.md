# Keyboard-First Ergonomics & POS/Warehouse Protocol

Professional ERP operators (cashiers, warehouse pickers, accountants) type dozens of documents per hour. If they are forced to grab a mouse, wait for modal animations, or tab through 15 useless fields, business productivity drops by 70%.

---

## 1. The Core Keyboard Rules

1. **`Enter` Key Advances Focus:**
   - In business data entry, `Enter` must behave like `Tab` in traditional web browsers: it advances focus to the next required cell or input.
   - Text inside the target cell must be **automatically selected** (`select()`) so typing immediately overwrites it without requiring `Backspace`.

2. **The `F3` Omnipresent Lookup ("Contains Search"):**
   - Pressing `F3` on any code field (Customer, Vendor, Item, Payment Term) opens a high-speed search dropdown.
   - **Crucial Rule:** The search must match **any substring (`LIKE '%test%'`)**, not merely prefixes (`LIKE 'test%'`). Operators often remember a word in the middle of a product name, not the item SKU.
   - Up/Down arrows navigate results; `Enter` commits selection and advances focus.

3. **The `F8` Multi-Row Picker:**
   - Pressing `F8` opens a picker to import rows from previous documents (e.g. pulling unbilled Delivery Notes into a Monthly Consolidated Invoice, or pulling items from a Quote into a Sales Order).
   - Spacebar toggles row selection; `Ctrl+A` selects all; `Enter` imports them into the active document.

4. **Esc Key Hierarchy:**
   - Level 1: Close active dropdown / search results.
   - Level 2: Revert uncommitted edits in current grid row.
   - Level 3: Prompt to cancel document.

5. **`Ctrl + Enter` (or `F10`): Instant Commit:**
   - Bypasses remaining non-mandatory fields, triggers instant validation, commits the document to the database, and prompts for print/email.

---

## 2. Anti-Crash Autosave & Draft Protection

1. **Local Persistent Storage:**
   - As the operator types, state (`header`, `lines`, `cursor_position`) is debounced (e.g. every 500ms) to persistent local storage (IndexedDB or LocalStorage key `erp.active_draft`).
2. **`beforeunload` Guard:**
   - If the operator accidentally presses `F5` (Refresh), `Ctrl+W` (Close Tab), or clicks a navigation link while an uncommitted document has lines, intercept the event with `window.addEventListener('beforeunload', ...)`.
3. **Draft Recovery Prompt on Startup:**
   - On application startup or when opening "New Document", check for an active draft.
   - If found, prompt the operator:
     > *"An uncommitted draft from [Date Time] was found for Customer [Name] with [N] rows. Do you want to resume or discard it?"*

---

## 3. Direct Hardware Printing (Bypass Print Dialogs)

1. **The Problem:** The standard browser `window.print()` dialog requires the operator to click "Print", select a printer, and confirm paper size every single time. In a warehouse printing 500 delivery notes a day, this is unacceptable.
2. **The Native Architecture:**
   - The backend desktop shell (Tauri / Rust or Local Agent daemon) communicates directly with the operating system print spooler:
     - **Windows:** Win32 Print Spooler API (`winspool.drv` / `OpenPrinter`, `StartDocPrinter`, `WritePrinter`).
     - **Linux / macOS:** CUPS raw queue.
     - **Thermal / Label Printers:** Raw ESC/POS commands or ZPL (Zebra Programming Language) sent directly via TCP/IP or raw USB COM port.
   - Invoices and shipping labels print silently and instantly the moment the document is committed.
