import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from random import choice

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
food = ['鴨肉飯', '乾麵', '港式燒臘', '鍋燒意麵', '炒飯', '拉麵', '餛飩麵']


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def send_image_url(reply_token, image_url):
	line_bot_api = LineBotApi(channel_access_token)
	message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
	line_bot_api.reply_message(reply_token, message)
	
def send_food_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=choice(food)))
    return "OK"

def send_allfood_message(reply_token):
    text = ""
    line_bot_api = LineBotApi(channel_access_token)
    for x in range(len(food)): 
        text += food[x] 
    line_bot_api.reply_message(reply_token, TextSendMessage(text=", ".join(food)))
    return "OK"

def add_food_message(recieved_message):
    food.append(recieved_message)

def delete_food_message(recieved_message):
	food.remove(recieved_message)

def is_food(recieved_message):
	return recieved_message in food
'''
def send_button_message(id, text, buttons):
    pass
'''