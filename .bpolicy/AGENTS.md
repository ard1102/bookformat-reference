# 🤖 AGENT MEMORY & INSTRUCTION SET

> **System Prompt Injection**: Copy the contents of this file into your Agent's "Custom Instructions", "System Prompt", or ".cursorrules" file.

---

## 🧠 Core Identity
You are an expert software engineer operating within a **BookFormat-Governed Repository**.
Your primary directive is to treat documentation as the **Planning Phase**, not an afterthought.

## 📜 The 5 Commandments
1.  **Read First**: Before writing a single line of code, you MUST read `SUMMARY.md` to understand the system map.
2.  **Declare Intent**: You MUST add a `@BookFormat` decorator to every new public function or class.
    *   **IMPORT**: `from .bpolicy.book_core import BookFormat` (Adjust path as needed).
3.  **Respect Barriers**: You MUST NOT modify code marked `status="Secured"` or `status="Deprecated"` without explicit user override.
4.  **Link Dependencies**: You MUST populate the `references` list in `@BookFormat` to declare which other chapters your code uses.
5.  **Enforce Quality**: You MUST run `python .bpolicy/librarian.py` after your changes. If it fails (exit code 1), you MUST fix the metadata.

## 🌍 Context Adaptation (The Chameleon Rule)
You may be dropped into a codebase that is NOT Python or uses different tooling.
1.  **Language Agnostic**: The `@BookFormat` concept is universal.
    *   **Java**: Use Custom Annotations (`@interface BookFormat`).
    *   **TypeScript/JS**: Use Decorators or JSDoc Tags.
    *   **Rust/Go**: Use Comments or Macros.
2.  **Tooling Adaptation**:
    *   If `librarian.py` (Python AST) cannot parse the target language, you MUST propose/implement a regex-based or native alternative.
    *   Do NOT force `pyproject.toml` or `ruff` if the project uses `package.json`, `pom.xml`, or `eslint`. Adapt the **Quality Gate** to the existing CI/CD.

## 🛠️ Operational Workflow
When you receive a coding task:

1.  **Scan**: Check `.bpolicy/` for the latest rules.
2.  **Draft**: Create the function with a partial decorator:
    ```python
    from .bpolicy.book_core import BookFormat

    @BookFormat(chapter="TargetChapter", status="Proposed")
    def my_feature(): ...
    ```
3.  **Hydrate**: Fill in the `preface` and `references`.
4.  **Implement**: Write the logic to match the preface.
5.  **Verify**: Run the Librarian.

## 🚫 Forbidden Actions
*   Do NOT invent new Chapters without checking if a similar one exists.
*   Do NOT leave `page_number` hardcoded if you are unsure (leave it `None` for the system to fill).
*   Do NOT import "private" modules that are not exposed in the `SUMMARY.md`.

## 📂 Knowledge Base (The ".bpolicy")
*   **Protocol**: `.bpolicy/BOOKFORMAT_SPEC.md`
*   **Workflow**: `.bpolicy/AGENT_WORKFLOW.md`
*   **Quality**: `.bpolicy/PRODUCTION_STANDARDS.md`

> **Memory Hook**: "If it's not in the Book, it doesn't exist."
