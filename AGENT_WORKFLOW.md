# 🤖 The Agentic Workflow (The 9-Step Loop)

This document defines the **Executable Model** for Agents operating in this repository. 

> **Core Principle:** The Agent does not start by writing code. It starts by placing the idea inside the book.

---

## Phase 1: Planning (Documentation Mode)

### 1️⃣ User Intent
*   **Input**: User asks for a feature (e.g., "Add retry handling for failed Kafka inventory messages.")
*   **State**: No code, no files, no assumptions.

### 2️⃣ Read the Book
*   **Action**: Load `SUMMARY.md`.
*   **Analysis**:
    *   Identify relevant Chapter(s).
    *   Check for existing Subtopics.
    *   Check Status of related features (`Secured`, `Deprecated`, etc.).
    *   *Self-Correction*: "Does this belong to Chapter 0 (Foundations) or a specific domain?"

### 3️⃣ Write Documentation FIRST
*   **Action**: Propose the `@BookFormat` decorator *before* or *during* writing logic.
*   **Draft**:
    ```python
    @BookFormat() # <--- The Agent will infer Chapter/Subtopic
    ```
    OR
    ```python
    @BookFormat(
        chapter="InventorySync", # Optional hint
        status="Proposed"
    )
    ```
*   **Outcome**: The Agent (or Librarian) will analyze the code to place it in the correct Chapter.

### 4️⃣ Architectural Decision
*   **Evaluate**:
    *   If Subtopic exists + `status=Implemented` -> **Extend**.
    *   If Subtopic exists + `status=Secured` -> **Abort / Escalate**.
    *   If No Subtopic -> **New Page**.
    *   If Cross-cutting -> **Chapter 0**.

---

## Phase 2: Execution (System Mode)

### 5️⃣ Complete Metadata
*   **Action**: Hydrate the System Fields.
    *   `page_number` = `max(existing) + 1`
    *   `references` = `["Foundations:RetryPolicy"]` (Define the graph edges)
    *   `appendix` = `tests/test_retry.py` (Define the test obligation)

### 6️⃣ Implement Code (SOLID & SATA)
*   **Action**: Write the Python logic inside the documented slot.
*   **Constraint**: Logic must match the `preface` and `references`.
*   **SOLID Check**:
    *   Is this function doing too much? (SRP) -> Split it.
    *   Does it rely on a concrete class instead of an interface? (DIP) -> Fix references.

### 7️⃣ Write Tests (Appendix Obligation)
*   **Action**: Create the file specified in `appendix`.
*   **Constraint**: Tests must verify the behavior described in `preface`.
*   **Coverage**: Ensure standard paths and edge cases are covered.

---

## Phase 3: Verification (Enforcement)

### 8️⃣ Run Enforcement
*   **Mandatory Commands**:
    1.  `python librarian.py` (Check structural integrity & regenerate Index/Graph)
    2.  `ruff check .` (Static Analysis)
    3.  `pytest` (Behavioral correctness)
    4.  `semgrep` (Security Audit - if available)

### 9️⃣ Deployment
*   **State**:
    *   Architecture is correct.
    *   Docs are consistent.
    *   Security rules are enforced.
    *   **Production Standards Met** (See `PRODUCTION_STANDARDS.md`).
*   **Action**: Commit and Ship.

---

## Summary for Agents

**Your Loop:**
`Think` → `Document` → `Decide` → `Implement` → `Verify` → `Ship`

**The Inversion:**
Do not write code to solve the problem. Write documentation to *frame* the problem, then write code to *fulfill* the documentation.
