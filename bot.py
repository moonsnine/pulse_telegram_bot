import json
import requests
from config import WEATHER_API_KEY, TOKEN

from telegram.ext import ContextTypes, Application, CommandHandler

DATA_FILE = "data.json"
data = {"notes": [], "expenses": []}


def save_data():
    with open("data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"notes": [], "expenses": []}

async def start_cmd(update, context):
    await update.message.reply_text(
        "Привет! Я бот-помощник.\n\n"
        "Команды:\n"
        "/note <текст> - добавить заметку\n"
        "/notes - показать заметки\n"
        "/weather <город> - погода\n"
        "/rate <из> <в> - курс валют\n"
        "/add_expenses - добавить расход\n"
        "/expenses - показать расходы"
    )

async def note_cmd(update, context):
    try:
        text = ' '.join(context.args)
        if not text:
            await update.message.reply_text("Вы не ввели заметку")
            return
        data["notes"].append(text)
        save_data()
        await update.message.reply_text("Заметка добавлена")
    except json.JSONDecodeError:
        await update.message.reply_text("Ошибка данных")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def notes_cmd(update, context):
    result = load_data()
    if not result["notes"]:
        await update.message.reply_text("Заметок нет")
        return
    notes = '/n'.join([f"{i}. {note}" for i, note in enumerate(result["notes"], 1)])
    await update.message.reply_text(notes)

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout = 5)
        if response.status_code == 200:
            result = response.json()
            return result["main"]["temp"]
    except requests.exceptions.ConnectionError:
        print("Нет покдлючения!")
    except requests.exceptions.Timeout:
        print("Вышло время ожидания")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка {e}")

def get_rate(base, target):
    url = f"https://open.er-api.com/v6/latest/{base.upper()}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result = response.json()
            target = target.upper()
            if target in result["rates"]:
                return result["rates"][target]
            else:
                print("Такой валюты нет")
        else:
            print(f"Ошибка: {response.status_code}")
    except Exception as e:
        print(f"Ошибка: {e}")


async def weather_cmd(update, context):
    if not context.args:
        await update.message.reply_text("Вы не ввели город")
        return
    city = ' '.join(context.args)
    result = get_weather(city)
    await update.message.reply_text(f"Температура: {result}")

async def rate_cmd(update, context):
    if len(context.args) != 2:
        await update.message.reply_text("Введены не 2 валюты")
        return
    base = context.args[0]
    target = context.args[1]
    result = get_rate(base, target)
    await update.message.reply_text(f"1 {base} = {result} {target}")

async def expenses_cmd(update, context):
    result = load_data()
    if not result["expenses"]:
        await update.message.reply_text("Расходов нет")
        return
    total = sum(result["expenses"])
    await update.message.reply_text(f"Итого: {total}")

async def add_expenses_cmd(update, context):
    if not context.args:
        await update.message.reply_text("Вы не ввели сумму расхода")
        return
    try:
        result = float(context.args[0])
        data["expenses"].append(result)
        save_data()
        await update.message.reply_text("Расход добавлен")
    except ValueError:
        await update.message.reply_text("Введите число")


def main():
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start_cmd))
        app.add_handler(CommandHandler("note", note_cmd))
        app.add_handler(CommandHandler("notes", notes_cmd))
        app.add_handler(CommandHandler("weather", weather_cmd))
        app.add_handler(CommandHandler("rate", rate_cmd))
        app.add_handler(CommandHandler("add_expenses", add_expenses_cmd))
        app.add_handler(CommandHandler("expenses", expenses_cmd))
        app.run_polling()

if __name__ == "__main__":
    main()









