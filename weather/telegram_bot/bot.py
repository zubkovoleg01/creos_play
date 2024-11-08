import os
import django
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from django.db import close_old_connections
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
django.setup()

from weather.weather_services import get_weather_data

TOKEN = "YOUR_TOKEN"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

builder_menu = ReplyKeyboardBuilder()
builder_menu.row(types.KeyboardButton(text="Узнать погоду"))


class WeatherStates(StatesGroup):
    waiting_for_city = State()


@dp.message(F.text == "/start")
async def start_command(message: types.Message):
    await message.answer(
        f"{message.from_user.first_name}, добро пожаловать! Нажмите кнопку ниже, чтобы узнать погоду.",
        reply_markup=builder_menu.as_markup(resize_keyboard=True)
    )


@dp.message(F.text == "Узнать погоду")
async def ask_city(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_city)
    await message.reply("Введите название города:")


async def async_get_weather_data(city_name, request_type="telegram"):
    result = await sync_to_async(get_weather_data)(city_name, request_type)
    close_old_connections()
    return result


@dp.message(WeatherStates.waiting_for_city)
async def get_weather(message: types.Message, state: FSMContext):
    city_name = message.text.strip()
    if not city_name:
        await message.reply("Пожалуйста, введите название города.")
        return
    try:
        data = await async_get_weather_data(city_name, request_type="telegram")

        if data:
            response = (
                f"Температура: {data['temperature']}°C\n"
                f"Давление: {data['pressure']} мм рт.ст.\n"
                f"Скорость ветра: {data['wind_speed']} м/с"
            )
        else:
            response = "Город введен неверно, попробуйте снова."
            await message.reply(response)
            await message.answer(
                "Нажмите кнопку ниже, чтобы попробовать еще раз.",
                reply_markup=builder_menu.as_markup(resize_keyboard=True)
            )
            await state.clear()
            return

        await message.reply(response)
        await message.answer(
            "Нажмите кнопку ниже, чтобы узнать погоду.",
            reply_markup=builder_menu.as_markup(resize_keyboard=True)
        )

        await state.clear()

    except Exception as e:
        response = f"Произошла ошибка!"
        await message.reply(response)

        await message.answer(
            "Нажмите кнопку ниже, чтобы попробовать еще раз.",
            reply_markup=builder_menu.as_markup(resize_keyboard=True)
        )
        await state.clear()


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
