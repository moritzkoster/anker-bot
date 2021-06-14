import json

with open("people.json", "r") as file:
    people = json.load(file)

for person in people:
    if "intr" not in person:
        person["intr"] = ["anker"]

with open("people.json", "w") as file:
    json.dump(people, file, indent=4)
