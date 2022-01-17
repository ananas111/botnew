#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit
import requests
from random import randint
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_KEY = getenv("API_KEY")
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
api_link_ria = 'https://developers.ria.com/auto/search?api_key=' + API_KEY + "&category_id=1"


class ChooseCar(StatesGroup):
    waiting_for_brand_name = State()
    waiting_for_model_name = State()
    waiting_for_area = State()


@dp.message_handler(commands="random")
async def cmd_random(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10", reply_markup=keyboard)


@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(str(randint(1, 10)))
    await call.answer()


@dp.message_handler(commands=["start"])
async def cmd_test1(message: types.Message):
    brands_api = 'https://developers.ria.com/auto/categories/1/marks?api_key=' + API_KEY
    brands_list = requests.get(brands_api).json()
    buttons_list = []
    for i in range(len(brands_list)):
        brand = brands_list[i]['name']
        buttons_list.append(brand)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = buttons_list
    keyboard.add(*buttons)
    send_mess = f"<b> Привет {message.from_user.first_name} {message.from_user.last_name} " \
                f"</b>!\nКакая марка тебя интересует?"
    await bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=keyboard)
    await ChooseCar.waiting_for_brand_name.set()


@dp.message_handler(content_types=['text'], state=ChooseCar.waiting_for_brand_name)
async def models(message: types.Message, state: FSMContext):
    await state.update_data(brand=message.text.strip())
    brand = message.text
    brand_id = get_brand_id(brand)
    models_api = 'https://developers.ria.com/auto/categories/1/marks/' + str(brand_id) + '/models?api_key=' + API_KEY
    models_list = requests.get(models_api).json()
    buttons_list = []
    for i in range(len(models_list)):
        model_name = models_list[i]['name']
        buttons_list.append(model_name)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = buttons_list
    keyboard.add(*buttons)
    send_mess = f"Какая модель тебя интересует?"
    await bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=keyboard)
    await ChooseCar.waiting_for_model_name.set()


@dp.message_handler(content_types=['text'], state=ChooseCar.waiting_for_model_name)
async def select_area(message: types.Message, state: FSMContext):
    await state.update_data(model_name=message.text.strip())
    area_api = 'https://developers.ria.com/auto/states?api_key=' + API_KEY
    area_list = requests.get(area_api).json()
    list_areas = []
    for i in range(len(area_list)):
        area_name = area_list[i]['name']
        list_areas.append(area_name)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = list_areas
    keyboard.add(*buttons)
    send_mess = f"Какая область тебя интересует?"
    await bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=keyboard)
    await ChooseCar.waiting_for_area.set()


@dp.message_handler(content_types=['text'], state=ChooseCar.waiting_for_area)
async def model_ads(message: types.Message, state: FSMContext):
    area_name = message.text
    area_id = get_area_id(area_name)
    user_data = await state.get_data()
    model_name = user_data['model_name']
    brand = user_data['brand']
    brand_id = get_brand_id(brand)
    model_id = get_model_id(brand_id, model_name)
    model_search_api = api_link_ria + '&marka_id=' + str(brand_id) + "&model_id=" + str(model_id) + '&state[0]=' + str(area_id)
    model = requests.get(model_search_api).json()
    ads_id_list = model['result']['search_result']['ids']
    list_ads = []
    for i in range(len(ads_id_list)):
        car_api = 'https://developers.ria.com/auto/info?api_key=' + API_KEY + '&auto_id=' + ads_id_list[i]
        cars_id_list = requests.get(car_api).json()
        car_link = 'https://auto.ria.com/uk' + cars_id_list['linkToView']
        await bot.send_message(message.chat.id, f"{car_link}")
        list_ads.append(car_link)
    print(list_ads)
    await state.finish()


def get_area_id(area_name):
    area_api = 'https://developers.ria.com/auto/states?api_key=' + API_KEY
    area_list = requests.get(area_api).json()
    for i in range(len(area_list)):
        if area_list[i]['name'] == area_name:
            area_id = area_list[i]['value']
            return area_id
        else:
            i += 1






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


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
