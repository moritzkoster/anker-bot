import json

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import python.datamgmt as dm

def interessts(context, query, user_id):
    keyboard = []
    col = []
    col.append(InlineKeyboardButton("Interessen hinzufügen", callback_data="{} {}".format(query.message.chat_id, "add_interessts")))
    col.append(InlineKeyboardButton("Interessen entfernen", callback_data="{} {}".format(query.message.chat_id, "rm_interessts")))
    keyboard.append(col)
    return {"chat_id": user_id, "text": "Was willst du tun?", "markup": InlineKeyboardMarkup(keyboard)}

def add_interessts(context, query, user_id):
    user = dm.get_user_by_id(user_id)
    keyboard = generate_keyboard(user, interessted=False)
    return {"chat_id": user_id, "text": "Was interessiert dich?", "markup": InlineKeyboardMarkup(keyboard)}


def rm_interessts(context, query, user_id):
    user = dm.get_user_by_id(user_id)
    keyboard = generate_keyboard(user, interessted=True)
    return {"chat_id": user_id, "text": "Was interessiert dich nicht mehr?", "markup": InlineKeyboardMarkup(keyboard)}

def generate_keyboard(user, interessted=False):
    list = get_list(user, interessted)
    keyboard, row = [], []
    action = "add_product"
    if interessted:
        action = "rm_product"

    left = True
    for product in list:
        if left:
            row = [InlineKeyboardButton(product["name"], callback_data=f"{user['id']} {action} {product['id']}")]
            left = False
        else:
            row.append(InlineKeyboardButton(product["name"], callback_data=f"{user['id']} {action} {product['id']}"))
            keyboard.append(row.copy())
            left = True
    if not left: keyboard.append(row.copy())
    return keyboard

def get_list(user, interessted):
    with open("products.json", "r") as file:
        list = json.load(file)
    intr = []
    for element in list:
        if interessted and element["id"] in user["intr"]:
            intr.append(element)
        if not interessted and element["id"] not in user["intr"]:
            intr.append(element)
    return intr


def add_product(context, query, user_id, values):
    product_id = values[0]
    user = dm.get_user_by_id(user_id)
    user["intr"].append(product_id)
    dm.write_user(user)
    name = dm.get_product_by_id(product_id)["name"]
    return {"chat_id": user_id, "text": f"Du wirst nun informiert, wenn {name} Aktion ist", "markup": False}


def rm_product(context, query, user_id, values):
    product_id = values[0]
    user = dm.get_user_by_id(user_id)
    user["intr"].remove(product_id)
    dm.write_user(user)
    name = dm.get_product_by_id(product_id)["name"]
    return {"chat_id": user_id, "text": f"Du wirst nicht informiert, wenn {name} Aktion ist", "markup": False}

def change_answer_mode(context, query, user_id):
    keyboard = []
    col = []
    col.append(InlineKeyboardButton("Text", callback_data=f"{query.message.chat_id} answer_mode text"))
    col.append(InlineKeyboardButton("Memes", callback_data=f"{query.message.chat_id} answer_mode meme"))
    keyboard.append(col)
    return {"chat_id": user_id, "text": "Wie willst benachrichtig werden?", "markup": InlineKeyboardMarkup(keyboard)}

def answer_mode(context, query, user_id, values):
    mode = values[0]
    user = dm.get_user_by_id(user_id)
    user["answer_mode"] = mode
    dm.write_user(user)
    return {"chat_id": user_id, "text": f"Du wirst nun per {mode} informiert wenn irgendwas Aktion ist", "markup": False}
