import json
import time
import schedule
import requests

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import python.datamgmt as dm
import python.inline_handler as ih

with open("settings.json", "r") as file:
    url = json.load(file)["url"]

def start(update, context):
    response = dm.append_id(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)

def stop(update, context):
    response = dm.del_by_id(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)

def settings(update, context):
    keyboard = []
    row = []
    row.append(InlineKeyboardButton("Interessen ändern", callback_data="{} {}".format(update.message.chat_id, "interessts")))
    keyboard.append(row)
    context.bot.send_message(chat_id=update.message.chat_id, text="Salletti Spaghetti. Was willst du tun?", reply_markup=InlineKeyboardMarkup(keyboard))

    update.message.delete()

def reminder():
    list = dm.get_products()
    for product in list:
        response = requests.get(f"http://{url}/{product['store']}/{product['id']}").text
        #response = input("Response: ")

        if response != "NOPROM":
            send_message_to(product['id'], response)
            #print("Heute ist ein guter Tag: " + response)

def send_message_to_all(message): #NOT USED
    with open("people.json", "r") as file:
        people = json.load(file)
        for person in people:
            updater.bot.send_message(chat_id=person["id"], text=message)


def send_message_to(product_id, message):
    with open("people.json", "r") as file:
        people = json.load(file)
        for person in people:
            if product_id in person["intr"]:
                updater.bot.send_message(chat_id=person["id"], text=message)

#MAIN--------------------------------------------------------------------------

with open('token.json', 'r') as token_file:
    token = json.load(token_file)["token"]

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CallbackQueryHandler(ih.inline_handler))

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler("stop", stop))
dispatcher.add_handler(CommandHandler("settings", settings))

updater.start_polling()

schedule.every().monday.at("08:00").do(reminder) # real Timer
#schedule.every(10).seconds.do(reminder) # for test only

while True:
    schedule.run_pending()
    time.sleep(5)
