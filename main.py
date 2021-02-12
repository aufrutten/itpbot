"""

(Problems)_
______________ ->
1) Problems with "news" when bot send posts
2) Problems with display comment






(What i'll should do)
______________ ->

1)  Make logging bot, to track errors and bugs
2)  команда по выдаче файла с HTML

"""
print(f'Starting {__file__}')

from configuration import config, keyboards
import logging

logging.basicConfig(**config.config_logger)

from time import sleep
from datetime import datetime
import asyncio

import parserFolder
import controllerDB

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove

logging.info('importing was successful')

bot = Bot(config.TOKEN)
ds = Dispatcher(bot)

db = controllerDB.SQLBase.SQLiter('./DATABASE/members.db')
db_Posts = controllerDB.DataBasePostsSQL.SQLPost('./DATABASE/POSTS_DATA.db')

pars = parserFolder.MainParser()


@ds.message_handler(commands=['author', 'original'])
async def author(message):
    authors = '@FBICIAIIA'
    text = f"Создатель бота - {authors}"

    if message.text == '/author':
        await bot.send_message(message.chat.id, text)
    elif message.text == '/original':
        await bot.send_message(message.chat.id, config.url)


@ds.message_handler(commands=['help'])
async def help_func(message):
    send_mess = """/author - Автор\n/unsubscribe - отписаться\n/start - подписатся\n/original - Ссылка на паблик"""
    logging.info('GETTING HELP')
    await bot.send_message(message.chat.id, send_mess)


@ds.message_handler(commands=['unsubscribe'])
async def unsubscribe(message):
    msg = 'Вы только что отписались...((( 😢\nК сожалению, вы не будете получать свежие посты 📡\n' \
          'а также потеряете навсегда доступ к прошедшим постам 💾'

    id_mem = message.chat.id
    status = False
    logging.warning(f'{id_mem} {message.from_user.username} unsubscribed')
    if db.get_Status(id_mem):
        db.edit_status_subscribe_member(id_mem, status)
        await bot.send_message(id_mem, msg)
    else:
        await bot.send_message(id_mem, "Вы от нас отписаны((( 😭")


@ds.message_handler(commands=['get_stat'])
async def stats(message):
    id_mem = message.chat.id
    result = db.getCountAllMembers()
    mess = f"Статистика: {result} Пользователей"
    logging.critical(f'{id_mem} {message.from_user.username} get stat')
    await bot.send_message(id_mem, mess)


@ds.message_handler(commands=['start'])
async def m_handler(message: types.Message):
    message_m = """
Привет!\n
Это бот группы ВК "На приеме у Шевцова"
Админ не является обладателем контента , а лишь ретранслирует его из оригинального источника!
По всем вопросам обращаться - @FBICIAIIA

/help - Помощь по командам
"""

    message_y = """Подпишитесь пожалуйста на нашу рассылку:)) - Это бесплатно"""

    id_person = message.chat.id
    name = message['from']['username']

    logging.warning('{}, {} was joined'.format(id_person, name))

    if not db.subscriber_exist(id_person):
        logging.error(f'{id_person}, {message.from_user.username}, {message.from_user.first_name}, HE IS THE FIRST')
        db.add_member(name, id_person)

    await bot.send_message(id_person, message_m)
    await message.answer(message_y, reply_markup=keyboards.greet_kb)


@ds.message_handler(content_types='text')
async def subscription(message: types.Message):
    turn_on = "Подписаться! 👋"
    id_mem = message.chat.id

    m_logging = f'id: {id_mem} name: {message.from_user.username} msg: \'{message.text}\''
    logging.warning(m_logging)

    if message.text == turn_on:
        status = True
        db.edit_status_subscribe_member(id_mem, status)
        await message.answer('Поздравляю вы подписались! 😃', reply_markup=ReplyKeyboardRemove(True))
        sleep(1)
        logging.warning(f'HE {message.from_user.username} subscribed, {message.chat.id}')

        if db.cheak_status_connection(id_mem):
            db.switch_status_connection(id_mem)
            posts = db_Posts.read_all_posts()

            for post in posts:
                _, content, comment, date = post

                comment = """{}\nDate: {}""".format(comment, date)
                try:
                    if content != ' ':
                        await bot.send_photo(id_mem, content, comment)
                    else:
                        await bot.send_message(id_mem, comment)
                except:

                    if len(comment) >= 290:
                        comment = comment[:286] + '...'

                    comment = """{}\nDate: {}""".format(comment, date)

                    if content != ' ':
                        await bot.send_photo(id_mem, content, comment)
                    else:
                        await bot.send_message(id_mem, comment)

                await asyncio.sleep(1)

            logging.warning(f'{id_mem}, {message.from_user.username}, {message.from_user.first_name}: было доставлен пак')
    else:
        text = '[{}] id: {} name: {} msg: \'{}\'\n'.format(datetime.today(),
                                                               id_mem,
                                                               message.from_user.username,
                                                               message.text)
        try:
            with open('file_message.txt', 'a') as f:
                f.write(text)
                f.close()
        except:
            with open('file_message.txt', 'w') as f:
                f.write(text)
                f.close()
        await bot.send_message(id_mem, 'Проблемы ебать?!... Пиши сюда сука! - @FBICIAIIA')


async def main_loop(sleep_for):
    logging.info('Before while LOOP')
    await asyncio.sleep(10)
    while True:
        if pars.comparison_index_in_file():
            logging.info('LOOP ------------> True')

            comment = """{0[comment]}\n\nАвтор: {0[owner]}""".format(pars.dictionary)
            photo = pars.dictionary['content']
            index_post = pars.dictionary['index']

            db_Posts.add_post(index_post, photo, comment)

            for id_W in db.getAllMembersStatusTrue():
                logging.warning(f'sending post {id_W}')

                if photo != ' ':
                    await bot.send_photo(id_W, photo, comment)
                elif photo == ' ':
                    await bot.send_message(id_W, comment)

            logging.info('Dispatch completed')
        else:
            logging.info('LOOP ------------> False')

        await asyncio.sleep(sleep_for)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(main_loop(500))
    executor.start_polling(ds, skip_updates=True)


if __name__ == '__main__':
    main()
