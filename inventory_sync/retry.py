from book_core import BookFormat
from .foundations import RetryPolicy

# Chapter 1: InventorySync
# Business Logic

@BookFormat(
    chapter="InventorySync",
    subtopic="Kafka-Consumer-Retry",
    status="Proposed",
    preface="Handles retries for failed Kafka inventory messages.",
    references=["Foundations:RetryPolicy"], # Graph Edge!
    
    # Partial Metadata (Human mode) - The Librarian will flag this as "TBD" in summary
    # In a real workflow, the 'Hydrate' step would fill these.
    # We leave them blank here to demonstrate the 'Partial' support.
)
def retry_failed_message(message, retry_policy: RetryPolicy):
    """Retry logic with backoff and max attempts."""
    if retry_policy.should_retry(message):
        retry_policy.schedule(message)
