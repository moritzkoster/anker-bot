import json

with open("people.json", "r") as file:
    people = json.load(file)

for person in people:
    person["answer_mode"] = "text"

with open("people.json", "w") as file:
    json.dump(people, file, indent=4)
