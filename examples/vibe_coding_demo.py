from book_core import BookFormat

# Scenario 1: The Vibe Coder
# The human just wants to write code. They don't care about page numbers or boilerplate.
# They provide the minimal "Intent" and let the system handle the "Bureaucracy".

@BookFormat(
    chapter="Examples",
    subtopic="Vibe-Feature",
    status="Proposed",
    preface="A quick prototype thrown together to test a user flow.",
    # No page_number, no author, no last_revised. 
    # The Librarian will flag this, and the Agent will fill it later.
)
def rapid_prototype_flow(user_id: str):
    """
    This function was written quickly. 
    The system will index it, so it doesn't get lost.
    """
    print(f"Validating user {user_id}...")
    return True
