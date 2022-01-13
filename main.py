import telebot
from telebot import types
import requests
from config import API_KEY, token
from sqlalchemy import create_engine
from telegram_bot_pagination import InlineKeyboardPaginator

bot = telebot.TeleBot(token)
api_link_ria = 'https://developers.ria.com/auto/search?api_key=' + API_KEY + "&category_id=1"
engine = create_engine('postgresql://postgres:123@localhost/bot')


'''
@bot.message_handler(commands=['insta'])
def instagram(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти в Инстаграм", url="https://www.instagram.com/itproger_official/"))
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже и погрузитесь в мир IT прямо сейчас",
                     parse_mode='html', reply_markup=markup)
'''


@bot.message_handler(commands=['start'])   #/start - Main menu
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    brands_api = 'https://developers.ria.com/auto/categories/1/marks?api_key=' + API_KEY
    brands_list = requests.get(brands_api).json()
    for i in range(len(brands_list)):
        brand = brands_list[i]['name']
        btn = types.KeyboardButton(f'{brand}')
        markup.add(btn)
    send_mess = f"<b> Привет {message.from_user.first_name} {message.from_user.last_name} " \
                f"</b>!\nКакая марка тебя интересует?"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def models(message):
    get_message_bot = message.text.strip()
    brand = get_message_bot
    brand_id = get_brand_id(brand)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    models_api = 'https://developers.ria.com/auto/categories/1/marks/' + str(brand_id) + '/models?api_key=' + API_KEY
    models_list = requests.get(models_api).json()
    for i in range(len(models_list)):
        model_name = models_list[i]['name']
        btn = types.KeyboardButton(f'{model_name}')
        markup.add(btn)
    send_mess = f"Какая модель тебя интересует?"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, model_ads, brand_id=brand_id)


@bot.message_handler(content_types=['text'])
def model_ads(message, brand_id):
    get_message_bot = message.text.strip()
    model_name = get_message_bot
    model_id = get_model_id(brand_id, model_name)
    model_search_api = api_link_ria + '&marka_id=' + str(brand_id) + "&model_id=" + str(model_id)
    model = requests.get(model_search_api).json()
    ads_id_list = model['result']['search_result']['ids']
    list_ads = []
    i = 0
    while i < len(ads_id_list):
        for i in range(3):
            car_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + ads_id_list[i]
            cars_id_list = requests.get(car_api).json()
            car_link = 'https://auto.ria.com/uk' + cars_id_list['linkToView']
            bot.send_message(message.chat.id, f"{car_link}")
            list_ads.append(car_link)
            i += 3

    print(list_ads)


def get_brand_id(brand):
    brands_api = 'https://developers.ria.com/auto/categories/1/marks?api_key=' + API_KEY
    brands_list = requests.get(brands_api).json()
    for i in range(len(brands_list)):
        if brands_list[i]['name'] == brand:
            brand_id = brands_list[i]['value']
            return brand_id
        else:
            i += 1


def get_model_id(brand_id, model_name):
    models_api = 'https://developers.ria.com/auto/categories/1/marks/' + str(brand_id) + '/models?api_key=' + API_KEY
    models_list = requests.get(models_api).json()
    for i in range(len(models_list)):
        if models_list[i]['name'] == model_name:
            model_id = models_list[i]['value']
            return model_id
        else:
            i += 1


def add_paramethers(param):
    api_link_ria = 'https://developers.ria.com/auto/search?api_key=' + API_KEY + "&category_id=1"
    api_link_ria = api_link_ria + param
    return api_link_ria


def get_cars_ids(brand_id, model_id):
    param = f'&marka_id={brand_id}&model_id={model_id}'
    filter_search = requests.get(api_link_ria + param).json()
    models = filter_search['result']['search_result']['ids']
    return models


bot.polling(none_stop=True)
