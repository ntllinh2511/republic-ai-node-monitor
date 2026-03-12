import telebot
import subprocess
import json
import time
import threading

# ==========================================
# 1. USER CONFIGURATION (EDIT THESE)
# ==========================================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
VALIDATOR_ADDR = "YOUR_VALIDATOR_ADDRESS_HERE" 

# Node Configuration
NODE_URL = "tcp://localhost:43657"
RPC_URL = "http://localhost:43657" 

bot = telebot.TeleBot(BOT_TOKEN)
last_missed_blocks = 0

# ==========================================
# 2. MAIN BOT COMMANDS
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "🤖 **Republic AI Node Monitor** 🤖\n"
        "*(Community Tool by @alexvnn)*\n\n"
        "🛠 **Available Commands:**\n"
        "👉 `/sync` - Check node sync status\n"
        "👉 `/val` - Check validator status\n"
        "👉 `/peers` - Check network peers\n\n"
        "*(Proactive Missed Block Alert is running in the background 24/7)*"
    )
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['sync'])
def check_sync(message):
    try:
        output = subprocess.check_output(f"curl -s {RPC_URL}/status", shell=True).decode('utf-8')
        data = json.loads(output)
        sync_info = data['result']['sync_info']
        height = sync_info['latest_block_height']
        catching_up = sync_info['catching_up']
        status = "🟢 100% Synced" if not catching_up else "🟡 Catching up..."
        bot.send_message(message.chat.id, f"📡 **SYNC STATUS**\n🧱 Current Block: `{height}`\n🔄 Status: {status}", parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **Sync Error:** Cannot connect to Node.", parse_mode='Markdown')

@bot.message_handler(commands=['val'])
def check_validator(message):
    try:
        cmd = f"republicd query staking validator {VALIDATOR_ADDR} --node {NODE_URL} -o json"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8')
        data = json.loads(output)
        val_info = data.get('validator', data) if 'validator' in data else data
        moniker = val_info.get('description', {}).get('moniker', 'Unknown')
        tokens = float(val_info.get('tokens', 0)) / 10**18
        status = val_info.get('status', 'UNKNOWN')
        icon = "🟢" if status == "BOND_STATUS_BONDED" else "🟡"
        res = (
            f"👑 **VALIDATOR PROFILE** 👑\n"
            f"📛 Moniker: `{moniker}`\n"
            f"💰 Bonded: `{tokens:.2f} ARAI`\n"
            f"📈 Status: {icon} `{status}`"
        )
        bot.send_message(message.chat.id, res, parse_mode='Markdown')
    except Exception:
        bot.send_message(message.chat.id, f"❌ **Validator Error:** Check your address config.")

@bot.message_handler(commands=['peers'])
def check_peers(message):
    try:
        output = subprocess.check_output(f"curl -s {RPC_URL}/net_info", shell=True).decode('utf-8')
        data = json.loads(output)
        n_peers = data['result']['n_peers']
        bot.send_message(message.chat.id, f"🌐 **NETWORK**\n🤝 Connected to: `{n_peers}` peers.", parse_mode='Markdown')
    except Exception:
        bot.send_message(message.chat.id, "❌ **Peers Error.**", parse_mode='Markdown')

def alert_missed_blocks():
    global last_missed_blocks
    while True:
        try:
            addr_out = subprocess.check_output("republicd comet show-address --home ~/.republicd", shell=True, stderr=subprocess.DEVNULL).decode('utf-8').strip()
            sign_cmd = f"republicd q slashing signing-info {addr_out} --node {NODE_URL} -o json"
            sign_out = subprocess.check_output(sign_cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8')
            sign_data = json.loads(sign_out)
            current_missed = int(sign_data.get('missed_blocks_counter', 0))
            if current_missed > last_missed_blocks:
                msg = f"🚨 **RED ALERT** 🚨\nYour node is missing blocks!\n📉 Missed blocks count: `{current_missed}`"
                bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
                last_missed_blocks = current_missed
        except Exception:
            pass
        time.sleep(300)

threading.Thread(target=alert_missed_blocks, daemon=True).start()

if __name__ == "__main__":
    bot.infinity_polling()
