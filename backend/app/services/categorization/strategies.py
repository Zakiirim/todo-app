from abc import ABC, abstractmethod
from typing import Optional


class CategorizationStrategy(ABC):
    """Strategy pattern: defines interface for different categorization approaches"""

    @abstractmethod
    def categorize(self, title: str, description: Optional[str]) -> str:
        pass


class KeywordStrategy(CategorizationStrategy):
    """
    Keyword-based categorization strategy.

    Analyzes text for category-specific keywords to determine task type.
    """

    URGENT_KEYWORDS = {
        "asap",
        "urgent",
        "emergency",
        "critical",
        "now",
        "immediately",
        "today",
        "deadline",
        "important",
    }

    WORK_KEYWORDS = {
        "meeting",
        "email",
        "report",
        "deadline",
        "project",
        "presentation",
        "call",
        "conference",
        "client",
        "review",
        "document",
        "proposal",
    }

    PERSONAL_KEYWORDS = {
        "buy",
        "home",
        "family",
        "doctor",
        "gym",
        "shopping",
        "vacation",
        "appointment",
        "birthday",
        "dinner",
        "friend",
        "personal",
    }

    def categorize(self, title: str, description: Optional[str]) -> str:
        text = f"{title} {description or ''}".lower()
        words = set(text.split())

        # Check urgent first (highest priority)
        if words & self.URGENT_KEYWORDS:
            return "urgent"

        # Then check work-related
        if words & self.WORK_KEYWORDS:
            return "work"

        # Then check personal
        if words & self.PERSONAL_KEYWORDS:
            return "personal"

        # Default to personal
        return "personal"


class PatternStrategy(CategorizationStrategy):
    """
    Pattern-based categorization strategy.

    Uses regex patterns and text structure to categorize tasks.
    Extensible for future ML-based categorization.
    """

    def categorize(self, title: str, description: Optional[str]) -> str:
        text = f"{title} {description or ''}".lower()

        # Check for urgent indicators (punctuation patterns)
        if "!!!" in text or "!!" in text:
            return "urgent"

        # Check for time-sensitive patterns
        if any(word in text for word in ["deadline", "due", "by"]):
            return "work"

        # Simple fallback to keyword strategy
        keyword_strategy = KeywordStrategy()
        return keyword_strategy.categorize(title, description)
