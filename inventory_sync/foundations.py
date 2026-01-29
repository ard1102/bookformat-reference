from book_core import BookFormat

# Chapter 0: Foundations
# Defines shared primitives used by the business logic.

@BookFormat(
    chapter="Foundations",
    subtopic="RetryPolicy",
    status="Implemented",
    preface="Defines the standard backoff and retry policy interface.",
    
    # System fields filled by Agent
    chapter_number=0,
    subtopic_number="0.1",
    page_number=1,
    author="System_Architect",
    last_revised="2026-01-29",
    solid_rating="A",
    how_to_use="Inherit from this class."
)
class RetryPolicy:
    def should_retry(self, context):
        return True
    
    def schedule(self, context):
        pass

