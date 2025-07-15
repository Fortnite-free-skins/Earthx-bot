import os
import telebot
import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WALLET_ADDRESS = 'TRwqhyL6RHMEin5zhkpmo8sB3jPjiGPjcT'
TOKEN_NAME = 'EarthX'
TOKEN_SYMBOL = 'ERX'
RATE = 10000
SOFT_CAP = 10000000
HARD_CAP = 50000000
PRESALE_END = datetime.datetime(2025, 12, 31)
RAISED = 7500000

bot = telebot.TeleBot(BOT_TOKEN)
users = {}

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("💸 Buy Tokens", callback_data="buy"),
        InlineKeyboardButton("📄 Submit TXID", callback_data="txid"),
        InlineKeyboardButton("📈 My Balance", callback_data="balance"),
        InlineKeyboardButton("🎁 Get Referral Link", callback_data="referral"),
        InlineKeyboardButton("📊 Presale Status", callback_data="status"),
        InlineKeyboardButton("❓ Help", callback_data="help")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    ref = message.text.split(" ")[-1] if len(message.text.split(" ")) > 1 else None
    if user_id not in users:
        users[user_id] = {"balance": 0, "ref": ref}
    bot.send_message(message.chat.id, f"👋 Welcome to the {TOKEN_NAME} ($${TOKEN_SYMBOL}) Presale!\n\n📥 Buy early and be part of the green revolution.\n\nUse the menu below to participate:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id

    if call.data == "buy":
        bot.send_message(call.message.chat.id, f"To buy {TOKEN_NAME}, send USDT (TRC20) to:\n\n💳 `{WALLET_ADDRESS}`\n\nMinimum: 10 USDT\nMaximum: 1000 USDT\n\nAfter sending, click 'Submit TXID'.", parse_mode='Markdown')

    elif call.data == "txid":
        msg = bot.send_message(call.message.chat.id, "📝 Please enter your transaction ID (TXID):")
        bot.register_next_step_handler(msg, handle_txid)

    elif call.data == "balance":
        balance = users.get(user_id, {}).get("balance", 0)
        bot.send_message(call.message.chat.id, f"💰 You’ve purchased: {balance} {TOKEN_SYMBOL} tokens.")

    elif call.data == "referral":
        bot.send_message(call.message.chat.id, f"🎁 Share this link to earn bonus tokens:\n\nhttps://t.me/EarthXPresaleBot?start={user_id}")

    elif call.data == "status":
        days_left = (PRESALE_END - datetime.datetime.now()).days
        progress = int((RAISED / HARD_CAP) * 10)
        bar = '█' * progress + '░' * (10 - progress)
        bot.send_message(call.message.chat.id, f"📊 Presale Status:\n\n• Total Raised: {RAISED:,} USDT\n• Soft Cap: {SOFT_CAP:,} USDT\n• Hard Cap: {HARD_CAP:,} USDT\n• Progress: {bar} {int((RAISED/HARD_CAP)*100)}%\n• Time Left: {days_left} days")

    elif call.data == "help":
        bot.send_message(call.message.chat.id, "Need help? Just send your questions here and we’ll assist you.")

def handle_txid(message):
    user_id = message.from_user.id
    txid = message.text
    users[user_id]["balance"] += RATE
    bot.send_message(message.chat.id, f"✅ TXID received! {RATE} {TOKEN_SYMBOL} added to your account.")

# Keep-alive server
app = Flask('')

@app.route('/')
def home():
    return "EarthX Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
bot.infinity_polling()
