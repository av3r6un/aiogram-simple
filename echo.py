from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message, ChatMemberUpdated
from config import Config
import asyncio

c = Config('bots/settings.yaml')
settings = c.settings
templates = c.templates

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(m: Message) -> None:
  print(m.text)
  await m.answer(f'Привет, {m.from_user.first_name}!')

@dp.message()
async def echo_handler(m: Message) -> None:
  print(m.text)
  try:
    await m.send_copy(chat_id=m.chat.id)
  except TypeError:
    await m.answer('Nice Try!')

@dp.chat_member()
async def on_join(event: ChatMemberUpdated):
  if event.chat.id == settings.MAIN_CHANNEL:
    changes = {'$username': event.from_user.username, '$name': event.from_user.first_name}
    await event.answer(c.template('hello').replace(**changes), disable_notification=True, disable_web_page_preview=True)

@dp.channel_post()
@dp.edited_channel_post()
async def echo_channel_handler(post: Message):
  print(post.text, post.chat.id)
  try:
    await post.send_copy(chat_id=post.chat.id)
  except TypeError:
    await post.answer('Nice Try!')


async def main() -> None:
  bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
  await dp.start_polling(bot)

if __name__ == '__main__':
  asyncio.run(main())
