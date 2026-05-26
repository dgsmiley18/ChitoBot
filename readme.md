# ChitoBot

ChitoBot is a Discord bot developed in Python using the [discord.py](https://discordpy.readthedocs.io/) library. It provides various administrative and community features for Discord servers, such as automatic welcome messages, role assignments, message logging, and modular command extensions via cogs.

## Features

- **Welcome Messages**: Sends a welcome message when a new member joins.
- **Farewell Notifications**: Notifies the channel when a member leaves.
- **Automatic Role Assignment**: Assigns roles to new members upon joining.
- **Message Logging**: Logs deleted and edited messages with content in a dedicated channel.
- **Modular Command Support**: Add or manage commands easily using cogs (extensions).
- **Command Synchronization**: Keeps commands synced on startup.

## Prerequisites

- Python 3.8 or higher
- discord.py

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/dgsmiley18/ChitoBot.git
    cd ChitoBot
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
    If there is no `requirements.txt`, install manually:
    ```sh
    pip install discord.py toml
    ```

3. **Configure `config.toml`**:
    ```toml
    [config]
    token = "YOUR_DISCORD_BOT_TOKEN"
    ```
    Replace `YOUR_DISCORD_BOT_TOKEN` with your actual Discord bot token.

4. *(Optional)* Create the `cogs/` directory to add modular features:
    ```sh
    mkdir cogs
    ```

## Usage

Run the bot with Python:
```sh
python bot.py
```

## Running with Docker

1. **Build the Docker image**:
    ```sh
    docker build -t chitobot .
    ```

2. **Run the container**:
    ```sh
    docker run -v $(pwd)/config.toml:/app/config.toml chitobot
    ```
    > Make sure your `config.toml` is accessible to the container; adjust the path if needed.

3. *(Optional)* If you use a `cogs/` folder for extensions:
    ```sh
    docker run -v $(pwd)/config.toml:/app/config.toml -v $(pwd)/cogs:/app/cogs chitobot
    ```

## Customization

- Add your own commands or event handlers in `bot.py` or as individual modules in the `cogs/` folder.
- Review the [discord.py documentation](https://discordpy.readthedocs.io/) for information on extensions and advanced features.

## License

MIT License. Feel free to use, modify, and share!

---

> Made with ❤️ by [dgsmiley18](https://github.com/dgsmiley18)