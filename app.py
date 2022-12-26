import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_image_message

load_dotenv()
fsm_link = 'https://c4c1-2001-b400-e28d-dfdb-d498-8ae8-d501-8755.jp.ngrok.io/show-fsm'

machine = TocMachine(
    states=["user", "main_menu", "drills", "positions", "rules", "help", "set", "receive", "serve", "spike", "block"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "main_menu",
            "conditions": "is_going_to_main_menu",
        },
        {
            "trigger": "advance",
            "source": ["main_menu", "drills", "positions", "rules", "help"],
            "dest": "main_menu",
            "conditions": "is_going_to_main_menu",
        },
        {
            "trigger": "advance",
            "source": "main_menu",
            "dest": "drills",
            "conditions": "is_going_to_drills",
        },
        {
            "trigger": "advance",
            "source": "main_menu",
            "dest": "positions",
            "conditions": "is_going_to_positions",
        },
        {
            "trigger": "advance",
            "source": "main_menu",
            "dest": "rules",
            "conditions": "is_going_to_rules",
        },
        {
            "trigger": "advance",
            "source": "drills",
            "dest": "set",
            "conditions": "is_going_to_set",
        },
        {
            "trigger": "advance",
            "source": "drills",
            "dest": "receive",
            "conditions": "is_going_to_receive",
        },
        {
            "trigger": "advance",
            "source": "drills",
            "dest": "serve",
            "conditions": "is_going_to_serve",
        },
        {
            "trigger": "advance",
            "source": "drills",
            "dest": "spike",
            "conditions": "is_going_to_spike",
        },
        {
            "trigger": "advance",
            "source":  "drills",
            "dest": "block",
            "conditions": "is_going_to_block",
        },
        {
            "trigger": "advance",
            "source": ["set", "receive", "serve", "spike", "block"],
            "dest": "drills",
        },
        {
            "trigger": "advance",
            "source":  ["drills", "positions", "rules", "main_menu"],
            "dest": "help",
            "conditions": "is_going_to_help",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


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
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, fsm_link)
            #send_text_message(event.reply_token, "Not Entering any State")
            if machine.state == 'user':
                send_text_message(event.reply_token, 'Welcome to this simple Volleyball Drill Generator for beginners~\n We can recommend different drills for you to improve your volleyball skills and help you review the rules of volleyball. \n Please input "menu" to begin.')
            elif machine.state == 'main_menu':
                send_text_message(event.reply_token, 'Please enter "menu" or select a service.')
            elif machine.state == 'drills':
                send_text_message(event.reply_token, 'What would you like to practice today? You can also enter "menu" to return to menu.')
            else:
                send_text_message(event.reply_token, 'Please enter "menu" to return to menu or "help" to contact creator. Thank you!')
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.svg", prog="dot", format="svg")
    return send_file("fsm.svg", mimetype="image/svg")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
