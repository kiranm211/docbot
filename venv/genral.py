from flask import Flask, render_template, request,Blueprint
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


genral = Blueprint("genral", __name__,static_folder="static",template_folder="templates/disease")
english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")

@genral.route("/")
def home():
    return render_template("index1.html")


@genral.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))