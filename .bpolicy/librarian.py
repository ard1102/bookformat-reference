import ast
import os
import re
import sys
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SUMMARY_FILE = os.path.join(PROJECT_ROOT, "SUMMARY.md")
GRAPH_FILE = os.path.join(PROJECT_ROOT, "SYSTEM_GRAPH.md")
BOOK_CORE_FILE = "book_core.py"
SEMGREP_CONFIG = ".semgrep.yml"

# --- Data Structures ---
class BookEntry:
    def __init__(self, file_path: str, line_no: int, func_name: str, metadata: Dict):
        self.file_path = file_path
        self.line_no = line_no
        self.func_name = func_name
        self.metadata = metadata

    @property
    def chapter(self): return self.metadata.get("chapter")
    @property
    def subtopic(self): return self.metadata.get("subtopic")
    @property
    def page_number(self): return self.metadata.get("page_number")
    @property
    def key(self): return f"{self.chapter}:{self.subtopic}"

# --- The Librarian Protocol Implementation ---

class Librarian:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.entries: List[BookEntry] = []
        self.errors: List[str] = []
        self.max_page_number = 0

    def scan_codebase(self):
        """Scans all .py files for @BookFormat decorators."""
        print(f"📖 Librarian scanning: {self.root_dir}")
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".py") and file != BOOK_CORE_FILE and "librarian.py" not in file:
                    self._parse_file(os.path.join(root, file))
        
        # Sort by page number for history, then chapter/subtopic for index
        self.entries.sort(key=lambda x: (x.page_number if x.page_number else 999999))
        self._validate_integrity()

    def _parse_file(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)
        except Exception as e:
            self.errors.append(f"Syntax Error in {file_path}: {e}")
            return

        rel_path = os.path.relpath(file_path, self.root_dir).replace("\\", "/")

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and getattr(decorator.func, "id", "") == "BookFormat":
                        meta = self._extract_metadata(decorator)
                        entry = BookEntry(rel_path, node.lineno, node.name, meta)
                        self.entries.append(entry)
                        if entry.page_number and isinstance(entry.page_number, int):
                            self.max_page_number = max(self.max_page_number, entry.page_number)

    def _extract_metadata(self, node: ast.Call) -> Dict:
        """Extracts kwargs from the decorator AST."""
        meta = {}
        for keyword in node.keywords:
            # Simple literal evaluation
            if isinstance(keyword.value, (ast.Str, ast.Constant)):
                 meta[keyword.arg] = keyword.value.value
            elif isinstance(keyword.value, ast.Num): # Python < 3.8
                 meta[keyword.arg] = keyword.value.n
            elif isinstance(keyword.value, ast.List):
                # Handle references list
                meta[keyword.arg] = [elt.value for elt in keyword.value.elts if isinstance(elt, (ast.Str, ast.Constant))]
            else:
                meta[keyword.arg] = None # Complex types not supported in this ref impl
        return meta

    def _validate_integrity(self):
        """Checks rules: Page numbers, References."""
        known_keys = {e.key for e in self.entries}
        seen_page_numbers = {}

        for entry in self.entries:
            # Rule: Mandatory Human Fields
            if not entry.chapter or not entry.subtopic:
                self.errors.append(f"Missing Chapter/Subtopic in {entry.file_path}:{entry.func_name}")
            
            # Rule: References must exist
            refs = entry.metadata.get("references") or []
            for ref in refs:
                if ref not in known_keys:
                    self.errors.append(f"Broken Reference: '{ref}' in {entry.func_name} (Target not found)")

            # Rule: Unique Page Numbers
            if entry.page_number is not None:
                if entry.page_number in seen_page_numbers:
                    prev_entry = seen_page_numbers[entry.page_number]
                    self.errors.append(f"Duplicate Page Number {entry.page_number}: {entry.key} conflicts with {prev_entry.key}")
                else:
                    seen_page_numbers[entry.page_number] = entry

            # Warning for partial system fields (in a strict mode, this would be an error)
            if entry.page_number is None:
                print(f"⚠️  Unfilled System Field: page_number for {entry.key} (Needs Hydration)")

    def generate_summary(self):
        """Generates SUMMARY.md."""
        if self.errors:
            # Errors will be printed in main execution block
            return False

        lines = ["# 📘 Project Book Index", "", "> Auto-generated by Librarian. Do not edit.", ""]
        
        # Group by Chapter
        chapters = {}
        for entry in self.entries:
            ch = entry.chapter
            if ch not in chapters: chapters[ch] = []
            chapters[ch].append(entry)

        # Sort Chapters (Foundations first, then alphabetical or by number)
        sorted_chapter_names = sorted(chapters.keys(), key=lambda x: (0 if x == "Foundations" else 1, x))

        for ch in sorted_chapter_names:
            lines.append(f"## Chapter: {ch}")
            for entry in chapters[ch]:
                pn = entry.page_number if entry.page_number else "TBD"
                status = entry.metadata.get("status", "Unknown")
                refs = entry.metadata.get("references")
                ref_str = f" 🔗 -> {refs}" if refs else ""
                
                lines.append(f"- **Page {pn}** · {entry.subtopic} ({status})")
                lines.append(f"  `{entry.func_name}` in [{entry.file_path}]({entry.file_path}){ref_str}")
            lines.append("")

        with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"\n✅ SUMMARY.md updated with {len(self.entries)} entries.")
        return True

    def generate_graph(self):
        """Generates a Mermaid graph of the system dependencies."""
        if self.errors:
            return False

        lines = ["# 🕸️ System Dependency Graph", "", "> Auto-generated by Librarian.", "", "```mermaid", "graph TD"]
        
        # Helper to sanitize node IDs for Mermaid
        def safe_id(key):
            return re.sub(r'[^a-zA-Z0-9]', '_', key)

        # Group by Chapter for subgraphs
        chapters = {}
        for entry in self.entries:
            ch = entry.chapter
            if ch not in chapters: chapters[ch] = []
            chapters[ch].append(entry)

        # Create Nodes (Grouped by Chapter)
        for chapter, entries in chapters.items():
            lines.append(f"    subgraph {safe_id(chapter)} [{chapter}]")
            for entry in entries:
                node_id = safe_id(entry.key)
                status = entry.metadata.get("status", "Proposed")
                
                # Style tweaks based on status
                style = ""
                if status == "Proposed": style = ":::proposed"
                elif status == "Secured": style = ":::secured"
                
                lines.append(f"        {node_id}([{entry.subtopic}]){style}")
            lines.append("    end")

        # Create Edges
        for entry in self.entries:
            source_id = safe_id(entry.key)
            refs = entry.metadata.get("references") or []
            for ref in refs:
                target_id = safe_id(ref)
                lines.append(f"    {source_id} -.-> {target_id}")

        # Styles
        lines.append("")
        lines.append("    classDef proposed stroke:#f9f,stroke-width:2px,stroke-dasharray: 5 5;")
        lines.append("    classDef secured stroke:#0f0,stroke-width:4px;")
        lines.append("```")

        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        print(f"✅ SYSTEM_GRAPH.md generated with dependency visualization.")
        return True

    def hydrate_codebase(self):
        """
        Agentic Capability: Fills in missing System Fields in the source code.
        For this reference implementation, we'll just simulate/log what we would do,
        or actually do it if simple.
        """
        # This is complex to do robustly with Regex, but let's try a simple version for the demo.
        # We assign new page numbers to entries that lack them.
        next_page = self.max_page_number + 1
        
        files_modified = set()
        
        for entry in self.entries:
            if entry.page_number is None:
                # Calculate new fields
                new_page = next_page
                next_page += 1
                new_date = datetime.now().strftime("%Y-%m-%d")
                
                print(f"💧 Hydrating {entry.key} -> Page {new_page}")
                
                # We need to rewrite the file. 
                # NOTE: In a real IDE, we'd use a robust refactoring tool. 
                # Here, we will append a TODO comment to the file to show intent without risking regex corruption.
                # OR we can just rely on the 'Manual/Agent' step to do this.
                pass 

if __name__ == "__main__":
    lib = Librarian(PROJECT_ROOT)
    lib.scan_codebase()
    
    if lib.errors:
        print("\n❌ LIBRARIAN FOUND ERRORS:")
        for e in lib.errors:
            print(f" - {e}")
        print("\n⛔ Build Failed: Documentation integrity compromised.")
        sys.exit(1)
        
    # Run Security Scan
    lib.run_security_scan()
    if lib.errors:
        print("\n❌ SECURITY VIOLATIONS FOUND:")
        for e in lib.errors:
            print(f" - {e}")
        sys.exit(1)

    success_summary = lib.generate_summary()
    success_graph = lib.generate_graph()
    
    if not (success_summary and success_graph):
        sys.exit(1)
    
    sys.exit(0)
