from typing import Callable, List, Optional, Union

def BookFormat(
    # Human-Authored Fields (Optional - Intent Driven)
    # Humans MAY provide these. If omitted, the Agent MUST infer them.
    chapter: Optional[str] = None,
    subtopic: Optional[str] = None,
    status: Optional[str] = None,
    preface: Optional[str] = None,
    
    # Graph / Edges (Optional)
    references: Optional[List[str]] = None,
    
    # System / Agent-Filled Fields (Mechanical)
    chapter_number: Optional[int] = None,
    subtopic_number: Optional[str] = None,
    page_number: Optional[int] = None,
    author: Optional[str] = None,
    how_to_use: Optional[str] = None,
    appendix: Optional[str] = None,
    security_level: str = "Medium", 
    last_revised: Optional[str] = None,
    solid_rating: Optional[str] = None,
):
    """
    The Canonical BookFormat Decorator.
    
    Args:
        chapter (str, optional): The conceptual chapter. Agent infers if missing.
        subtopic (str, optional): The specific section. Agent infers if missing.
        status (str, optional): Lifecycle state. Agent defaults to "Proposed".
        preface (str, optional): Description. Agent generates from code if missing.
        ...
    """
    def decorator(func: Callable) -> Callable:
        setattr(func, "_book_format", {
            "chapter": chapter,
            "subtopic": subtopic,
            "status": status,
            "preface": preface,
            "references": references or [],
            "chapter_number": chapter_number,
            "subtopic_number": subtopic_number,
            "page_number": page_number,
            "author": author,
            "how_to_use": how_to_use,
            "appendix": appendix,
            "security_level": security_level,
            "last_revised": last_revised,
            "solid_rating": solid_rating,
        })
        return func
    return decorator
