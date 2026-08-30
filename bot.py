import telebot

# আপনার টেলিগ্রাম বট টোকেনটি এখানে বসান
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.Telebot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
❤️ ⚡ 「 𝚁𝙾𝙺𝚈 𝚄𝙻𝚃𝚁𝙰 𝚂𝙿𝙴𝙴𝙳 」 ⚡
━━━━━━━━━━━━━━━━━━━━
👋 **আরে MD. SOUROV HASAN কোপারু যে! সোনা, আমি জানতাম তুমি আসবে কোপ দিতে😁!**
🤖 **Powered by: Gemini AI & Sourov**
━━━━━━━━━━━━━━━━━━━━
🚀 **Engine:** _v31.0_ | 🛰️ **Status:** _Full গরম_ 🔥
━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "কাজ শুরু করো")
def start_work(message):
    bot.reply_to(message, "👤 **ইউজারনেম লিস্ট দাও (প্রতি লাইনে একটি):**", parse_mode='Markdown')

bot.infinity_polling()
