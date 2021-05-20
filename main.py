import json
import time
import schedule

import requests

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

with open("settings.json", "r") as file:
    url = json.load(file)["url"]

def start(update, context):
    response = append_id(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)

def stop(update, context):
    response = del_by_id(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


def append_id(id):
    with open("people.json", "r") as file:
        people = json.load(file)

    for person in people:
        if person["id"] == id:
            return "Du hast dich bereits angemeldet. Du kannst dich mit '/stop' wieder abmelden"

    people.append({"id": id})

    with open("people.json", "w") as file:
        json.dump(people, file, indent=4)
    return """🎉🍺 Willkommen, giiriger Anker Suffer 🍺🎉
Sobald Anker Aktion ist im Coop, schickt dir dieser Bot eine Nachricht
Die Nachricht kommt nur am ersten Tag der Aktion.
Du kannst dich mit '/stop' wieder abmelden
Zum waule 🍻"""

def del_by_id(id):
    with open("people.json", "r") as file:
        people = json.load(file)
    for i in range(len(people)):
        person = people[i]
        if id == person["id"]:
            del people[i]
            break
    with open("people.json", "w") as file:
        people = json.dump(people, file, indent=4)

    return "Tschüss du abtrünniger Wassertrinker."

def reminder():
    response = requests.get("http://" + url + "/coop/anker").text
    #response = input("Response: ")

    if new_prom(response):
        send_message_to_all("Heute ist ein guter Tag: " + response)
        #print("Heute ist ein guter Tag: " + response)

def new_prom(response):
    newprom = False

    with open("promotion.json", "r") as file:
        promotions = json.load(file)

    ankerprom = promotions["anker"]["promotion"]
    if not ankerprom and response != "NOPROM":
        ankerprom = True
        newprom = True
    elif ankerprom and response == "NOPROM":
        ankerprom = False

    promotions["anker"]["promotion"] = ankerprom
    with open("promotion.json", "w") as file:
        json.dump(promotions, file, indent=4)
    return newprom

def send_message_to_all(message):
    with open("people.json", "r") as file:
        people = json.load(file)
        for person in people:
            updater.bot.send_message(chat_id=person["id"], text=message)



#MAIN--------------------------------------------------------------------------

with open('token.json', 'r') as token_file:
    token = json.load(token_file)["token"]

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler("stop", stop))

updater.start_polling()

schedule.every().day.at("08:00").do(reminder) # real Timer
#schedule.every(10).seconds.do(reminder) # for test only

while True:
    schedule.run_pending()
    time.sleep(10)
