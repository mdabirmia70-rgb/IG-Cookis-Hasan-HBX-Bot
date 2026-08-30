import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_start = types.KeyboardButton("🚀 কাজ শুরু করো")
    markup.add(btn_start)

    welcome_text = """
❤️ ⚡ 「 𝚁𝙾𝙺𝚈 𝚄𝙻𝚃𝚁𝙰 𝚂𝙿𝙴𝙴𝙳 」 ⚡
━━━━━━━━━━━━━━━━━━━━
👋 **আরে MD. SOUROV HASAN কোপারু যে! সোনা, আমি জানতাম তুমি আসবে কোপ দিতে😁!**
🤖 **Powered by: Gemini AI & Sourov**
━━━━━━━━━━━━━━━━━━━━
🚀 **Engine:** _v31.0_ | 🛰️ **Status:** _Full গরম_ 🔥
━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 কাজ শুরু করো")
def start_work(message):
    bot.reply_to(message, "👤 **ইউজারনেম লিস্ট দাও (প্রতি লাইনে একটি):**", parse_mode='Markdown')

# ইউজারনেম লিস্ট রিসিভ এবং প্রসেস করার নতুন হ্যান্ডলার
@bot.message_handler(func=lambda message: message.text != "🚀 কাজ শুরু করো" and not message.text.startswith('/'))
def process_usernames(message):
    # ইউজারনেমগুলোকে লাইন অনুযায়ী আলাদা করা
    usernames = message.text.strip().split('\n')
    total = len(usernames)

    bot.reply_to(message, f"⏳ **মোট {total} টি ইউজারনেম পাওয়া গেছে! প্রসেসিং শুরু হচ্ছে...**", parse_mode='Markdown')

    # এখানে আপনার মূল কাজের লজিক (যেমন: কুকিজ চেক বা অন্য কিছু) যুক্ত করতে পারেন
    for username in usernames:
        user = username.strip()
        if user:
            # উদাহরণস্বরূপ একটি রেসপন্স (আপনার প্রয়োজন অনুযায়ী পরিবর্তন করবেন)
            print(f"Processing: {user}")

    bot.send_message(message.chat.id, f"✅ **সবগুলো ({total} টি) ইউজারনেমের কাজ শেষ হয়েছে!**", parse_mode='Markdown')

bot.infinity_polling()



