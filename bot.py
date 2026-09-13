import json
import requests
from config import WEATHER_API_KEY, TOKEN
from models import *
from storage import Storage as st
from telegram.ext import ContextTypes, Application, CommandHandler

DATA_FILE = "data.json"
data = {"notes": [], "expenses": []}

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
        note = Note(text, datetime.now().date()).name
        if not text:
            await update.message.reply_text("Вы не ввели заметку")
            return
        data["notes"].append(note)
        print(data)
        st.save(data)
        await update.message.reply_text("Заметка добавлена")
    except json.JSONDecodeError:
        await update.message.reply_text("Ошибка данных")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def notes_cmd(update, context):
    result = st.load()
    if not result["notes"]:
        await update.message.reply_text("Заметок нет")
        return
    notes = '/n'.join([f"{i}. {note}" for i,note in enumerate(result["notes"], 1)])
    await update.message.reply_text(notes)

async def expenses_cmd(update, context):
    result = st.load()
    if not result["expenses"]:
        await update.message.reply_text("Расходов нет")
        return
    total = sum(result["expenses"].value)
    await update.message.reply_text(f"Итого: {total}")

async def add_expenses_cmd(update, context):
    if not context.args:
        await update.message.reply_text("Вы не ввели сумму расхода")
        return
    try:
        result = Expense(float(context.args[0]), datetime.now()).value
        data["expenses"].append(result)
        st.save(data)
        await update.message.reply_text("Расход добавлен")
    except ValueError:
        await update.message.reply_text("Введите число")


def main():
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start_cmd))
        app.add_handler(CommandHandler("note", note_cmd))
        app.add_handler(CommandHandler("notes", notes_cmd))
        app.add_handler(CommandHandler("add_expenses", add_expenses_cmd))
        app.add_handler(CommandHandler("expenses", expenses_cmd))
        app.run_polling()

if __name__ == "__main__":
    main()









