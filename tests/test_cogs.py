import inspect
from unittest.mock import MagicMock

from cogs import fun, moderation
from cogs.fun import Fun
from cogs.moderation import Moderation


def test_cogs_setup_functions():
    """Ensure each cog file exports a valid async setup function."""
    assert hasattr(fun, "setup")
    assert inspect.iscoroutinefunction(fun.setup)
    assert hasattr(moderation, "setup")
    assert inspect.iscoroutinefunction(moderation.setup)


def test_cog_initialization():
    """Test that cogs can be instantiated with a mock bot object."""
    mock_bot = MagicMock()
    mock_bot.log_channel_id = 0
    mock_bot.latency = 0.042

    fun_cog = Fun(mock_bot)
    mod_cog = Moderation(mock_bot)

    assert fun_cog.bot == mock_bot
    assert mod_cog.bot == mock_bot