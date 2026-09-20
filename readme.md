# 🤖 ChitoBot

**A lightweight, modular, and self-hostable Discord bot powered by Python and discord.py.**




[](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Configuration](#-configuration) • [Docker Deployment](#-docker-deployment) • [Commands](#-available-commands)



---

## 📖 Overview

**ChitoBot** is designed from the ground up for server administrators and developers seeking a clean, dependable bot for single or multi-server hosting. Built with modern `discord.py` 2.x paradigms, it supports slash commands (`app_commands`), modular cogs, dynamic permission checks, and robust logging with **zero hardcoded IDs**.

---

## ✨ Features

- 🛡️ **Comprehensive Moderation:** Built-in safeguards, timeout/mute management, purge utility, and automated DM notifications prior to disciplinary actions.
- 📜 **Audit & Message Logging:** Real-time event dispatches for deleted and edited messages formatted into clean embeds.
- 🚪 **Server Gatekeeping:** Configurable welcome and farewell notices with automated newcomer role assignment (*Auto-Role*).
- 🧩 **Modular Cog Architecture:** Features are cleanly separated into isolated cogs for easy maintenance and extensibility.
- ⚙️ **Config-Driven & Flexible:** Toggle optional features on/off simply by setting their ID to `0` in `config.toml`.
- 🐳 **Container Native:** Optimized multi-stage Docker builds with support for environment variable injection.

---

## 📋 Requirements

* **Python 3.11+**
* A registered **Discord Application** and **Bot Token** via the Discord Developer Portal
* **Privileged Gateway Intents** enabled in your developer dashboard:
  * `Server Members Intent`
  * `Message Content Intent`

---

## 🚀 Quick Start

### 1. Clone & Setup Virtual Environment

```bash
# Clone the repository
git clone https://github.com/dgsmiley18/ChitoBot.git
cd ChitoBot

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install package dependencies
pip install .
```

### 2. Configuration

Copy the provided template and add your credentials:

```bash
cp config.example.toml config.toml
```

Edit `config.toml` to suit your server setup:

```toml
[bot]
token = "YOUR_DISCORD_BOT_TOKEN"
prefix = "!"

[guild]
# Primary guild ID for instant local slash command registration.
# Set to 0 to enable global command synchronization across all servers.
guild_id = 0

[features]
# Feature toggles: set any unused ID to 0 to safely disable it
welcome_channel_id = 0
auto_role_id = 0
log_channel_id = 0
```

### 3. Launch

```bash
python bot.py
```

---

## 🐳 Docker Deployment

ChitoBot can be deployed in seconds using Docker or Docker Compose.

### Using Docker CLI

```bash
# Build the image
docker build -t chitobot .

# Run with mounted config
docker run -d \
  --name chitobot \
  --restart unless-stopped \
  -v "$(pwd)/config.toml:/app/config.toml:ro" \
  chitobot
```

### Using Docker Compose (Recommended)

Create a `docker-compose.yml` file:

```yaml
services:
  chitobot:
    build: .
    container_name: chitobot
    restart: unless-stopped
    volumes:
      - ./config.toml:/app/config.toml:ro
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN:-}
```

Run in the background:

```bash
docker compose up -d
```

---

## 🛠️ Available Commands

### 🛡️ Moderation (`cogs/moderation.py`)

| Command | Arguments | Permissions | Description |
| :--- | :--- | :--- | :--- |
| `/ban` | `[reason]` | `Ban Members` | Bans a member or user from the server with DM notice and audit logging. |
| `/mute` |  `[reason]` | `Moderate Members` | Applies a temporary timeout to a member. |
| `/purge` | `[reason]` | `Manage Messages` | Deletes up to 100 recent messages from the current channel. |

### 🎈 Fun & Utilities (`cogs/fun.py`)

| Command | Arguments | Description |
| :--- | :--- | :--- |
| `/ping` | *None* | Displays websocket latency in milliseconds. |
| `/pfp` | `[member]` | Displays the full-size profile avatar of yourself or a specified user. |
| `/userinfo` | `[member]` | Shows detailed account information, badges, join timestamps, and roles. |

---

## 📂 Project Structure

```text
ChitoBot/
├── cogs/
│   ├── fun.py               # Fun, profile, and user diagnostic commands
│   └── moderation.py        # Moderation utilities and audit event logs
├── bot.py                   # Client entrypoint, intent configuration, and event listeners
├── config.example.toml      # Configuration template with field descriptions
├── Dockerfile               # Production-ready slim container definition
├── pyproject.toml           # PEP 518/621 dependency & package metadata
└── README.md
```

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to check the issues page.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.