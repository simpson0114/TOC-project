from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_url, send_food_message, add_food_message, send_allfood_message, delete_food_message, is_food

photo = ['https://images.zi.org.tw/ireneslife/2018/08/23222608/1535034368-95cf834c4d3687e1347ed20f3cdb7cab.jpg',
]
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "吃什麼"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "有什麼"

    def is_adding_food(self,event):
        text = event.message.text
        return text.lower() == "加食物"

    def is_deleting_food(self, event):
        text = event.message.text
        return text.lower() == "刪食物"

    def is_showing_foodphoto(self, event):
        text = event.message.text
        return text.lower() == "照片"

    def not_empty(self, event):
        text = event.message.text
        return (text.lower() != "" and not(is_food(text.lower())))

    def is_food_in_list(self, event):
        text = event.message.text
        return is_food(text.lower())

    def on_enter_state1(self, event):
        print("choose one food")
        reply_token = event.reply_token
        send_food_message(reply_token)
        self.go_back()

    def on_exit_choosefood(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        reply_token = event.reply_token
        send_allfood_message(reply_token)
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")
        
    def on_enter_add_food(self, event):
        print("I'm adding food")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入要新增的食物")


    def on_exit_add_food(self, event):
        print("Leaving add_food")
        reply_token = event.reply_token
        add_food_message(event.message.text.lower())
        send_text_message(reply_token, "已新增")

    def on_enter_delete_food(self, event):
        print("I'm deleting food")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入要刪除的食物")

    def on_exit_delete_food(self, event):
        print("Leaving delete_food")
        reply_token = event.reply_token
        delete_food_message(event.message.text.lower())
        send_text_message(reply_token, "已刪除")

    def on_enter_show_foodphoto(self, event):
        print("show food photo")
        reply_token = event.reply_token
        send_image_url(reply_token, photo[0])
        self.go_back()

    def on_enter_show_foodphoto(self):
        print("Leave show_foodphoto")