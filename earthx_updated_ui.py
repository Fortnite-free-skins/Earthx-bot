
import os
import telebot

# Get bot token from Render environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Start command with EarthX UI
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome to the EarthX ($ERX) Token Presale!\n\n"
        "🌱 Support eco-friendly crypto innovation as an early investor.\n\n"
        "📄 Token Details:\n"
        "• Token Name: EarthX\n"
        "• Symbol: $ERX\n"
        "• Total Supply: 1,000,000,000 ERX\n"
        "• Presale Rate: 1 USDT = 10,000 ERX\n"
        "• Presale Ends: December 31, 2025\n\n"
        "👇 Use the buttons below to participate!"
    )

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('💸 Buy Tokens', '📈 My Balance')
    markup.row('📄 Submit TXID', '🎁 Referral Link')
    markup.row('📊 Presale Status', '❓ Help')

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Menu Options
@bot.message_handler(func=lambda m: m.text == "💸 Buy Tokens")
def buy_tokens(message):
    bot.send_message(message.chat.id,
        "✅ To buy EarthX tokens:\n"
        "Send USDT (TRC20) to:\n"
        "`TRwqhyL6RHMEin5zhkpmo8sB3jPjiGPjcT`\n\n"
        "💰 1 USDT = 10,000 $ERX\n"
        "_After payment, click '📄 Submit TXID'_",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: m.text == "📈 My Balance")
def my_balance(message):
    bot.send_message(message.chat.id,
        "📊 Balance Info:\n"
        "• Invested: 0 USDT\n"
        "• Reserved: 0 $ERX\n"
        "(🛠 Real tracking requires database/API integration.)"
    )

@bot.message_handler(func=lambda m: m.text == "📄 Submit TXID")
def submit_txid(message):
    bot.send_message(message.chat.id,
        "📝 Please enter your transaction ID (TXID) below:"
    )

@bot.message_handler(func=lambda m: m.text == "🎁 Referral Link")
def referral_link(message):
    user_id = message.chat.id
    referral = f"https://t.me/YOUR_BOT_USERNAME?start=ref_{user_id}"
    bot.send_message(message.chat.id,
        f"📢 Share & Earn:\nHere’s your referral link:\n{referral}"
    )

@bot.message_handler(func=lambda m: m.text == "📊 Presale Status")
def presale_status(message):
    bot.send_message(message.chat.id,
        "📊 Presale Progress:\n"
        "Total Raised: 7,500,000 USDT\n"
        "Presale Ends: December 31, 2025\n"
        "Status: 🔥 Ongoing"
    )

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_menu(message):
    bot.send_message(message.chat.id,
        "❓ Help Menu:\n"
        "• 💸 Buy Tokens: How to invest\n"
        "• 📄 Submit TXID: Confirm your payment\n"
        "• 🎁 Referral Link: Invite & earn\n"
        "• 📊 Presale Status: View progress\n"
        "• 📈 My Balance: See your token balance"
    )

# Simple TXID catcher
@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def txid_handler(message):
    if len(message.text.strip()) > 25:
        bot.send_message(message.chat.id, "✅ TXID received. We’ll verify and confirm shortly!")

# Start polling
bot.polling()
