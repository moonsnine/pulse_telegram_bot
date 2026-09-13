import json

class Storage:
    @staticmethod
    def save(data):
        with open("data.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load():
        try:
            with open("data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"notes": [], "expenses": []}

    @staticmethod
    def add(item, data):
        if not item:
            return
        data["notes"].append(item)
        Storage.save()

