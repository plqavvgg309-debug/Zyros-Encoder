import telebot
import base64
import zlib
import os
from flask import Flask
from threading import Thread

# 1. إعداد السيرفر الوهمي لمنع النوم
app = Flask('')

@app.route('/')
def home():
    return "Zyros System is Live!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعدادات البوت
API_TOKEN = '8638887897:AAFN75MN9waxxJ42CktWeLCSVroH990Bc9c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👑 الملك زايـروس في خدمتك سيدي.\n\nأرسل ملف البايثون الآن ليتم تشفيره بأعلى حماية.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ أرسل ملفات .py فقط سيدي.")
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        source_code = downloaded_file.decode('utf-8')

        # نظام التشفير المتقدم v2
        compressed = zlib.compress(source_code.encode('utf-8'))
        encoded_b64 = base64.b64encode(compressed).decode('utf-8')
        final_hex = encoded_b64.encode('utf-8').hex()
        
        final_code = f"# PROTECTED BY ZYROS v2.0\nimport base64, zlib\nexec(zlib.decompress(base64.b64decode(bytes.fromhex('{final_hex}').decode())).decode())"

        output_name = f"Enc_{message.document.file_name}"
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(final_code)

        with open(output_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ تم التشفير بنجاح.")
        os.remove(output_name)
    except Exception as e:
        bot.reply_to(message, f"⚠️ خطأ: {str(e)}")

# 3. تشغيل السيرفر والبوت معاً
if __name__ == "__main__":
    keep_alive()  # تشغيل السيرفر في الخلفية
    bot.polling(none_stop=True)
