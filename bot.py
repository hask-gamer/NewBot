import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from btn import *

BOT_TOKEN = "6359732207:AAHGmVYWjrEgW2C7F-pzjiTBbYqK-4AsjKM"

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


async def command_menu(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Ishga tushirish'),
        ]
    )


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer("Salom")


@dp.callback_query_handler(text="like")
async def get_like_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data["like"] + 1

    await state.update_data(like=count)
    btn = await get_text_inline_btn(like=count, dislike=data['dislike'])
    await call.message.edit_reply_markup(reply_markup=btn)
    await call.answer("Javobingiz uchun rahmat", show_alert=True)


@dp.callback_query_handler(text="dislike")
async def get_dislike_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data['dislike'] + 1

    await state.update_data(dislike=count)
    btn = await get_text_inline_btn(like=data['like'], dislike=count)
    await call.message.edit_reply_markup(reply_markup=btn)
    await call.answer("Javobingiz uchun rahmat", show_alert=True)


@dp.message_handler(content_types=["text"])
async def get_text_handler(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(like=0, dislike=0)
    btn = await get_text_inline_btn()
    await message.answer(text, reply_markup=btn)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=command_menu)
