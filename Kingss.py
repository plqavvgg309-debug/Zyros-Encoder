import telebot
import base64
import zlib
import marshal
import os

# توكن البوت الخاص بك سيدي
API_TOKEN = '8638887897:AAFmPQZVSbt0ZhUNYHg6N_eEtrFcUAMowLU'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👑 أهلاً بك سيدي اللورد زايـروس\n\nقم بإرسال ملف البايثون (.py) الآن وسأقوم بتشفيره لك فوراً بـ 5 طبقات حماية.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ سيدي، يرجى إرسال ملفات بايثون فقط.")
        return

    try:
        # تحميل الملف من التليجرام
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        source_code = downloaded_file.decode('utf-8')

        # --- عملية التشفير الطبقي (بروتوكول زايـروس) ---
        # 1. تحويل إلى Bytecode (Marshal)
        compiled_code = compile(source_code, '<zyros>', 'exec')
        marshaled = marshal.dumps(compiled_code)
        
        # 2. الضغط (Zlib)
        compressed = zlib.compress(marshaled)
        
        # 3. التشفير النصي (Base64)
        encoded = base64.b64encode(compressed).decode('utf-8')
        
        # 4. بناء هيكل التشغيل المحمي
        final_code = f"""# PROTECTED BY ZYROS ENCRYPTION SYSTEM
# AUTHORIZED USE ONLY
import base64, marshal, zlib
exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"""

        # حفظ الملف المشفر
        output_name = f"Enc_{message.document.file_name}"
        with open(output_file_name := output_name, "w", encoding="utf-8") as f:
            f.write(final_code)

        # إرسال الملف المشفر للسيد
        with open(output_file_name, "rb") as f:
            bot.send_document(message.chat.id, f, caption="✅ تم التشفير بنجاح سيدي.\nالملف الآن محمي ولا يمكن سرقته.")
        
        # تنظيف الملفات المؤقتة
        os.remove(output_file_name)

    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء التشفير: {str(e)}")

print("Bot is running...")
bot.polling()
