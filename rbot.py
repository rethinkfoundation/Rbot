import os
import sys
import json
import requests
from flask import Flask, request,render_template, redirect
from bot.run import run_bot
from templates.forms import InputForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '22334455'
@app.route('/', methods=['GET'])
def verify():
    """verify"""
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "go to http://127.0.0.1:5000/test", 200

@app.route('/test',methods=['GET', 'POST'])
def test():
    """test UI"""
    form = InputForm()
    if form.validate_on_submit():
        reply = run_bot(form.input_data.data)
        input_text = form.input_data.data
        form.input_data.data = ""
        return render_template('index.html', reply = reply, form = form, input_text = input_text)
    return render_template('index.html', form = form)

def log(message):
    """function for logging"""
    if message:
       print(str(message))
       sys.stdout.flush()
    else:
       print("NULL")
       sys.stdout.flush()

if __name__ == '__main__':
    #app.debug = True
    app.run()
