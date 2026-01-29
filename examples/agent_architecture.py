from book_core import BookFormat

# Scenario 2: The Agent Architect
# An AI agent is asked to build a complex payment subsystem.
# It knows it must declare its dependencies explicitly so the graph is valid.

@BookFormat(
    chapter="PaymentSystem",
    subtopic="Payment-Gateway",
    status="Implemented",
    preface="Abstracts the connection to Stripe/PayPal.",
    references=["Foundations:RetryPolicy"], # Links to the core retry logic
    # The Agent is diligent, so it might even fill these if it knows the state,
    # but usually it leaves page_number to the Librarian to avoid conflicts.
    author="Agent-Claude-3.5",
    security_level="High"
)
class PaymentGateway:
    def process(self, amount):
        pass

@BookFormat(
    chapter="PaymentSystem",
    subtopic="Transaction-Logger",
    status="Implemented",
    preface="Logs all financial transactions for audit.",
    references=["PaymentSystem:Payment-Gateway"], # Internal dependency
    author="Agent-Claude-3.5"
)
def log_transaction(tx_id):
    pass
