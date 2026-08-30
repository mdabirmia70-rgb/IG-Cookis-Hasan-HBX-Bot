import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # বাটন তৈরি করার অংশ
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
    # reply_markup=markup যোগ করার কারণে কিবোর্ডে বাটনটি শো করবে
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 কাজ শুরু করো")
def start_work(message):
    bot.reply_to(message, "👤 **ইউজারনেম লিস্ট দাও (প্রতি লাইনে একটি):**", parse_mode='Markdown')

bot.infinity_polling()
