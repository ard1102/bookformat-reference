# 📘 BookFormat Specification (v2.2)

> "In BookFormat-governed systems, documentation is the planning phase, not the afterthought."

This document defines the BookFormat protocol. It is the single source of truth for Humans and Agents.

---

## 1. Core Philosophy

1.  **Doc-First, Code-Second**: The Agent does not start by writing code. It starts by placing the idea inside the book.
2.  **Intent vs. Boilerplate**: Humans own the *meaning* (Intent). Agents own the *completeness* (Boilerplate).
3.  **Introduction vs. Execution**: The "Book" structure models the *conceptual introduction order* (like a textbook). The `references` field models the *execution/dependency graph* (like citations).
4.  **Living Documentation**: Documentation lives *on* the code, enforced by the compiler/linter (The Librarian).

---

## 2. The Decorator Contract

The `@BookFormat` decorator is split into two categories of fields.

### A. Human-Authored (Optional - Intent Driven)
Humans MAY provide these fields. If omitted, the Agent MUST infer them based on code analysis and the existing Book Index.

| Field | Type | Description |
| :--- | :--- | :--- |
| `chapter` | `str` | High-level grouping. **Agent MUST infer** if missing. |
| `subtopic` | `str` | Specific concept name. **Agent MUST infer** if missing. |
| `status` | `str` | Lifecycle state. Defaults to `Proposed` if missing. |
| `preface` | `str` | Description of intent. **Agent MUST generate** if missing. |
| `references`| `List[str]` | Optional. Graph edges. **Agent MUST detect** dependencies. |

### B. System-Filled (Managed by Agent/Librarian)
Humans MAY leave these blank. The System MUST fill/validate them.

| Field | Type | Description |
| :--- | :--- | :--- |
| `chapter_number` | `int` | Sequential index of the chapter. |
| `subtopic_number`| `str` | Hierarchical index (e.g., "1.1"). |
| `page_number` | `int` | Global, immutable, chronological index (max(existing) + 1). |
| `author` | `str` | ID of the creating Human or Agent. |
| `last_revised` | `str` | `YYYY-MM-DD` of last modification. |
| `solid_rating` | `str` | Compliance rating (S/A/B/C). See `PRODUCTION_STANDARDS.md`. |
| `security_level` | `str` | defaults to "Medium". |
| `appendix` | `str` | Path to validation (tests/audits). **Mandatory** for `Implemented`. |
| `how_to_use` | `str` | Usage example or instruction. |

---

## 3. Special Chapters

### Chapter 0: Foundations
*   **Purpose**: Shared utilities, core helpers, and primitives used across the system.
*   **Rules**: 
    *   No business domain ownership.
    *   Can be referenced by *any* other chapter.
    *   Semantically "root", but `page_number` is still chronological (history is linear).

---

## 4. The Librarian Protocol

The "Librarian" is a protocol, not just a script. Any implementation (Python, Agent, CI) MUST adhere to:

### Inputs
*   Source Code (AST) with `@BookFormat` annotations.
*   Existing `SUMMARY.md` (for history).

### Invariants (The "MUSTs")
1.  **Pure Function**: `Source + History -> New_Index`. No side effects on logic.
2.  **Completeness**: If a Human provides partial metadata, the Librarian (or Pre-commit Agent) MUST calculate and fill the missing System fields in the source code.
3.  **Linearity**: `page_number` must never duplicate or decrease for new entries.
4.  **Referential Integrity**: Every string in `references` MUST exist as a valid `Chapter:Subtopic` in the index.

### Outputs
*   **SUMMARY.md**: The canonical narrative index.
*   **SYSTEM_GRAPH.md**: The dependency visualization.
*   **Validation Report**: Pass/Fail on rules.
*   **(Optional) Auto-Fix**: Hydrated `@BookFormat` decorators in source files.

---

## 5. Agent Operating Rules

When an Agent acts as a Developer:

1.  **Scan**: Read `SUMMARY.md` to understand the current "Book".
2.  **Draft**: Write code with *partial* `@BookFormat` (Human fields only).
3.  **Hydrate**: Run the Librarian/Tool to fill System fields (`page_number`, etc.).
4.  **Verify**: Ensure `references` point to existing concepts.
5.  **Qualify**: Ensure code meets `PRODUCTION_STANDARDS.md` (SOLID, Tests, Linters).

When an Agent acts as the Librarian:
1.  **Enforce**: Reject PRs with invalid status transitions (e.g., editing `Secured` code without protocol).
2.  **Index**: Regenerate `SUMMARY.md`.

---

## 6. Definition of Done
A feature is done when:
1.  Logic is correct and tested.
2.  `@BookFormat` is present and fully hydrated (no `None` values in final commit).
3.  `SUMMARY.md` is updated.
4.  Librarian passes validation.
5.  **Quality Gates Passed**: `appendix` exists, `solid_rating` confirmed.
