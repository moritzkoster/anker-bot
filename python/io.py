import json
import random

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import python.datamgmt as dm
import python.inline_handler as ih


with open("settings.json", "r") as file:
    dict = json.load(file)
    DEBUG = dict["DEBUG"]
    fancy_ans = dict["fancy_answer"]

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

def fancy_answer(name, prom, store):
    if fancy_ans == "server": # the old server delivers fancy answers by himself, no need to adapt them.
        return prom
    with open("data/" + name + ".json", "r") as file:
        texts = json.load(file)
    text = random.choice(texts)
    return text.format(DISC=prom, STORE=store)

# def send_message_to_all(message): #NOT USED
#     with open("people.json", "r") as file:
#         people = json.load(file)
#         for person in people:
#             updater.bot.send_message(chat_id=person["id"], text=message)


def message_to_interessted(product_id, message):
    with open("people.json", "r") as file:
        people = json.load(file)
        for person in people:
            if product_id in person["intr"]:
                send(person["id"], message)
                #updater.bot.send_message(chat_id=person["id"], text=message)

def send(chat_id, text, reply_markup=False):
    if DEBUG:
        print(f"TO: {chat_id}, MSG: {text}, KEYBOARD: {reply_markup}")
    elif reply_markup:
        updater.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    else:
        updater.bot.send_message(chat_id=chat_id, text=text)

def send_dict(dict):
    send(dict["chat_id"], dict["text"], reply_markup=dict["markup"])

def inline_handler(update, context):
    query = update.callback_query
    query_data = query.data.split(" ")
    user, key = query_data[0:2]
    if len(query_data) > 2:
        values = query_data[2:]

    if key == "interessts":
        response = ih.interessts(context, query, user)
        send_dict(response)
    if key == "add_interessts":
        response = ih.add_interessts(context, query, user)
        send_dict(response)
    if key == "rm_interessts":
        response = ih.rm_interessts(context, query, user)
        send_dict(response)
    if key == "add_product":
        response = ih.add_product(context, query, user, values)
        send_dict(response)
    if key == "rm_product":
        response = ih.rm_product(context, query, user, values)
        send_dict(response)

    update.callback_query.message.delete()


with open('token.json', 'r') as token_file:
    token = json.load(token_file)["token"]

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CallbackQueryHandler(inline_handler))

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler("stop", stop))
dispatcher.add_handler(CommandHandler("settings", settings))

updater.start_polling()
