from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import smart_solver

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=['GET'])
def health_check():
    return "Math Solver Bot is running! 🧮"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    
    if "=" in user_text:
        result = smart_solver.parse_and_solve(user_text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    else:
        help_text = "🧮 วิธีใช้งาน Math Solver Bot\n\nส่งโจทย์ในรูปแบบ: ตัวเลข=ผลลัพธ์\n\nตัวอย่าง:\n• 24056=901\n• 1245=54"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=help_text)
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)