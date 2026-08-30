import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ইউজারের ডাটা অস্থায়ীভাবে জমা রাখার জন্য ডিকশনারি
user_data = {}

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
    msg = bot.reply_to(message, "👤 **ইউজারনেম লিস্ট দাও (প্রতি লাইনে একটি):**", parse_mode='Markdown')
    # পরবর্তী মেসেজটি get_usernames ফাংশনে পাঠাবে
    bot.register_next_step_handler(msg, get_usernames)

def get_usernames(message):
    chat_id = message.chat.id
    usernames = [u.strip() for u in message.text.strip().split('\n') if u.strip()]
    
    if not usernames:
        bot.send_message(chat_id, "❌ কোনো ইউজারনেম পাওয়া যায়নি! আবার চেষ্টা করুন।")
        return

    # ইউজারনেম সেভ করা
    user_data[chat_id] = {'usernames': usernames}
    total = len(usernames)

    msg = bot.send_message(chat_id, f"🔑 **{total}টি আইডির জন্য পাসওয়ার্ড দাও:**", parse_mode='Markdown')
    # পরবর্তী মেসেজটি get_password ফাংশনে পাঠাবে
    bot.register_next_step_handler(msg, get_password)

def get_password(message):
    chat_id = message.chat.id
    user_data[chat_id]['password'] = message.text.strip()

    msg = bot.send_message(chat_id, "🔐 **২এফএ সিক্রেট (2FA key) দাও:**", parse_mode='Markdown')
    # পরবর্তী মেসেজটি process_all_data ফাংশনে পাঠাবে
    bot.register_next_step_handler(msg, process_all_data)

def process_all_data(message):
    chat_id = message.chat.id
    user_data[chat_id]['2fa'] = message.text.strip()

    usernames = user_data[chat_id]['usernames']
    password = user_data[chat_id]['password']
    two_fa_keys = user_data[chat_id]['2fa']
    total_count = len(usernames)

    # কাজ শুরুর মেসেজ
    bot.send_message(chat_id, f"🤖 **কাজ শুরু হয়েছে... মোট {total_count} টি অ্যাকাউন্ট প্রসেস করা হচ্ছে।**", parse_mode='Markdown')

    # এখানে আপনার লগইন বা কুকিজ বের করার অটোমেশন লজিক কাজ করবে
    # উদাহরণস্বরূপ একটি মেসেজ লুক দেওয়া হচ্ছে:
    for user in usernames:
        bot.send_message(chat_id, f"✅ `_{user}_`\n*কুকি বের হইছে!* 🔥", parse_mode='Markdown')

    # ফাইনাল রিপোর্ট
    report = f"""
📊 **ফাইনাল রিপোর্ট (ROKY - COOKIES)**
━━━━━━━━━━━━━━━━━━━━
♻️ **মোট আইডি:** _{total_count}_ টা
🍪 **কুকি বের হইছে:** _{total_count}_ টা
❌ **লগইন ব্যর্থ:** _0_ টা
━━━━━━━━━━━━━━━━━━━━
🔥 **<POWERED BY GEMINI & SOUROV>**
"""
    bot.send_message(chat_id, report, parse_mode='Markdown')
    
    # মেমোরি ক্লিয়ার
    del user_data[chat_id]

bot.infinity_polling()
