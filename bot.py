import os
import io
import time
import pyotp
import openpyxl
import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

# ----------------- Selenium Automation Function -----------------
def run_single_test_login(url, username, password, otp_secret):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ব্যাকগ্রাউন্ডে চালানোর জন্য
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # বট সনাক্তকরণ এড়াতে Standard User-Agent যুক্ত করা হয়েছে
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    cookies_str = ""

    try:
        driver.get(url)
        time.sleep(4)

        # ১. ইউজারনেম ও পাসওয়ার্ড ইনপুট
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        
        # সাবমিট বাটনে ক্লিক
        login_btn = driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_btn.click()
        time.sleep(5)

        # ২. TOTP 2FA ইনপুট (যদি সিক্রেট দেওয়া থাকে)
        if otp_secret:
            totp = pyotp.TOTP(otp_secret)
            token = totp.now()
            
            # OTP ইনপুট বক্স খুঁজে মান বসানো
            otp_box = driver.find_element(By.NAME, "verificationCode")
            otp_box.send_keys(token)
            
            confirm_btn = driver.find_element(By.XPATH, '//button[contains(text(),"Confirm") or @type="button"]')
            confirm_btn.click()
            time.sleep(5)

        # ৩. সেশন কুকিজ সংগ্রহ
        cookies = driver.get_cookies()
        if cookies:
            cookies_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
        
        return cookies_str if cookies_str else None

    except Exception as e:
        print(f"[{username}] Automation error: {e}")
        return None

    finally:
        driver.quit()

# ----------------- Telegram Bot Handlers -----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
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
    bot.register_next_step_handler(msg, get_usernames)

def get_usernames(message):
    chat_id = message.chat.id
    usernames = [u.strip() for u in message.text.strip().split('\n') if u.strip()]
    
    if not usernames:
        bot.send_message(chat_id, "❌ কোনো ইউজারনেম পাওয়া যায়নি!")
        return

    user_data[chat_id] = {'usernames': usernames}
    total = len(usernames)

    msg = bot.send_message(chat_id, f"🔑 **{total}টি আইডির জন্য পাসওয়ার্ড দাও:**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, get_password)

def get_password(message):
    chat_id = message.chat.id
    user_data[chat_id]['password'] = message.text.strip()

    msg = bot.send_message(chat_id, "🔐 **২এফএ সিক্রেট (2FA key) দাও (না থাকলে 'none' লিখুন):**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_all_data)

def process_all_data(message):
    chat_id = message.chat.id
    raw_2fa = message.text.strip()
    
    # ২এফএ সিক্রেট থেকে স্পেস রিমুভ করা
    otp_secret = None if raw_2fa.lower() == 'none' else raw_2fa.replace(" ", "")

    user_data[chat_id]['2fa'] = otp_secret
    usernames = user_data[chat_id]['usernames']
    password = user_data[chat_id]['password']
    total_count = len(usernames)

    # আপনার নির্দিষ্ট লগইন URL দিন (উদাহরণস্বরূপ Instagram)
    target_url = "https://www.instagram.com/accounts/login/"

    bot.send_message(chat_id, f"🤖 **কাজ শুরু হয়েছে... মোট {total_count} টি অ্যাকাউন্ট প্রসেস করা হচ্ছে।**", parse_mode='Markdown')

    cookies_data = ""
    success_users = []
    failed_users = []

    for user in usernames:
        cookie_res = run_single_test_login(target_url, user, password, otp_secret)

        if cookie_res:
            bot.send_message(chat_id, f"✅ `_{user}_`\n*কুকি বের হইছে!* 🔥", parse_mode='Markdown')
            cookies_data += f"{user}:{cookie_res}\n"
            success_users.append(user)
        else:
            bot.send_message(chat_id, f"❌ `_{user}_`\n*লগইন ব্যর্থ হয়েছে!*", parse_mode='Markdown')
            failed_users.append(user)

    # ১. TXT ফাইল জেনারেট
    if cookies_data:
        txt_file = io.BytesIO(cookies_data.encode('utf-8'))
        txt_file.name = "ROKY_COOKIES.txt"
        bot.send_document(chat_id, txt_file)

    # ২. Excel (XLSX) ফাইল জেনারেট
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Account Status"
    ws.append(["Username", "Status"])
    
    for u in success_users:
        ws.append([u, "Success"])
    for u in failed_users:
        ws.append([u, "Failed"])

    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    excel_file.name = "SUCCESS_ACCOUNTS.xlsx"
    bot.send_document(chat_id, excel_file)

    # ফাইনাল সামারি
    report = f"""
📊 **ফাইনাল রিপোর্ট (ROKY - COOKIES)**
━━━━━━━━━━━━━━━━━━━━
♻️ **মোট আইডি:** _{total_count}_ টা
🍪 **কুকি বের হইছে:** _{len(success_users)}_ টা
❌ **লগইন ব্যর্থ:** _{len(failed_users)}_ টা
━━━━━━━━━━━━━━━━━━━━
🔥 **<POWERED BY GEMINI & SOUROV>**
"""
    bot.send_message(chat_id, report, parse_mode='Markdown')
    
    if chat_id in user_data:
        del user_data[chat_id]

if __name__ == "__main__":
    bot.infinity_polling()
