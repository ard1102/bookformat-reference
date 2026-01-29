# AGENT RULES (NON-NEGOTIABLE)

## RULE 1: The Human/System Split
*   **Inputs**: You MAY receive instructions to write code with only `chapter`, `subtopic`, `status`, `preface`.
*   **Outputs**: You MUST ensure the final code committed to the repo has **FULL** metadata.
    *   If you are writing the code, you must calculate the `page_number` (max + 1) and other system fields.
    *   OR you must run the `librarian` tool to fill them.

## RULE 2: Introduction vs. Execution
*   **Do not confuse Chapter order with Execution order.**
*   Chapters group concepts. `references` show execution dependencies.
*   If you need to use a utility, check if it exists in **Chapter 0: Foundations**. If not, propose it there.

## RULE 3: Immutable History
*   `page_number` is a history log. NEVER change the `page_number` of an existing feature.
*   New features ALWAYS get `max(all_pages) + 1`.

## RULE 4: Security Barriers
*   If `status == "Secured"`: **STOP**. You cannot edit this without specific "Break Glass" authorization.
*   If `status == "Deprecated"`: **STOP**. Do not modify logic. Only delete references TO it.

## RULE 5: Referential Integrity
*   If you add `references=["Auth:Login"]`, you MUST verify that `Auth:Login` exists in the `SUMMARY.md`.

## RULE 6: The Librarian is Law
*   After any change, run `python librarian.py`.
*   If it fails, fix the metadata. Do not force-merge.
