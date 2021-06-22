import json

def append_id(id):
    id = str(id)
    with open("people.json", "r") as file:
        people = json.load(file)

    for person in people:
        if person["id"] == id:
            return "Du hast dich bereits angemeldet. Du kannst dich mit '/stop' wieder abmelden"

    people.append({"id": id, "intr": ["anker"]})

    with open("people.json", "w") as file:
        json.dump(people, file, indent=4)
    return """🎉🍺 Willkommen, giiriger Anker Suffer 🍺🎉
Sobald Anker Aktion ist im Coop, schickt dir dieser Bot eine Nachricht
Die Nachricht kommt nur am ersten Tag der Aktion.
Du kannst dich mit '/stop' wieder abmelden
Zum waule 🍻"""

def del_by_id(user_id):
    with open("people.json", "r") as file:
        people = json.load(file)
    for i in range(len(people)):
        person = people[i]
        if str(user_id) == person["id"]:
            del people[i]
            break
    with open("people.json", "w") as file:
        people = json.dump(people, file, indent=4)

    return "Tschüss du abtrünniger Wassertrinker."

def new_prom(product, response):

    with open("promotion.json", "r") as file:
        promotions = json.load(file)

    lastprom = promotions[product]["promotion"]
    promotions[product]["promotion"] = response

    with open("promotion.json", "w") as file:
        json.dump(promotions, file, indent=4)

    if response != "NOPROM" and response != lastprom:
        return True
    return False



# UTILITIES --------------------------------------------------------------------

def get_people():
    with open("people.json", "r") as file:
        return json.load(file)


def get_user_by_id(user_id):
    for person in get_people():
        if str(user_id) == person["id"]:
            return person

def get_products():
    with open("products.json", "r") as file:
        return json.load(file)

def get_product_by_id(id):
    for product in get_products():
        if id == product["id"]:
            return product


def write_user(user):
    with open("people.json", "r") as file:
        people = json.load(file)

    for i in range(len(people)):
        person = people[i]
        if user["id"] == person["id"]:
            people[i] = user

    with open("people.json", "w") as file:
        json.dump(people, file, indent=4)
