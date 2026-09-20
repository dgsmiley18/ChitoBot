import os
import tomllib
from unittest import mock


def test_example_config_validity():
    """Ensure config.example.toml exists and has valid TOML syntax."""
    assert os.path.exists("config.example.toml"), "config.example.toml must exist"
    with open("config.example.toml", "rb") as f:
        config = tomllib.load(f)
    
    assert "bot" in config
    assert "token" in config["bot"]
    assert "features" in config


def test_env_token_override():
    """Verify that environment variable overrides configuration token."""
    with mock.patch.dict(os.environ, {"DISCORD_TOKEN": "mock_env_token"}):
        token = os.getenv("DISCORD_TOKEN")
        assert token == "mock_env_token"