# 📘 BookFormat: The Documentation Enforcement Protocol

> **"Documentation is not an output. Documentation is the planning phase."**

**BookFormat** is a governance layer for Agentic IDEs and Human-AI Teams. It treats your codebase as a linear book, enforcing structure, dependency graphs, and documentation compliance *before* code is committed.

---

## 🚀 Why BookFormat?

### For Humans ("Vibe Coders")
*   **Flow State**: Write code with minimal tags (`@BookFormat(status="Proposed")`). The system handles the organization.
*   **No Drift**: The `Librarian` ensures your docs and architecture never fall out of sync with the code.

### For AI Agents
*   **Context Map**: `SUMMARY.md` provides a token-efficient map of the entire system.
*   **Safety Rails**: `status="Secured"` tells Agents "Do Not Touch" without needing complex prompts.
*   **Graph Awareness**: Explicit `references` prevent circular dependencies and architectural spaghetti.

---

## 📂 Repository Structure

This repository is a **Reference Implementation**. You are meant to **Fork** or **Copy** the core patterns.

```text
.
├── .bpolicy/               # 🤖 Agent Policy & Governance Docs
│   ├── AGENT_RULES.md      # Rules for Agents
│   ├── AGENT_WORKFLOW.md   # The 9-Step Process
│   ├── BOOKFORMAT_SPEC.md  # The Protocol Spec
│   └── ...
├── book_core.py            # The @BookFormat decorator (The Contract)
├── librarian.py            # The Enforcer (Generates Index & Graph)
└── SUMMARY.md              # The Auto-Generated Index
```

---

## 🛠️ How to Adopt

### Option A: Start Fresh (Recommended)
1.  Fork this repository.
2.  Delete the `inventory_sync/` and `examples/` folders.
3.  Run `python librarian.py` to reset the index.
4.  Start coding!

### Option B: Add to Existing Repo
1.  Copy `book_core.py` and `librarian.py` to your root.
2.  Copy the `.bpolicy/` folder to your root.
3.  Add `@BookFormat` to your critical entry points.
4.  Run `python librarian.py` to generate your first graph.

See [.bpolicy/HOW_TO_ADOPT.md](.bpolicy/HOW_TO_ADOPT.md) for a detailed migration guide.

---

## ⚡ Quick Start

1.  **Install Dependencies** (Standard Python)
    ```bash
    # No heavy dependencies required for the core protocol!
    # Librarian uses standard library 'ast'.
    ```

2.  **Run the Librarian**
    ```bash
    python librarian.py
    ```
    *Check `SUMMARY.md` and `SYSTEM_GRAPH.md` to see the results.*

3.  **Visualize the Graph**
    *   Open `SYSTEM_GRAPH.md` in an editor that supports Mermaid.js (like VS Code or GitHub).

---

## 📜 The Rules

1.  **Doc-First**: Define the `@BookFormat` intent before writing logic.
2.  **Linear History**: Pages are chronological (`page_number`).
3.  **Explicit Edges**: Dependencies must be declared in `references`.

*Read [.bpolicy/BOOKFORMAT_SPEC.md](.bpolicy/BOOKFORMAT_SPEC.md) for the full protocol.*
