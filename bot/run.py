

import sys
import json
import random
from bot.secret_sauce.action_models import action_train, action_predict
from bot.secret_sauce.seqtoseq_model import seqtoseq_train, reply_predict


def log(message):
    """log function"""
    if message:
        print(str(message))
        sys.stdout.flush()
    else:
        print("NULL")
        sys.stdout.flush()

def run_bot(sentence):
    """function to run the bot"""
    intent = action_predict(str(sentence))
    #log(intent)
    reply = dsl_protocol(intent, sentence)

    if reply == "none":
        #log(reply)
        reply = reply_predict(str(sentence))
        if reply == "error":
            reply = "I dont know. You better ask a real person"
    return reply

def seqtoseq_train_protocol(sentence):
    """function to train the seqtoseq model"""
    training_data = []
    with open('bot/datasets/chitchat_dataset.json') as data_file:
        data = json.load(data_file)

    for line in data:
    #fetching training data
        training_data.append((line["question"], line["answer"]))
    seqtoseq_train(20000, training_data, tfl=False)
    print(reply_predict(sentence))

def action_train_protocol(sentence):
    """function to train the action prediction model"""
    training_data = []
    with open('bot/datasets/action_dataset.json') as data_file:
        data = json.load(data_file)

    for line in data:
        #fetching training data
        training_data.append(line)

    action_train(20000, training_data) #training the model

    print("intent:" + action_predict(sentence))

def test_run_protocol():
    """function for test running the bot"""
    while True:
        k = input("user: ")
        print("rbot: ", run_bot(k))



def dsl_protocol(intent, sentence):
    """domain specific language for the bot"""
    rep = {}
    rep["text"] = "none"
    key = {'contact':'You can send email to this email id volunteers@rethinkfoundation.in', 'wiki':'http://wiki.rethinkfoundation.in', 'blog':'http://blog.rethinkfoundation.in'
       , 'open':'http://rethinkfoundation.in', 'location':'http://www.bit.ly/gettorethink'}
    if intent != "none":
        rep["text"] = random.choice(["check this out:", "here you go:", "I found this:"]) + key[intent]
    return rep["text"]





