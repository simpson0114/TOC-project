import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

from fsm import TocMachine
from utils import send_text_message, add_food_message
from random import choice

load_dotenv()

food = ['鴨肉飯', '乾麵', '港式燒臘', '鍋燒意麵', '炒飯', '拉麵', '餛飩麵']

machine = TocMachine(
    states=["user", "choosefood", "all_food", "add_food", "delete_food", "show_foodphoto"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "choosefood",
            "conditions": "is_going_to_choosefood",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "all_food",
            "conditions": "is_going_to_all_food",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "add_food",
            "conditions": "is_adding_food",
        },
        {
            "trigger": "advance",
            "source": "add_food",
            "dest": "user",
            "conditions": "not_empty",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "delete_food",
            "conditions": "is_deleting_food",
        },
        {
            "trigger": "advance",
            "source": "delete_food",
            "dest": "user",
            "conditions": "is_food_in_list",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "show_foodphoto",
            "conditions": "is_showing_foodphoto",
        },
        {"trigger": "go_back", "source": ["choosefood", "all_food", "show_foodphoto"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

machine.get_graph().draw("fsm.png", prog="dot", format="png")
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        if event.message.text == "吃什麼":
            line_bot_api.reply_message(event.reply_token, TextMessage(text = choice(food)))

        elif event.message.text == "圖片":
            image_url = 'https://images.zi.org.tw/ireneslife/2018/08/23222608/1535034368-95cf834c4d3687e1347ed20f3cdb7cab.jpg'
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
        
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=event.message.text)
            )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "請輸入「吃什麼」決定下一餐\n請輸入「有什麼」看現有食物種類\n請輸入「加食物」新增想要的食物\n請輸入「刪食物」刪除不要的食物\n請輸入「照片」顯示美食照片")
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ['port']
    app.run(host="0.0.0.0", port=port, debug=True)
