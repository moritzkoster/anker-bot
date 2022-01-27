import json
import random

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import python.datamgmt as dm
import python.inline_handler as ih


with open("settings.json", "r") as file:
    dict = json.load(file)
    DEBUG = dict["DEBUG"]
    TERMINAL_ANSWER = dict["terminal_answer"]
    TEST_TOKEN = dict["test_token"]
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
    row.append(InlineKeyboardButton("Antwortart ändern", callback_data=f"{update.message.chat_id} change_answer_mode"))
    keyboard.append(row)
    context.bot.send_message(chat_id=update.message.chat_id, text="Salletti Spaghetti. Was willst du tun?", reply_markup=InlineKeyboardMarkup(keyboard))

    update.message.delete()

def info(update, context):
    text = dm.get_text("info")
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

def test_function(update, context):
    meme = fancy_meme("anker", "TEST", "TEST")
    context.bot.send_photo(chat_id=update.message.chat_id, photo=meme)

def fancy_answer(name, prom, store):
    if fancy_ans == "server": # the old server delivers fancy answers by himself, no need to adapt them.
        return prom
    try:
        with open("data/" + name + ".json", "r") as file:
            texts = json.load(file)
        text = random.choice(texts)
        return text.format(DISC=prom, STORE=store)
    except:
        product_name = dm.get_product_by_id(name)["name"]
        return f'{product_name} isch {prom} im {store}'

def fancy_meme(product_id, prom, store):
    try:
        with open("data/meme.json", "r") as file:
            available_memes = json.load(file)
        filename = random.choice(available_memes[product_id])
        return open(f"data/meme/{filename}", "rb")
    except:
        return False

# def send_message_to_all(message): #NOT USED
#     with open("people.json", "r") as file:
#         people = json.load(file)
#         for person in people:
#             updater.bot.send_message(chat_id=person["id"], text=message)


def message_to_interessted(product_id, response, store_name):
    meme = fancy_meme(product_id, response, store_name)
    text = fancy_answer(product_id, response, store_name)

    with open("people.json", "r") as file:
        people = json.load(file)
        for person in people:
            if product_id in person["intr"]:
                if person["answer_mode"] == "meme" and meme:
                    updater.bot.send_photo(chat_id=person["id"], photo=meme)
                # if person["answer_mode"] == "text":
                send(person["id"], text)

                #updater.bot.send_message(chat_id=person["id"], text=message)

def send(chat_id, text, reply_markup=False):
    if TERMINAL_ANSWER:
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
    if key == "change_answer_mode":
        response = ih.change_answer_mode(context, query, user)
        send_dict(response)
    if key == "answer_mode":
        response = ih.answer_mode(context, query, user, values)
        send_dict(response)

    update.callback_query.message.delete()


with open('token.json', 'r') as token_file:
    if TEST_TOKEN: token = json.load(token_file)["test-token"]
    else: token = json.load(token_file)["token"]

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CallbackQueryHandler(inline_handler))

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler("stop", stop))
dispatcher.add_handler(CommandHandler("settings", settings))
dispatcher.add_handler(CommandHandler("info", info))

if DEBUG: dispatcher.add_handler(CommandHandler("test", test_function))

updater.start_polling()
