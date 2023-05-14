

import telebot
from telebot import types
import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent


bot = telebot.TeleBot('5802220982:AAGs_sTxvByPBwjfWXl87L61Isx-OKiJ0ww')

BASE_URL = "https://avtodnr.ru/?page="

HEADERS = {"User-Agent": UserAgent().random}

words = ["jetta", "джетт", "tiguan", "golf", "тигуан", "гольф" ]


def oops():
    return "Ой, вы походу ошиблись при вводе, попрошу вводить слова 😊\n\nПопробуйте еще раз выбрать нужную кнопку и ввести ключевое слово"


async def main():
    a = ''
    for i in range(1, 15):
        async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL + str(i), headers=HEADERS) as response:
                r = await aiohttp.StreamReader.read(response.content)
                soup = BS(r, "html.parser")
                items = soup.find_all("div", {"class": "col-12 col-md-6 singleBlockCol"})
                for item in items:
                    title = item.find("a", {"class": "post-content"})
                    link = title.get("href")
                    data = item.find("div", {"class": "col-6 text-right"}).text.strip()
                    for s in words:
                        if str(title).lower().find(s.lower()) != -1:
                            a += f"{title.text.strip()[:30]} | {data} | {link}\n\n"
    return a


# loop = asyncio.new_event_loop()
# a = loop.run_until_complete(main())
# print(a)


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Вывести автомобили")
    item2 = types.KeyboardButton("Добавить ключевое слово")
    item3 = types.KeyboardButton("Удалить ключевое слово")
    item4 = types.KeyboardButton("Вывести список ключевых слов")

    markup.add(item1, item2, item3, item4)

    return markup


@bot.message_handler(commands=['site'])
def Site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти в на сайт", url="https://avtodnr.ru/"))
    sti = open('static/1.jpg', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже для перехода", parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=['start'])
def Welcome(message):
    sti = open('static/2.png', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                     "бот, который ""умеет отслеживать автомобили по вашим запросам. "
                     "\nДоступные команды:\n"
                     "/start - запуск бота\n"
                     "/site - сайт с продажей авто\n"
                     .format(message.from_user, bot.get_me()), parse_mode='html',
                     reply_markup=start_menu())


@bot.message_handler(content_types=['text'])
def Menu_Change(message):
    if message.text == 'Вывести автомобили':
        bot.send_message(message.chat.id, "Пару секундочек...")
        loop = asyncio.new_event_loop()

        a = loop.run_until_complete(main())

        if a is not None:
            bot.send_message(message.chat.id, a)

    if message.text == 'Добавить ключевое слово':
        bot.send_message(message.chat.id, add(message))

    if message.text == 'Удалить ключевое слово':
        bot.send_message(message.chat.id, dell(message))

    if message.text == 'Вывести список ключевых слов':
        bot.send_message(message.chat.id, ' , '.join(words))


@bot.message_handler(commands=['add'])
def add(message):
    send = bot.send_message(message.chat.id,
                            "Введите ключевое слово")
    bot.register_next_step_handler(send, register_add)


def register_add(message):
    try:
        last = str(message.text.split()[0])
        bot.send_message(message.chat.id,
                         "Ключевое слово добавлено " + last)
        words.append(str(last))

    except ValueError:
        error(message)
    except AttributeError:
        error(message)
    except KeyError:
        error(message)


@bot.message_handler(commands=['dell'])
def dell(message):
    send = bot.send_message(message.chat.id,
                            "Введите слово из списка")

    bot.register_next_step_handler(send, register_dell)


def register_dell(message):
    try:
        last = str(message.text.split()[0])
        bot.send_message(message.chat.id,
                         "Ключевое слово удалено " + last)
        words.remove(str(last))

    except ValueError:
        error(message)
    except AttributeError:
        error(message)
    except KeyError:
        error(message)


def error(message):
    bot.send_message(message.chat.id, oops())


bot.polling(none_stop=True)
