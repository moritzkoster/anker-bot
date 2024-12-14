import json
import re

def append_id(id):
    id = str(id)
    with open("data/people.json", "r") as file:
        people = json.load(file)

    for person in people:
        if person["id"] == id:
            return "Du hast dich bereits angemeldet. Du kannst dich mit '/stop' wieder abmelden"

    people.append({"id": id, "intr": ["anker"]})

    with open("data/people.json", "w") as file:
        json.dump(people, file, indent=4)
    return get_text("welcome")

def del_by_id(user_id):
    with open("data/people.json", "r") as file:
        people = json.load(file)
    for i in range(len(people)):
        person = people[i]
        if str(user_id) == person["id"]:
            del people[i]
            break
    with open("data/people.json", "w") as file:
        people = json.dump(people, file, indent=4)

    return "Tschüss du abtrünniger Wassertrinker."

def new_prom(product, response):

    with open("data/promotion.json", "r") as file:
        promotions = json.load(file)

    if product in promotions:
        lastprom = promotions[product]["promotion"]
    else:
        lastprom = "NOPROM"
        promotions[product] = {}

    promotions[product]["promotion"] = response

    with open("data/promotion.json", "w") as file:
        json.dump(promotions, file, indent=4)

    if response != "NOPROM" and response != lastprom:
        if product != "anker":
            return True
        
        # ONLY 45% or more prom for Anker Beer
        for field in ["([0-9]{2})%", "([0-9]{2})% ab [2-9]"]:
            if int(re.match(field, response)[1]) >= 45: # convert this shit to integers 
                return True
        if re.match("2 für 1", response):
            return True

    return False



# UTILITIES --------------------------------------------------------------------

def get_promotions():
    with open("data/promotion.json", "r") as file:
        return file.read()

def get_people():
    with open("data/people.json", "r") as file:
        return json.load(file)

def get_text(key):
    with open("data/text.json", "r") as file:
        return json.load(file)[key]

def get_user_by_id(user_id):
    for person in get_people():
        if str(user_id) == person["id"]:
            return person

def get_products():
    with open("data/products.json", "r") as file:
        return json.load(file)

def get_product_by_id(id):
    for product in get_products():
        if id == product["id"]:
            return product


def write_user(user):
    with open("data/people.json", "r") as file:
        people = json.load(file)

    for i in range(len(people)):
        person = people[i]
        if user["id"] == person["id"]:
            people[i] = user

    with open("data/people.json", "w") as file:
        json.dump(people, file, indent=4)
