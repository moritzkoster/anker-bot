import json

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import python.datamgmt as dm

def inline_handler(update, context):
    query = update.callback_query
    query_data = query.data.split(" ")
    user, key = query_data[0:2]
    if len(query_data) > 2:
        values = query_data[2:]

    if key == "interessts":
        interessts(context, query, user)
    if key == "add_interessts":
        add_interessts(context, query, user)
    if key == "rm_interessts":
        rm_interessts(context, query, user)
    if key == "add_product":
        add_product(context, query, user, values)
    if key == "rm_product":
        rm_product(context, query, user, values)

    update.callback_query.message.delete()

def interessts(context, query, user_id):
    keyboard = []
    col = []
    col.append(InlineKeyboardButton("Interessen hinzufügen", callback_data="{} {}".format(query.message.chat_id, "add_interessts")))
    col.append(InlineKeyboardButton("Interessen entfernen", callback_data="{} {}".format(query.message.chat_id, "rm_interessts")))
    keyboard.append(col)
    context.bot.send_message(chat_id=query.message.chat_id, text="Was willst du tun?", reply_markup=InlineKeyboardMarkup(keyboard))

def add_interessts(context, query, user_id):
    user = dm.get_user_by_id(user_id)
    keyboard = generate_keyboard(user, interessted=False)
    context.bot.send_message(chat_id=user_id, text="Was interessiert dich?", reply_markup=InlineKeyboardMarkup(keyboard))

def rm_interessts(context, query, user_id):
    user = dm.get_user_by_id(user_id)
    keyboard = generate_keyboard(user, interessted=True)
    context.bot.send_message(chat_id=user_id, text="Was interessiert dich nicht mehr?", reply_markup=InlineKeyboardMarkup(keyboard))

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
    context.bot.send_message(chat_id=user_id, text=f"Du wirst nun informiert, wenn {name} Aktion ist")
    #else: print(f"Du wirst nun informiert, wenn {product} Aktion ist")

def rm_product(context, query, user_id, values):
    product_id = values[0]
    user = dm.get_user_by_id(user_id)
    user["intr"].remove(product_id)
    dm.write_user(user)

    name = dm.get_product_by_id(product_id)["name"]
    context.bot.send_message(chat_id=user_id, text=f"Du wirst nicht mehr informiert, wenn {name} Aktion ist")
    #else: print(f"Du wirst nicht mehr informiert, wenn {product} Aktion ist")
