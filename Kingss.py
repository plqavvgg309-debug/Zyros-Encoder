import telebot
import base64
import zlib
import os

# توكن البوت الخاص بك سيدي
API_TOKEN = '8638887897:AAFmPQZVSbt0ZhUNYHg6N_eEtrFcUAMowLU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👑 أهلاً بك سيدي اللورد زايـروس\n\nتم تحديث النظام ليعمل على جميع الإصدارات.\nأرسل ملف الـ .py الآن لتشفيره.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ سيدي، يرجى إرسال ملفات بايثون فقط.")
        return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        source_code = downloaded_file.decode('utf-8')

        # تشفير آمن ومتوافق (بدون Marshal)
        compressed = zlib.compress(source_code.encode('utf-8'))
        encoded_b64 = base64.b64encode(compressed).decode('utf-8')
        final_hex = encoded_b64.encode('utf-8').hex()
        
        final_code = f"""# PROTECTED BY ZYROS v2.0\nimport base64, zlib\nexec(zlib.decompress(base64.b64decode(bytes.fromhex('{final_hex}').decode())).decode())"""

        output_name = f"Enc_{message.document.file_name}"
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(final_code)

        with open(output_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ تم التشفير بنجاح سيدي.\nهذه النسخة تعمل على Pydroid وكل الإصدارات.")
        os.remove(output_name)
    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ: {str(e)}")

bot.polling(none_stop=True)
