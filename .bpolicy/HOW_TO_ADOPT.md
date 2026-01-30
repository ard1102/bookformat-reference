# 🛠️ How to Adopt BookFormat

This guide explains how to integrate the BookFormat protocol into your project.

---

## Scenario 1: New Project (Greenfield)

**Goal**: Build a system that is "Agent-Ready" from Day 1.

1.  **Clone the Reference**:
    Download `book_core.py` and `librarian.py` into your project root.

2.  **Add the Specs**:
    Copy `BOOKFORMAT_SPEC.md` and `AGENT_RULES.md`. These files are crucial instructions for any AI agent (Cursor, Trae, Copilot) you work with.

3.  **Initialize Chapter 0**:
    Create a file `foundations.py` and define your first shared utility (e.g., a Logger or Config loader).
    ```python
    @BookFormat(chapter="Foundations", subtopic="Config", status="Implemented")
    class Config: ...
    ```

4.  **Run the Librarian**:
    ```bash
    python .bpolicy/librarian.py
    ```
    You now have a `SUMMARY.md` and `SYSTEM_GRAPH.md`.

---

## Scenario 2: Existing Project (Brownfield)

**Goal**: Tame a chaotic codebase and make it understandable for Agents.

**Strategy**: Do NOT try to tag everything at once. Use the "Strangler Fig" pattern.

1.  **Install the Core**:
    Copy the core files (`book_core.py`, `librarian.py`) to your root.

2.  **Identify Core Domains**:
    Pick *one* critical module (e.g., `UserAuth`).

3.  **Tag the Entry Points**:
    Add `@BookFormat` to the main public functions/classes of that module.
    ```python
    @BookFormat(chapter="UserAuth", subtopic="Login", status="Secured")
    def login(): ...
    ```

4.  **Hydrate**:
    Run `python librarian.py`.
    *Result*: You now have a "Partial Map" of your system.

5.  **Iterate**:
    As you touch old files, add `@BookFormat` tags. Over time, the "Dark Matter" of your codebase becomes illuminated in the `SYSTEM_GRAPH.md`.

---

## 🧹 Cleanup (Post-Adoption)

Once you have copied `.bpolicy/` and `SUMMARY.md` to your project, you can remove the reference artifacts.

**Safe to Delete:**
*   `pyproject.toml` (Unless you want to use our Ruff config)
*   `inventory_sync/` (Demo Code)
*   `examples/` (Demo Code)
*   `.gitignore` (Use your own)

**Command:**
```bash
# Linux/Mac
rm -rf inventory_sync examples pyproject.toml .gitignore

# Windows (PowerShell)
Remove-Item -Recurse -Force inventory_sync, examples, pyproject.toml, .gitignore
```

**MUST KEEP:**
*   `.bpolicy/` (The Engine)
*   `SUMMARY.md` (The Map)

**System Prompt Injection:**
Add the contents of `AGENT_RULES.md` and `AGENT_WORKFLOW.md` to your Agent's "Custom Instructions" or "System Prompt".

**Key Instruction**:
> "You are working in a BookFormat repository. Before writing code, you must check SUMMARY.md. All new functions must have a @BookFormat decorator."

---

## 📦 CI/CD Integration

To enforce the protocol, add a check to your GitHub Actions / GitLab CI. The Librarian is now **CI-Ready** and will exit with code 1 if it finds:
*   Broken References
*   Duplicate Page Numbers
*   Missing Mandatory Fields
*   Syntax Errors

```yaml
steps:
  - name: Run Librarian (Quality Gate)
    run: python .bpolicy/librarian.py
    # Fails immediately if docs are broken

  - name: Check for Uncommitted Changes
    run: |
      git diff --exit-code SUMMARY.md SYSTEM_GRAPH.md
      # If this fails, it means the developer didn't commit the updated index.
```
