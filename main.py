import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()


events = {}


@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "Привет! Я бот-календарь. Вот доступные команды:\n"
        "/add_event <дата> <событие> - добавить событие\n"
        "/show_events - показать все события\n"
        "/delete_event <дата> <событие> - удалить событие\n"
        "/events_on_date <дата> - показать события на конкретную дату"
    )


@dp.message(Command("add_event"))
async def add_event(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Используй: /add_event <дата> <событие>")
        return
    date, event = args[1], args[2]
    events.setdefault(date, []).append(event)
    await message.answer(f"Событие '{event}' добавлено на {date}.")


@dp.message(Command("show_events"))
async def show_events(message: Message):
    if not events:
        await message.answer("Событий пока нет.")
        return
    response = "Все события:\n" + "\n".join([f"{date}: {', '.join(evs)}" for date, evs in events.items()])
    await message.answer(response)


@dp.message(Command("delete_event"))
async def delete_event(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Используй: /delete_event <дата> <событие>")
        return
    date, event = args[1], args[2]
    if date not in events or event not in events[date]:
        await message.answer(f"Событие '{event}' на {date} не найдено.")
        return
    events[date].remove(event)
    if not events[date]:  # Удаляем дату, если событий больше нет
        del events[date]
    await message.answer(f"Событие '{event}' удалено с {date}.")


@dp.message(Command("events_on_date"))
async def events_on_date(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Используй: /events_on_date <дата>")
        return
    date = args[1]
    if date not in events:
        await message.answer(f"На {date} событий нет.")
        return
    response = f"События на {date}:\n" + "\n".join(events[date])
    await message.answer(response)


@dp.message()
async def echo(message: Message):
    await message.answer(
        "Используй команды:\n"
        "/add_event <дата> <событие>\n"
        "/show_events\n"
        "/delete_event <дата> <событие>\n"
        "/events_on_date <дата>"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
