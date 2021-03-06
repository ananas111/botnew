import telebot
from telebot import types
import requests
from config import API_KEY, token

bot = telebot.TeleBot(token)
api_link_ria = 'https://developers.ria.com/auto/search?api_key=' + API_KEY + "&category_id=1"


@bot.message_handler(commands=['insta'])
def instagram(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти в Инстаграм", url="https://www.instagram.com/itproger_official/"))
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже и погрузитесь в мир IT прямо сейчас",
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('Audi')
    btn2 = types.KeyboardButton('Mercedes-Benz')
    btn3 = types.KeyboardButton('BMW')
    btn4 = types.KeyboardButton('Honda')
    btn5 = types.KeyboardButton('Ford')
    btn6 = types.KeyboardButton('Lexus')
    btn7 = types.KeyboardButton('Другие')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    send_mess = f"<b> Привет {message.from_user.first_name} {message.from_user.last_name} " \
                f"</b>!\nКакая модель тебя интересует?"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


def get_brand_id(brand):
    brands_api = 'https://developers.ria.com/auto/categories/1/marks?api_key=' + API_KEY
    brands_list = requests.get(brands_api).json()
    print(brands_list)
    for i in range(len(brands_list)):
        if brands_list[i]['name'] == brand:
            brand_id = brands_list[i]['value']
            return brand_id
        else:
            i += 1


def add_paramethers(param):
    api_link_ria = 'https://developers.ria.com/auto/search?api_key=' + API_KEY + "&category_id=1"
    api_link_ria = api_link_ria + param
    return api_link_ria


def get_model_id(brand_id):
    param = f'&marka_id={brand_id}'
    filter_search = requests.get(api_link_ria + param).json()
    models = filter_search['result']['search_result']['ids']
    return models


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip()
    if get_message_bot == 'Audi':
        brand_id = get_brand_id(get_message_bot)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}")

    elif get_message_bot == 'Mercedes-Benz':
        brand_id = get_brand_id(get_message_bot)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}")

    elif get_message_bot == 'BMW':
        brand_id = get_brand_id(get_message_bot)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}")

    elif get_message_bot == 'Honda':
        brand_id = get_brand_id(get_message_bot)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}")

    elif get_message_bot == 'Ford':
        brand_id = get_brand_id(get_message_bot)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}")

    elif get_message_bot == 'Lexus':
        brand_id = get_brand_id(get_message_bot)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}")

    elif get_message_bot == "Другие":
        bot.send_message(message.chat.id, 'Введите название модели автомобиля')
        bot.register_next_step_handler(message, other)


@bot.message_handler(content_types=['text'])
def other(message):
    get_message_bot = message.text.strip()
    try:
        brand = get_message_bot
        brands_api = 'https://developers.ria.com/auto/categories/1/marks?api_key=' + API_KEY
        brands_list = requests.get(brands_api).json()
        brand_id = get_brand_id(brand)
        models = get_model_id(brand_id)
        for i in range(len(models)):
            model_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + models[i]
            model = requests.get(model_api).json()
            model_link = 'https://auto.ria.com/uk' + model['linkToView']
            i += 1
            bot.send_message(message.chat.id, f"{model_link}", brands_list)
    except Exception:
        bot.send_message(message.from_user.id, 'Вы ввели данные в неправильном формате.')


bot.polling(none_stop=True, interval=0)
