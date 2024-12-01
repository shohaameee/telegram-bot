import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint

from datetime import datetime  # Buyurtma vaqtini aniqlaydi

from aiogram.utils import keyboard

TOKEN = "7761371808:AAFTvhxxzLdWTD0vtvuysu7aCKANo7OCjVk"
channel_username = "@Zayavkalarim"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
user_orders = {}


email = "olimovabdulaziz464@gmail.com"
password = "GKJCUiYZrACgkj39Fbx9st6OpA2vwaE9snIBpKo7"


@dp.message(Command("start"))
async def startup(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"state": "PHONE_NUMBER"}
    await message.answer(
        "Welcome to our bot! Please do the following steps to continue.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📲 Share Number", request_contact=True)]],
            resize_keyboard=True, one_time_keyboard=True
        ))


async def process_food_menu(message):
    pass


async def process_item_selection(message):
    pass


async def process_show_basket(message):
    pass


async def process_call(message):
    pass


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await startup(message)
        return

    state = user_data[user_id]["state"]

    if state == "PHONE_NUMBER":
        await phone_number(message)
    elif state == "VERIFICATION":
        await check_verification(message)
    elif state == "ADDRESS":
        await address(message)
    elif message.text == "ℹ️ Informations":
        await show_settings(message)
    elif state == "DISCOUNTS":
        await process_main_menu(message)
    elif state == "FOOD_MENU":
        await process_food_menu(message)
    elif state == "ITEM_SELECTION":
        await process_item_selection(message)
    elif state == "BASKET":
        await process_show_basket(message)
    elif state == 'CALL_MENU':
        await process_call(message)
    else:
        await process_main_menu(message)


async def phone_number(message: types.Message):
    user_id = message.from_user.id
    if message.contact is not None:
        phone = message.contact.phone_number
    else:
        phone = message.text

    numbers = '+9874563210'
    tru_num = all(i in numbers for i in phone)

    if tru_num:
        user_data[user_id]['phone'] = phone
        verification_code = randint(1000, 9999)
        user_data[user_id]['verification_code'] = verification_code

        # token = await get_eskiz(email, password)
        # await send_sms(phone, token)                  #BU ikkisini ham oxirida yoqish kere

        user_data[user_id]["state"] = "VERIFICATION"
        await message.answer(f"Enter following verification code: {verification_code}")
    else:
        await message.answer(f"Raqam mavjud emas! Boshqatan urunib ko'ring:")

async def address(message: types.Message):
    user_id = message.from_user.id
    if message.location:
        user_data[user_id][
            "address"] = f"Latitude: {message.location.latitude}, Longitude: {message.location.longitude}"
    else:
        user_data[user_id]["address"] = message.text
    user_data[user_id]["state"] = "MAIN_MENU"
    await show_main_menu(message)

async def check_verification(message: types.Message):
    user_id = message.from_user.id
    if message.text == str(user_data[user_id]['verification_code']):
        user_data[user_id]["state"] = "ADDRESS"
        await message.answer("What's Your Name")
    else:
        await message.reply("Verification code is incorrect!!! Please try again!")

async def show_main_menu(message: types.Message):
    keyboard = [
        [KeyboardButton(text="ℹ️ Information")],
        [KeyboardButton(text="📩 Application")],
    ]

    await message.answer("You got a chance to write a petition or suggestion for Tashkent Metropolitan. Please write your text below:", reply_markup=ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    ))


async def process_main_menu(message: types.Message):
    user_id = message.from_user.id
    if message.text == "ℹ️ Informations":
        await show_settings(message)
        await message.answer('🌞Welcome to our project named "Tashkent metro for everyone"! 🚨Contribute in making Tashkent more accessible for everyone, by writing a petition or your suggestions in here. ⏳We will be receiving and sending your petitions to the responsible people, and will make sure not a single message goes unnoticed✅',
                                reply_markup=ReplyKeyboardMarkup(
                                keyboard=keyboard,
                                resize_keyboard=True,
                                one_time_keyboard=True
                             ))

    elif message.text == "ℹ️ Informations":
        await show_settings(message)
        await message.answer(
            '🌞Welcome to our project named "Tashkent metro for everyone"! 🚨Contribute in making Tashkent more accessible for everyone, by writing a petition or your suggestions in here. ⏳We will be receiving and sending your petitions to the responsible people, and will make sure not a single message goes unnoticed✅',
                reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
                ))



async def show_discounts(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]["state"] = "DISCOUNTS"
    await message.answer("Sizning shahringizda aksiya mavjud emas")



async def show_basket(message: types.Message):
    await bot.send_message(channel_username,
                            f"{phone_number} \n\n Ariza {show_main_menu}")
    await show_main_menu(message)

async def show_orders(message: types.Message):
    user_id = message.from_user.id
    orders = user_orders.get(user_id, [])

    if not orders:
        await message.reply("Sizning buyurtma tarixingiz bo'sh.")
    else:
        order_history = ""
        for order in orders:
            order_history += f"{order['summary']}\n\nTo'lov: {order['total']} so'm\nManzil: {order['address']}\nBuyurtma berilgan vaqti: {order['time']}\n\n"

        await message.reply(f"Sizning buyurtma tarixingiz:\n\n{order_history}")

    user_data[user_id]["state"] = "MAIN_MENU"

async def Information(message: types.Message):
    if message.text == "ℹ️ Information":
        await message.answer(
            '🌞Welcome to our project named "Tashkent metro for everyone"! 🚨Contribute in making Tashkent more accessible for everyone, by writing a petition or your suggestions in here. ⏳We will be receiving and sending your petitions to the responsible people, and will make sure not a single message goes unnoticed✅',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            ))

async def Application(message: types.Message):
    if message.text == "📩 Application":
        await show_settings(message)
        await message.answer(
            'Enter Your Application',
                reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            ))

async def show_settings(message: types.Message):
    user_id = message.from_user.id
    await message.answer("This project was initially based on the ideas of two BMU students Firdavs Anvarov and Ulug'bek Xayitboyev, to make Tashkent metro for everyone.This bot was created with the help of Fayzullaxon Muhiddinov. \n If you have any questions feel free to contact us: \nFirdavs Anvarov: +998 (94) 652-44-20 \nUlug'bek Xayitboyev: +998 (99) 559-63-25")


async def main():
    await dp.start_polling(bot)

print('The bot is running...')

if __name__ == "__main__":
    asyncio.run(main())


