from transitions.extensions import GraphMachine

from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_input_goal(self, event):
        text = event.message.text
        return text.lower() == "start"

    def on_enter_input_goal(self, event):
        title = 'What would you like to practice?'
        text = 'Please enter "serve", "receive", "set", "spike", or "rules".'
        btn = [
            MessageTemplateAction(
                label = 'serve',
                text ='serve'
            ),
            MessageTemplateAction(
                label = 'receive',
                text = 'receive'
            ),
            MessageTemplateAction(
                label = 'set',
                text ='set'
            ),
            MessageTemplateAction(
                label = 'spike',
                text ='spike'
            ),
            MessageTemplateAction(
                label = 'rules',
                text ='rules'
            ),
        ]
        url = 'https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dm9sbGV5YmFsbHxlbnwwfHwwfHw%3D&w=1000&q=80'
        send_button_message(event.reply_token, title, text, btn, url)
    
    def is_going_to_serve(self, event):
        text = event.message.text
        return text.lower() == "serve"
    
    def is_going_to_receive(self, event):
        text = event.message.text
        return text.lower() == "receive"
    
    def is_going_to_spike(self, event):
        text = event.message.text
        return text.lower() == "spike"
    
    def is_going_to_set(self, event):
        text = event.message.text
        return text.lower() == "set"
    
    def is_going_to_rules(self, event):
        text = event.message.text
        return text.lower() == "rules"
    
    def on_enter_serve(self, event):
        text_mes = 'Good choice!!\n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=9Xd-nuj54As'
        send_text_message(event.reply_token, text_mes)

    def on_enter_recieve(self, event):
        text_mes = 'Good choice!!\n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=v77BEawqIWE'
        send_text_message(event.reply_token, text_mes)
    
    def on_enter_set(self, event):
        text_mes = 'Good choice!!\n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=-aDqyumtad0'
        send_text_message(event.reply_token, text_mes)
    
    def on_enter_spike(self, event):
        text_mes = 'Good choice!!\n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=VrMI1dpV8c0'
        send_text_message(event.reply_token, text_mes)
    
    def on_enter_rules(self, event):
        text_mes = 'Forgot the rules? You can review the rules here: \n https://www.theartofcoachingvolleyball.com/basic-volleyball-rules-and-terminology/'
        send_text_message(event.reply_token, text_mes)

    def on_exit_state1(self):
        print("Leaving state1")


    def on_exit_state2(self):
        print("Leaving state2")
