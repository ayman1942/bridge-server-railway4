from flask import Flask, request
import telegram
import os
import json

BOT_TOKEN = '7446987073:AAHUuVl_LJj33LQPr9Npm9RPQE9tW8HAev0'
bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)

UPLOAD_FOLDER = 'screenshots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '✅ Bridge Server is Running on Render (Debug Mode)'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)

        print("\n📩 [WEBHOOK] Received Telegram Update:")
        print(json.dumps(data, indent=2))

        update = telegram.Update.de_json(data, bot)

        if update.message and update.message.photo:
            photo_file = update.message.photo[-1].get_file()
            file_path = os.path.join(UPLOAD_FOLDER, f'{update.message.message_id}.jpg')
            photo_file.download(file_path)
            print(f'📥 تم حفظ الصورة: {file_path}')
        else:
            print("⚠️ التحديث توصلنا به، لكن ما فيهش صورة...")

    except Exception as e:
        print(f"❌ وقعات شي غلطة: {str(e)}")

    return 'OK'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

