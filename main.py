import json
import time
import schedule
import requests

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import python.datamgmt as dm
import python.inline_handler as ih
import python.io as io

with open("settings.json", "r") as file:
    url = json.load(file)["url"]

def reminder():
    list = dm.get_products()
    for product in list:
        response = requests.get(f"http://{url}/{product['store']}/{product['id']}").text.strip()

        if dm.new_prom(product["id"], response):
            #message = io.fancy_answer(product["id"], response, product["store_name"])
            io.message_to_interessted(product['id'], response, product["store_name"])


#MAIN--------------------------------------------------------------------------

schedule.every().day.at("08:00").do(reminder) # real Timer
#schedule.every(10).seconds.do(reminder) # for test only

while True:
    schedule.run_pending()
    time.sleep(5)
