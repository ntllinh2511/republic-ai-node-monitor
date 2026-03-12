# 🤖 Republic AI Node & Validator Monitor (Telegram Bot)

A high-performance, lightweight community tool designed for [Republic AI](https://republic.ai/) node operators. This bot allows you to monitor your node infrastructure and validator health directly through Telegram, ensuring you never miss a beat in the network.

## ✨ Key Features

* **📡 Real-time Sync Tracking (`/sync`):** Fetches pure JSON data via RPC to monitor block height and catching-up status.
* **👑 Validator Health Monitor (`/val`):** Instant insights into your bonded tokens, moniker, and active set status.
* **🌐 Network Peer Overview (`/peers`):** Keep track of your node's connectivity with the network.
* **🚨 Smart Missed-Block Alert (Killer Feature):** * Runs as a background daemon checking `signing-info` every 5 minutes.
    * **Auto-Activation:** Designed with logic to handle the `NotFound` state for inactive/unbonded validators. Once your node enters the Active Set, the alert system automatically kicks in without requiring a bot restart.

## ⚙️ Prerequisites

* **OS:** Ubuntu 22.04 / 24.04 LTS
* **Environment:** Python 3.10+ and `python3-venv`
* **Credentials:** A Telegram Bot Token (from [@BotFather](https://t.me/botfather)) and your Telegram Chat ID.

## 🚀 Installation & Setup

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/ntllinh2511/republic-ai-node-monitor.git](https://github.com/ntllinh2511/republic-ai-node-monitor.git)
    cd republic-ai-node-monitor
    ```

2.  **Create and activate a Virtual Environment:**
    ```bash
    python3 -m venv bot_env
    source bot_env/bin/activate
    pip install pyTelegramBotAPI requests
    ```

3.  **Configure your Bot:**
    Open `republic_bot.py` and fill in your credentials:
    ```python
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    CHAT_ID = "YOUR_CHAT_ID_HERE"
    VALIDATOR_ADDR = "raivaloper1..." # Your validator address
    ```

## 🛠 Running the Bot 24/7

To ensure your monitor stays online even after you close your terminal session, it is recommended to use `tmux`:

1.  **Start a new tmux session:**
    ```bash
    tmux new -s republic_bot
    ```
2.  **Run the bot:**
    ```bash
    source bot_env/bin/activate
    python3 republic_bot.py
    ```
3.  **Detach from session:** Press `Ctrl + B`, then `D`.
4.  **Re-attach anytime:** `tmux attach -t republic_bot`

## 🤝 Contribution

This tool was built with passion for the Republic AI ecosystem by **alexvnn**. Feel free to fork, submit PRs, or report issues!

---
*Developed for the Republic AI Testnet.*
