from backend.app.services.categorization.strategies import KeywordStrategy, PatternStrategy
from backend.app.services.categorization.factory import CategorizerFactory


def test_keyword_strategy_categorizes_urgent():
    """Test urgent keyword detection"""
    strategy = KeywordStrategy()
    result = strategy.categorize("URGENT: Fix production bug", "Critical issue")
    assert result == "urgent"


def test_keyword_strategy_categorizes_work():
    """Test work keyword detection"""
    strategy = KeywordStrategy()
    result = strategy.categorize("Schedule meeting with client", None)
    assert result == "work"


def test_keyword_strategy_categorizes_personal():
    """Test personal keyword detection"""
    strategy = KeywordStrategy()
    result = strategy.categorize("Buy groceries", "Shopping list")
    assert result == "personal"


def test_keyword_strategy_defaults_to_personal():
    """Test default categorization"""
    strategy = KeywordStrategy()
    result = strategy.categorize("Random task", "No specific keywords")
    assert result == "personal"


def test_pattern_strategy_detects_urgent_punctuation():
    """Test urgent detection via punctuation patterns"""
    strategy = PatternStrategy()
    result = strategy.categorize("Fix this now!!!", None)
    assert result == "urgent"


def test_factory_creates_keyword_strategy():
    """Test Factory pattern creates correct strategy"""
    categorizer = CategorizerFactory.create_categorizer("keyword")
    assert isinstance(categorizer, KeywordStrategy)


def test_factory_creates_pattern_strategy():
    """Test Factory pattern creates pattern strategy"""
    categorizer = CategorizerFactory.create_categorizer("pattern")
    assert isinstance(categorizer, PatternStrategy)


def test_factory_defaults_to_keyword():
    """Test Factory default strategy"""
    categorizer = CategorizerFactory.create_categorizer("unknown")
    assert isinstance(categorizer, KeywordStrategy)
