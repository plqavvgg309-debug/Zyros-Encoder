import telebot
import base64
import zlib
import os

# توكن البوت الخاص بك
API_TOKEN = '8638887897:AAFmPQZVSbt0ZhUNYHg6N_eEtrFcUAMowLU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👑 أهلاً بك سيدي اللورد زايـروس\n\nتم تحديث نظام التشفير للجيل الثاني (متوافق مع جميع الإصدارات).\nأرسل ملف الـ .py الآن.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ سيدي، يرجى إرسال ملفات بايثون فقط.")
        return

    try:
        # 1. تحميل الملف
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        source_code = downloaded_file.decode('utf-8')

        # 2. عملية التشفير (الضغط ثم الـ Base64 ثم الـ Hex)
        # تم إلغاء Marshal لحل مشكلة الـ Opcode
        compressed = zlib.compress(source_code.encode('utf-8'))
        encoded_b64 = base64.b64encode(compressed).decode('utf-8')
        final_hex = encoded_b64.encode('utf-8').hex()
        
        # 3. بناء هيكل التشغيل المحمي (متوافق 100%)
        final_code = f"""# PROTECTED BY ZYROS v2.0
# AUTHORIZED USE ONLY
import base64, zlib
exec(zlib.decompress(base64.b64decode(bytes.fromhex('{final_hex}').decode())).decode())"""

        output_name = f"Enc_{message.document.file_name}"
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(final_code)

        with open(output_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ تم التشفير بنجاح سيدي.\nهذه النسخة تعمل على Pydroid وكل الإصدارات.")
        
        os.remove(output_name)

    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ: {str(e)}")

bot.polling()
