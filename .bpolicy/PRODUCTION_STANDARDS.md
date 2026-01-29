# 🏭 Production Standards & Quality Gates

> "BookFormat doesn't just index code; it enforces quality."

This document defines how **SOLID**, **SDLC**, **Testing**, and **Static Analysis** are integrated into the BookFormat governance layer.

---

## 1. SOLID Principles via Metadata

BookFormat translates abstract SOLID principles into concrete, enforceable structural rules.

| Principle | BookFormat Implementation | Enforcement |
| :--- | :--- | :--- |
| **S**ingle Responsibility | **One Subtopic = One Concept.** A Page should not do two things. If the `preface` needs "and", split it. | **Agent Check**: If a function grows too large, propose splitting into new Subtopics. |
| **O**pen/Closed | **Status locking.** Once a Page is `Secured`, you cannot modify it. You must create a *new* Page that references/extends it. | **Librarian**: Rejects edits to `Secured` files without "Break Glass" protocol. |
| **L**iskov Substitution | **Foundations Contracts.** Classes in Chapter 0 must have rigid interfaces. | **Type Checker**: Strict MyPy/Pyright on Chapter 0. |
| **I**nterface Segregation | **Granular Chapters.** Don't dump everything in `Utils`. Use specific Chapters (e.g., `PaymentUtils`, `DateUtils`). | **Review**: "Foundations" should be small primitives only. |
| **D**ependency Inversion | **Explicit References.** High-level logic (`InventorySync`) depends on abstractions (`Foundations`), declared in `references`. | **Graph Check**: Cycles in `references` are forbidden. |

---

## 2. SDLC (Software Development Life Cycle)

The `status` field drives the SDLC state machine.

### Phase 1: The Proposal (`status="Proposed"`)
*   **Goal**: Design & Planning.
*   **Requirements**:
    *   `preface` is written (The "Why").
    *   `references` are drafted (The "How").
    *   **No implementation code required.**
*   **Gate**: Peer/Agent Review of the architecture.

### Phase 2: Implementation (`status="Implemented"`)
*   **Goal**: Working Code.
*   **Requirements**:
    *   Code fulfills `preface`.
    *   `appendix` points to valid tests.
    *   Linters (Ruff) pass.
*   **Gate**: CI Pipeline Green.

### Phase 3: Hardening (`status="Secured"`)
*   **Goal**: Long-term Stability.
*   **Requirements**:
    *   `security_level` is set.
    *   `solid_rating` is "A" or "S".
    *   No "TODO" comments.
    *   100% Test Coverage.
*   **Gate**: Security Audit / Senior Approval.

### Phase 4: End of Life (`status="Deprecated"`)
*   **Goal**: Safe Removal.
*   **Requirements**:
    *   No *active* pages reference this page.
    *   `how_to_use` updated with migration path.

---

## 3. SATA (Static Analysis, Testing, Auditing) Protocol

To ensure "Production Readiness", the following tools are mandatory. The Librarian acts as the orchestrator.

### A. Static Analysis (The Linter)
*   **Tools**: `ruff`, `mypy`.
*   **Rule**: You cannot commit `status="Implemented"` code if linters fail.
*   **BookFormat Integration**:
    *   The Agent runs `ruff check .` before setting `status="Implemented"`.
    *   If `solid_rating="S"`, strict typing (`mypy --strict`) is enforced.

### B. Testing (The Appendix)
*   **Tools**: `pytest`.
*   **Rule**: Every Book Entry MUST have an `appendix` pointing to its test file.
*   **BookFormat Integration**:
    *   If `appendix` is missing, Librarian flags as **Incomplete**.
    *   If `appendix` exists but file is missing, Librarian flags as **Broken**.
    *   **Agent Workflow**: The Agent reads the `preface` to generate the test cases in the `appendix`.

### C. Auditing (The Governance)
*   **Tools**: `semgrep`, `librarian.py`.
*   **Rule**: Security rules defined in `.semgrep.yml` must pass.
*   **BookFormat Integration**:
    *   High-risk chapters (e.g., `SecurityCore`) trigger extra Semgrep rules.
    *   Librarian verifies that `references` do not violate architectural boundaries (e.g., `UI` chapter calling `Database` chapter directly).

---

## 4. Definition of "Production Ready"

A feature is **Production Ready** only when:

1.  **Metadata is Complete**: No `None` fields (System-hydrated).
2.  **Graph is Healthy**: No cycles, no broken references.
3.  **Tests Exist**: `appendix` file exists and passes.
4.  **Lint Free**: `solid_rating` matches the Linter output.
5.  **Status is Accurate**: Code matches the declared `status`.

> **The Result**: You don't just ship "code". You ship a **verified, documented, compliant chapter** of the system.
