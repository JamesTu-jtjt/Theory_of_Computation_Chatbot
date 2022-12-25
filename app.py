import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "input_goal", "set", "receive", "serve", "spike", "rules"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "input_goal",
            "conditions": "is_going_to_input_goal",
        },
        {
            "trigger": "advance",
            "source": "input_goal",
            "dest": "set",
            "conditions": "is_going_to_set",
        },
        {
            "trigger": "advance",
            "source": "input_goal",
            "dest": "receive",
            "conditions": "is_going_to_receive",
        },
        {
            "trigger": "advance",
            "source": "input_goal",
            "dest": "serve",
            "conditions": "is_going_to_serve",
        },
        {
            "trigger": "advance",
            "source": "input_goal",
            "dest": "spike",
            "conditions": "is_going_to_spike",
        },
        {
            "trigger": "advance",
            "source": ["set", "receive", "serve", "spike", "input_goal"],
            "dest": "rules",
            "conditions": "is_going_to_rules",
        },
        {
            "trigger": "advance",
            "source": ["set", "receive", "serve", "spike", "rules"],
            "dest": "input_goal",
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
            #send_text_message(event.reply_token, "Not Entering any State")
            if machine.state == 'user':
                send_text_message(event.reply_token, 'Welcome to this simple Volleyball Drill Generator for beginners~\n We can recommend different drills for you to improve your volleyball skills and help you review the rules of volleyball. \n Please input "start" to begin.')
            elif machine.state == 'input_goal':
                send_text_message(event.reply_token, 'What would you like to practice today? Please enter "serve", "receive", "set", or "spike" to get drills and "rules" to review the rules of volleyball.')
            elif machine.state == 'serve' or machine.state == 'receive' or machine.state == 'set' or machine.state == 'spike' or machine.state == 'rules':
                send_text_message(event.reply_token, 'Please enter "start" to begin next drill or "rules" to review the rules of volleyball.')
            
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
