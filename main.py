import json
import time
import schedule

import requests

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

url = "127.0.0.1:5000"

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
    return "Willkommen, giiriger Anker Suffer :beer::tada: Du kannst dich mit '/stop' wieder abmelden"

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

    return "Tschüss du Abtrünniger Wassertrinker."

def reminder():
    response = requests.get("http://" + url + "/coop/anker").text
    print(response)

    with open("promotion.json", "r") as file:
        promotions = json.load(file)

    if promotions["anker"] == False and response != "kei Aktion":
        promotions["anker"] == True
        send_message_to_all("Heute ist ein guter Tag: " + response)

    if promotions["anker"] == True and response == "kei Aktion":
        promotions["anker"] == False

    with open("promotion.json", "w") as file:
        promotions = json.dump(promotions, file, indent=4)

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
