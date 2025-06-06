
from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SLATE_WEBHOOK_URL = os.getenv('SLATE_WEBHOOK_URL')


@app.route('/submit-reel', methods=['POST'])
def submit_reel():
    caption = request.form.get('caption')
    schedule = request.form.get('schedule')
    telegram_notify = request.form.get('telegramNotify') == 'true'
    slate_notify = request.form.get('slateNotify') == 'true'
    media = request.files.get('media')

    if not caption or not schedule or not media:
        return jsonify({'error': 'Missing fields'}), 400

    filename = secure_filename(media.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    media.save(filepath)

    scheduled_post = {
        'mediaPath': filepath,
        'caption': caption,
        'schedule': schedule
    }

    # Save to JSON file for n8n to pull
    with open('reels-config.json', 'w') as f:
        import json
        json.dump({'reels': [scheduled_post]}, f, indent=2)

    # Notify Telegram
    if telegram_notify and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        message = f'📅 New Reel Scheduled\n📝 Caption: {caption}\n🕒 Scheduled for: {schedule}'
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        )

    # Notify Slate
    if slate_notify and SLATE_WEBHOOK_URL:
        requests.post(SLATE_WEBHOOK_URL, json={
            'event': 'ReelScheduled',
            'data': {
                'caption': caption,
                'schedule': schedule,
                'media': filename
            }
        })

    return jsonify({'message': 'Reel scheduled successfully'}), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)
