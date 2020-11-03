#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram import Bot, Dispatcher, executor, types
import utils
from os import environ


bot = Bot(token=environ["1371051662:AAG3J8XLw0HqHyKGmccOoIZAhWjetABrYpo"])  # Pass token as environment variable
dp = Dispatcher(bot)


# /start command with possible deeplink
# See https://core.telegram.org/bots#deep-linking
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    words = message.text.split()
    if len(words) > 1 and words[1] == "help_decipher":
        await bot.send_message(message.chat.id, "Use /decode <pasted text> command to decipher that message.")
    else:
        await bot.send_message(message.chat.id, "Use /encode {text} command to convert string to emoji and /decode "
                                                "{text} for a reverse opeartion")


@dp.message_handler(commands=["encode"])
async def cmd_encode(message: types.Message):
    tokens = message.text.split()
    if len(tokens) < 2:
        await message.reply("Please provide text to encode")
        return
    text_to_encode = " ".join(tokens[1:])

    if message.chat.type == "private":
        await bot.send_message(message.chat.id, utils.encode(text_to_encode))
    else:
        await message.reply(utils.encode(text_to_encode))


@dp.message_handler(commands=["decode"])
async def cmd_encode(message: types.Message):
    tokens = message.text.split()
    if len(tokens) < 2:
        await message.reply("Please provide text to decode")
        return
    text_to_decode = " ".join(tokens[1:])

    decoded_text_or_error = None
    try:
        decoded_text_or_error = utils.decode(text_to_decode)
    except Exception:
        decoded_text_or_error = "Could not decode this text. You can only decode emoji"

    if message.chat.type == "private":
        await bot.send_message(message.chat.id, decoded_text_or_error)
    else:
        await message.reply(decoded_text_or_error)


@dp.inline_handler()
async def inline_mode(query: types.InlineQuery):
    if not query.query:
        return
    keyboard = types.InlineKeyboardMarkup()
    # don't forget to replace "base100bot" in the next line with your bot's username!
    btn_decipher = types.InlineKeyboardButton(text="Decode this text (copy it before)",
                                              url="https://t.me/base100bot?start=help_decipher")
    keyboard.add(btn_decipher)
    ciphertext = utils.encode(query.query)
    answer = types.InlineQueryResultArticle(
        id="1",
        title=query.query,
        description=ciphertext,
        input_message_content=types.InputTextMessageContent(message_text=ciphertext),
        reply_markup=keyboard
    )
    await bot.answer_inline_query(query.id, [answer], cache_time=3600)


if __name__ == "__main__":
    executor.start_polling(dp)
