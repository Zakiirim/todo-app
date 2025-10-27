from backend.app.services.categorization.strategies import (
    CategorizationStrategy,
    KeywordStrategy,
    PatternStrategy,
)


class CategorizerFactory:
    """
    Factory pattern: creates appropriate categorizer based on strategy type.

    Centralizes categorizer creation logic and allows easy addition of new strategies.
    """

    @staticmethod
    def create_categorizer(strategy_type: str = "keyword") -> CategorizationStrategy:
        """
        Creates and returns a categorization strategy instance.

        Args:
            strategy_type: Type of strategy ('keyword', 'pattern', or future 'ml')

        Returns:
            CategorizationStrategy instance
        """
        strategies = {
            "keyword": KeywordStrategy,
            "pattern": PatternStrategy,
        }

        strategy_class = strategies.get(strategy_type, KeywordStrategy)
        return strategy_class()
