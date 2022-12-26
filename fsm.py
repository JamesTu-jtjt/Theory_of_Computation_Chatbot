from transitions.extensions import GraphMachine
from utils import send_text_message, send_image_carousel, send_button_message, send_image_message, send_carousel_message
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_main_menu(self, event):
        text = event.message.text
        return text.lower() == "menu"
    
    def on_enter_main_menu(self, event):
        title = 'What would you like to do?'
        text = 'Select any option.'
        btn = [
            MessageTemplateAction(
                label = 'drills',
                text ='drills'
            ),
            MessageTemplateAction(
                label = 'positions',
                text = 'positions'
            ),
            MessageTemplateAction(
                label = 'rules',
                text = 'rules'
            ),
            MessageTemplateAction(
                label = 'help',
                text ='help'
            ),
        ]
        url = 'https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dm9sbGV5YmFsbHxlbnwwfHwwfHw%3D&w=1000&q=80'
        send_button_message(event.reply_token, title, text, btn, url)
        self.go_back()

    def is_going_to_drills(self, event):
        text = event.message.text
        return text.lower() == "drills"

    def on_enter_drills(self, event):
        serve = 'https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024c3c35952665dc91bc80_Dimensions-Sports-Volleyball-Volleyball-Serve-Underhand-Icon.svg'
        set_ball = 'https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024e237b140a08969279dd_Dimensions-Sports-Volleyball-Volleyball-Set-Icon.svg'
        receive_ball = 'https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024d423f1376603ea4346e_Dimensions-Sports-Volleyball-Volleyball-Dig-Icon.svg'
        spike = 'https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024dd43f1376025fa43567_Dimensions-Sports-Volleyball-Volleyball-Spike-Attack-Men.svg'
        block = 'https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024c8cffdd737c80e4e0a7_Dimensions-Sports-Volleyball-Volleyball-Block-Icon.svg'
        urls = [serve, receive_ball, set_ball, spike, block]
        labels = ['Serve', 'Receive', 'Set', 'Spike', 'Block']
        texts = ['Serve', 'Receive', 'Set', 'Spike', 'Block']
        send_image_carousel(event.reply_token, urls, labels, texts)
    
    def is_going_to_positions(self, event):
        text = event.message.text
        return text.lower() == "positions"
    
    def on_enter_positions(self, event):
        overall = ['https://volleyballvault.com/wp-content/uploads/2022/04/VOLLEYBALLpositions.jpg?ezimgfmt=rs:352x201/rscb1/ngcb1/notWebP', 'http://www.volleyballadvisors.com/6-positions-of-volleyball.html', 'court layout']
        setter = ['https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024e237b140a08969279dd_Dimensions-Sports-Volleyball-Volleyball-Set-Icon.svg', 'https://www.improveyourvolley.com/volleyball-setter.html', 'setter']
        middle_blocker = ['https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024c8cffdd737c80e4e0a7_Dimensions-Sports-Volleyball-Volleyball-Block-Icon.svg', 'https://www.improveyourvolley.com/volleyball-blocker.html', 'blocker']
        hitter = ['https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024dbaee042279bb8ef7a4_Dimensions-Sports-Volleyball-Volleyball-Spike-Attack-Icon.svg', 'https://www.improveyourvolley.com/volleyball-outside-hitter.html', 'hitter']
        libero = ['https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/60024cd71ba6f767f05749a7_Dimensions-Sports-Volleyball-Volleyball-Dive-Icon.svg', 'https://www.improveyourvolley.com/volleyball-libero.html', 'libero']
        position_list = [overall, setter, middle_blocker, hitter, libero]
        col = []
        for i in position_list:
            c = ImageCarouselColumn(
                image_url = i[0],
                action = URITemplateAction(
                    label = i[2],
                    uri = i[1]
                )
            )
            col.append(c)
        send_carousel_message(event.reply_token, col)
        
    def is_going_to_rules(self, event):
        text = event.message.text
        return text.lower() == "rules"
    
    def on_enter_rules(self, event):
        text_mes = 'Forgot the rules? You can review the rules here: \n https://www.theartofcoachingvolleyball.com/basic-volleyball-rules-and-terminology/'
        send_text_message(event.reply_token, text_mes)
        self.go_back()
    
    def is_going_to_help(self, event):
        text = event.message.text
        return text.lower() == "help"
    
    def on_enter_help(self, event):
        text_mes = 'Dear valued user, \n    '
        text_mes += 'We apologize for any inconvenience that you may have experienced with our chatbot. '
        text_mes += 'We strive to provide the best possible service and are deeply sorry that our chatbot was not able to fulfill your needs. '
        text_mes += 'We take all feedback seriously and will work to improve the performance of our chatbot in the future. '
        text_mes += 'Thank you for bringing this to our attention. '
        text_mes += 'If you would like to provide further feedback or have any further questions, please do not hesitate to contact us at jamestu6301@gmail.com. '
        text_mes += 'We hope to have the opportunity to serve you better in the future.\n\nSincerely,\nJames'
        send_text_message(event.reply_token, text_mes)
    
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
    
    def is_going_to_block(self, event):
        text = event.message.text
        return text.lower() == "block"
    
    def on_enter_serve(self, event):
        float_serve = 'https://www.youtube.com/watch?v=keoujsEGQ8M'
        jump_serve = 'https://www.youtube.com/watch?v=aLdrBI0wlqY'
        underoverhand_serve = 'https://www.youtube.com/watch?v=SnG7XJDunzs'
        topspin_serve = 'https://www.youtube.com/watch?v=EDmck_G9Cn4'
        
        text_mes = 'Good choice!! Serving is one of the first steps in volleyball. \n Here are some simple drills for you~ \n'
        text_mes = text_mes + "For beginners: underhand and overhand serve: " + underoverhand_serve + '\n'
        text_mes = text_mes + "For intermediate players: topspin serve: " + topspin_serve + '\n'
        text_mes = text_mes + "For intermediate players: float serve: " + float_serve + '\n'
        text_mes = text_mes + "For advanced players: jump serve:" + jump_serve + '\n'
        text_mes = text_mes + "Good luck training and let me know when you are done!"
        send_text_message(event.reply_token, text_mes)
        self.go_back()

    def on_enter_receive(self, event):
        text_mes = 'Good choice!! Receiving is the core of defense in volleyball\n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=v77BEawqIWE'
        text_mes = text_mes + "\nGood luck training and let me know when you are done!"
        send_text_message(event.reply_token, text_mes)
        self.go_back()
    
    def on_enter_set(self, event):
        text_mes = 'Good choice!! Setting looks easy, but it is actually more technically challenging than you think. \n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=-aDqyumtad0'
        text_mes = text_mes + "\nGood luck training and let me know when you are done!"
        send_text_message(event.reply_token, text_mes)
        self.go_back()
    
    def on_enter_spike(self, event):
        text_mes = 'Good choice!! Spiking is the star of highlights in a volleyball game. \n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=VrMI1dpV8c0'
        text_mes = text_mes + "\nGood luck training and let me know when you are done!"
        send_text_message(event.reply_token, text_mes)
        self.go_back()
        
    def on_enter_block(self, event):
        text_mes = 'Good choice!! Blocking is the key to good defense for your team against spikes. \n Here is a simple drill for you~ \n https://www.youtube.com/watch?v=30IxcOsUXGM'
        text_mes = text_mes + "\nGood luck training and let me know when you are done!"
        send_text_message(event.reply_token, text_mes)
        self.go_back()
