import emoji
import telebot
import time
import requests
import locale
from datetime import datetime
from bs4 import BeautifulSoup

bot = telebot.TeleBot('')

BYN_CURRENCY = 'https://select.by/kurs/'
full_page = requests.get(BYN_CURRENCY)
soup = BeautifulSoup(full_page.content, 'html.parser')
convert = soup.findAll('span', {'itemprop': 'price'})
convert_1 = soup.findAll('td', {})

CURRENCY_RATE = {
    'доллар сша': [convert[0].text, convert[1].text, convert_1[4].text, 'USD', emoji.emojize(":United_States:")],
    'евро': [convert[2].text, convert[3].text, convert_1[9].text, 'EUR', emoji.emojize(":European_Union:")],
    'российский рубль': [convert[4].text, convert[5].text, convert_1[14].text, 'RUB', emoji.emojize(":Russia:")],
    'злотый': [convert[6].text, convert[7].text, convert_1[19].text, 'PLN', emoji.emojize(":Poland:")],
    'гривна': [convert[8].text, convert[9].text, convert_1[24].text, 'UAH', emoji.emojize(":Ukraine:")]}


@bot.message_handler(commands=['start'])
def greetings(message):
    keyboardI = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboardI.add(key_yes)
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')  # кнопка «Нет»
    keyboardI.add(key_no)

    hour = time.localtime()  # Greetings
    if hour.tm_hour <= 12:
        phrase = emoji.emojize(
            'Доброе утро! Желаете узнать точный курс валюты на сегодня? :smiling_face_with_smiling_eyes:')
    elif hour.tm_hour > 12 and hour.tm_hour <= 17:
        phrase = emoji.emojize(
            'Добрый день! Желаете узнать точный курс валюты на сегодня? :smiling_face_with_smiling_eyes:')
    else:
        phrase = emoji.emojize(
            'Добрый вечер! Желаете узнать точный курс валюты на сегодня? :smiling_face_with_smiling_eyes:')
    bot.send_message(message.chat.id, phrase, reply_markup=keyboardI)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker_1(call):
    keyboardR = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if call.data == "yes":
        buttons = ['Доллар США', 'Евро', 'Российский рубль', 'Злотый', 'Гривна']
        keyboardR.add(*buttons)
        bot.send_message(call.message.chat.id, 'Чудесно :) Курс какой валюты Вас интересует? ', reply_markup=keyboardR)
    elif call.data == "no":
        buttons = ['Конечно', 'Пожалуй, нет!']
        keyboardR.add(*buttons)
        bot.send_message(call.message.chat.id, 'Понял:) В таком случае могу предолжить Вам прочесть последние новости!',
                         reply_markup=keyboardR)


@bot.message_handler(content_types=['text'])
def default_test(message):
    if message.text == 'Конечно':
        url_button = telebot.types.InlineKeyboardButton(text="Перейти к новостям",
                                                        url="https://newssearch.yandex.by/news/rubric/business",
                                                        callback_data='view')
        keyboard = telebot.types.InlineKeyboardMarkup().add(url_button)
        bot.send_message(message.chat.id, emoji.emojize(
            "Нажми на кнопку, чтобы узнать о последних новостях в экономике прямо сейчас :face_with_monocle:"),
                         reply_markup=keyboard)
        bot.send_message(message.chat.id, emoji.emojize(
            "Узнайте последние новости и будьте в курсе всех событий!\nКак только я Вам понадоблюсь, напишите - /start"))
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDPjhhiX_Ns9nFyd7paB2WA2QH2Oo2iQACDQADwDZPE6T54fTUeI1TIgQ')
    elif message.text == 'Пожалуй, нет!':
        bot.send_message(message.chat.id,
                         "Тогда увидимя в следующий раз \nКак только я Вам понадоблюсь, напишите /start")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDPjhhiX_Ns9nFyd7paB2WA2QH2Oo2iQACDQADwDZPE6T54fTUeI1TIgQ')
    else:
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')  # кнопка «Нет»
        keyboard.add(key_no)

        locale.setlocale(locale.LC_ALL, '')
        today = datetime.today()
        d = today.strftime('%d %b %Y')

        for k, v in CURRENCY_RATE.items():
            if message.text.lower() == k:
                bot.send_message(message.chat.id,
                                 f'Курс BYN по отношению к {v[3]} {v[4]} на {d} г.''\n''\n'
                                 f'Продажа валюты банком: {v[0]}''\n'
                                 f'Покупка валюты банком: {v[1]}''\n'
                                 f'Курс НБ РБ: {v[2]}''\n''\n')
                bot.send_message(message.chat.id, 'Желаете узнать курс другой валюты?', reply_markup=keyboard)


@bot.message_handler(func=lambda call: True)
def currency_2():
    callback_worker_1


bot.polling()
