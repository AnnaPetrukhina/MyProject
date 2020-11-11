# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database
import logging
import cv2
import bs4
import requests
import peewee
import re
from playhouse.db_url import connect
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor
from models import Weather

RE_DATE = r"^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.)(0[1-9]|1[0-2])(\.)[0-9][0-9]$"
DATABASE_PROXY = peewee.DatabaseProxy()

CONDITIONS = {"clear": "Ясно",
              "partly cloudy": "Переменная облачность",
              "overcast": "Пасмурная погода",
              "mostly cloudy": "В основном облачно",
              "rain": "Дождь",
              "drizzle": "Моросит",
              "light rain": "Легкий дождь",
              "heavy rain": "Ливень",
              "sleet": "Мокрый снег",
              "light sleet": "Легкий мокрый снег",
              "heavy sleet": "Сильный мокрый снег",
              "snow": "Снег",
              "flurries": "Очень легкий снег",
              "light snow": "Легкий снег",
              "heavy snow": "Сильный снег",
              "foggy": "Туманно"
              }


class WeatherMaker:

    def __init__(self, date=None):
        if date is None:
            date = datetime.now()
            self.date = date.strftime("%Y-%m-%d")
        else:
            self.date = date
        self.url = f"https://darksky.net/details/55.7616,37.6095/{self.date}/si12/en"
        self.wind = ""
        self.humidity = ""
        self.weather = "неизвестно"

    def _get_temperature(self, temperature, high_low_temperature):
        average_temperature = temperature.find_next('span', class_='num').contents
        units_temperature = temperature.find_next('span', class_='unit').contents
        average_temperature.extend(units_temperature)
        self.average_temperature = "".join(average_temperature)
        high_low = []
        for temperature in high_low_temperature:
            high_low.extend(temperature.contents)
        self.low_temperature = high_low[0]
        self.high_temperature = high_low[1]

    @staticmethod
    def _get_information(information):
        inf = information.find_next("span", class_="num swip").contents + \
              information.find_next("span", class_="unit swap").contents
        return "".join(inf)

    def _get_weather(self, weather):
        weather_english = weather.contents
        if len(weather_english) != 0:
            for condition_en, condition_ru in CONDITIONS.items():
                log.debug(f"Ищем CONDITIONS в {weather_english[0]}")
                if condition_en in weather_english[0].lower():
                    self.weather = condition_ru
        log.debug("Погода неизвестна")

    def parser(self):
        try:
            html = requests.get(self.url).text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            temperature = soup.find('div', class_="temperature")
            high_low_temperature = soup.find_all('span', class_='temp')
            self._get_temperature(temperature=temperature, high_low_temperature=high_low_temperature)
            wind = soup.find('div', class_="wind")
            self.wind = self._get_information(information=wind)
            humidity = soup.find('div', class_="humidity")
            self.humidity = self._get_information(information=humidity)
            weather = soup.find('p', id="summary")
            self._get_weather(weather=weather)
        except Exception as exp:
            log.info(f"Неожиданная ошибка: {exp}")
            print(f"Неожиданная ошибка: {exp}")

    def run(self):
        self.parser()
        self.date = datetime.strptime(self.date, "%Y-%m-%d")
        self.date = self.date.strftime("%d.%m.%y")
        weather = {
            "дата": self.date,
            "средняя температура": self.average_temperature,
            "максимальная температура": self.high_temperature,
            "минимальная температура": self.low_temperature,
            "ветер": self.wind,
            "влажность": self.humidity,
            "погода": self.weather
        }
        log.debug(weather)
        return weather


class ImageMaker:

    def __init__(self, weather_date, path, path_result, show=True):
        self.weather_date = weather_date
        self.image_for_postcard = {
            "переменная облачность": "cloud.jpg",
            "в основном облачно": "cloud.jpg",
            "пасмурная погода": "cloud.jpg",
            "туманно": "cloud.jpg",
            "дождь": "rain.jpg",
            "моросит": "rain.jpg",
            "легкий дождь": "rain.jpg",
            "ливень": "rain.jpg",
            "сильный снег": "snow.jpg",
            "легкий снег": "snow.jpg",
            "мокрый снег": "snow.jpg",
            "легкий мокрый снег": "snow.jpg",
            "сильный мокрый снег": "snow.jpg",
            "снег": "snow.jpg",
            "очень легкий снег": "snow.jpg",
            "ясно": "sun.jpg",
            "неизвестно": "question.jpg"
        }

        self.method = {
            "cloud.jpg": lambda step: (120 + step // 4, 120 + step // 4, 120 + step // 4),
            "rain.jpg": lambda step: (255, step // 2, step // 2),
            "snow.jpg": lambda step: (255, 255, step // 2),
            "sun.jpg": lambda step: (step // 2, 255, 255),
            "question.jpg": lambda step: (step // 2, 255, 255)
        }
        self.path = path
        self.path_result = path_result
        self.empty_path = path / "empty.jpg"
        self.image = cv2.imread(f"{self.empty_path}")
        self.thickness = 10
        self.show = show

    def weather_condition(self, image, picture, state_weather):
        width = image.shape[1]
        height = image.shape[0]
        image_weather = cv2.imread(f"{picture}")
        for step in range(0, width + 1, 5):
            color = self.method[state_weather](step)
            start_point = (step, 0)
            end_point = (step, height)
            image = cv2.line(image, start_point, end_point, color, self.thickness)
        image[50:50 + image_weather.shape[0], 25:25 + image_weather.shape[1]] = image_weather
        return image

    def add_text(self):
        im = Image.open(self.path_result)
        draw = ImageDraw.Draw(im)
        font_path_ticket = Path.cwd() / "fonts" / "ofont.ru_Bressay Trial.ttf"
        font = ImageFont.truetype(f"{font_path_ticket}", size=30)
        draw.text((17, 20), f'{self.weather_date["дата"]}', font=font, fill=ImageColor.colormap['black'])
        draw.text((135, 100), f'{self.weather_date["средняя температура"]}',
                  font=font, fill=ImageColor.colormap['black'])
        draw.text((140, 65), f'{self.weather_date["погода"]}', font=font, fill=ImageColor.colormap['black'])
        draw.text((20, 160), f'{self.weather_date["минимальная температура"]} ... '
                             f'{self.weather_date["максимальная температура"]}',
                  font=font, fill=ImageColor.colormap['black'])
        font = ImageFont.truetype(f"{font_path_ticket}", size=25)
        draw.text((290, 175), f'Ветер: {self.weather_date["ветер"]}', font=font, fill=ImageColor.colormap['black'])
        draw.text((290, 210), f'Влажность: {self.weather_date["влажность"]}',
                  font=font, fill=ImageColor.colormap['black'])
        im.save(self.path_result)

    def show_postcard(self):
        postcard = cv2.imread(f"{self.path_result}")
        cv2.imshow("Image_probe", postcard)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def run(self):
        image = cv2.imread(f"{self.empty_path}")
        weather = self.weather_date["погода"]
        state_weather = "question.jpg"
        postcard_image = self.path / state_weather
        if weather.lower() in self.image_for_postcard:
            postcard_image = self.path / self.image_for_postcard[weather.lower()]
            state_weather = self.image_for_postcard[weather.lower()]
        postcard = self.weather_condition(image=image, picture=postcard_image, state_weather=state_weather)
        cv2.imwrite(f"{self.path_result}", postcard)
        self.add_text()
        if self.show:
            self.show_postcard()


class DatabaseUpdater:

    def __init__(self, weather_data, beginning_period, end_period):
        self.weather = weather_data
        self.request = beginning_period
        self.start = beginning_period
        self.end = end_period
        self.state = {"saving": self.adding_weather_forecasts,
                      "receiving": self.getting_weather_forecasts}

    def _data_collection(self):
        try:
            data = Weather.get(Weather.date == self.request)
            return {"дата": self.request,
                    "средняя температура": data.average_temperature,
                    "максимальная температура": data.high_temperature,
                    "минимальная температура": data.low_temperature,
                    "ветер": data.wind,
                    "влажность": data.humidity,
                    "погода": data.weather_description}
        except Exception as ex:
            log.info(f"Ошибка: {ex}")
            print(f"{self.request} нет в БД")
            return 0

    def _saving_data(self):
        try:
            Weather.create(
                date=self.weather["дата"],
                average_temperature=self.weather["средняя температура"],
                low_temperature=self.weather["минимальная температура"],
                high_temperature=self.weather["максимальная температура"],
                wind=self.weather["ветер"],
                humidity=self.weather["влажность"],
                weather_description=self.weather["погода"]
            )
        except peewee.IntegrityError:
            print(f"{self.weather['дата']} уже есть в БД")
            log.debug(f"{self.weather['дата']} уже есть в БД")
        except Exception as ex:
            log.info(f"Ошибка: {ex}")

    def adding_weather_forecasts(self, date, weather_data):
        date_weather = date.strftime("%Y-%m-%d")
        self.weather = WeatherMaker(date=date_weather).run()
        self.request = date.strftime("%d.%m.%y")
        log.debug(f"{date} сохраняем в БД")
        self._saving_data()
        return weather_data

    def getting_weather_forecasts(self, date, weather_data):
        self.request = date.strftime("%d.%m.%y")
        log.debug(f"{date} получаем из БД")
        w = self._data_collection()
        weather_data.append(w)
        return weather_data

    def period(self, state):
        if self.start > self.end:
            self.start, self.end = self.end, self.start
        log.debug(f"Период: {self.start, self.end}")
        weather_for_period = []
        beginning_period = self.start
        while beginning_period <= self.end:
            weather_for_period = self.state[state](date=beginning_period, weather_data=weather_for_period)
            beginning_period += timedelta(days=1)
        return weather_for_period

    def getting_postcard(self, path_img, weather_data=None, show=False):
        if weather_data is None or len(weather_data) == 0:
            weather_data = self.period(state="receiving")
            log.debug("Получение данных для создания открытки")
        for data in weather_data:
            if data != 0:
                path_postcard = path_img / "weather_postcard" / f"postcard_{data['дата']}.jpg"
                im_maker = ImageMaker(weather_date=data, path=path_img, path_result=path_postcard, show=show)
                im_maker.run()

    def show_weather(self, weather_data=None):
        if weather_data is None or len(weather_data) == 0:
            weather_data = self.period(state="receiving")
            log.debug("Получение данных для показа погоды")
        for data in weather_data:
            if data != 0:
                print(f"Погода {data['дата']}:")
                for k, v in data.items():
                    if k == "дата":
                        continue
                    elif k == "погода":
                        print(v)
                    else:
                        print(f"{k}: {v}")
                print(" ")


def date_period():
    period_weather = input("Введите начало перида, конец периода через пробел с запятой "
                           "(дата в формате день.месяц.год) >>> ")
    try:
        beginning_period, end_period = period_weather.split(", ")
        while re.fullmatch(RE_DATE, beginning_period) is None or re.fullmatch(RE_DATE, end_period) is None:
            period_weather = input("Вы ввели неправильно. Попробуйте еще раз >>> ")
            beginning_period, end_period = period_weather.split(", ")
        beginning_period = datetime.strptime(beginning_period, "%d.%m.%y")
        end_period = datetime.strptime(end_period, "%d.%m.%y")
        return beginning_period, end_period
    except Exception as ex:
        log.info(f"Произошла ошибка {ex} при вводе периода")
        return 0, 0


def get_date_period(beginning_period, end_period):
    while beginning_period == end_period == 0:
        print("Вы ввели неправильно. Попробуйте еще раз")
        beginning_period, end_period = date_period()
    return beginning_period, end_period


def weather_last_week(path_img):
    end_period = datetime.now() - timedelta(days=1)
    log.debug(f"Конец недели {end_period}")
    beginning_period = end_period - timedelta(days=6)
    log.debug(f"Начало недели {beginning_period}")
    print(f"Погода за прошлую неделю ({beginning_period.strftime('%d.%m.%y')}"
          f"-{end_period.strftime('%d.%m.%y')}):\n")
    db_last_week = DatabaseUpdater(weather_data=None, beginning_period=beginning_period, end_period=end_period)
    db_last_week.period(state="saving")
    log.debug("Добавили данные погоды за прошлую неделю в БД")
    weather = db_last_week.period(state="receiving")
    db_last_week.getting_postcard(path_img=path_img, weather_data=weather, show=True)
    db_last_week.show_weather(weather_data=weather)


def actions_available_user(selecting_user_action, user_action, weather_date, db_user_action):
    if len(weather_date) != 0:
        log.debug(f"Данные о погоде за период {db_user_action.start, db_user_action.end} уже получены")
        postcard_date_weather_period = weather_date
    else:
        log.debug(f"Данных о погоде за период {db_user_action.start, db_user_action.end} нет")
        postcard_date_weather_period = None

    log.debug(f"Пользователь выбрал действие {selecting_user_action}")
    if selecting_user_action == "1" or selecting_user_action == "2":
        log.debug(f"Действие {user_action[0]}")
        weather_date = user_action[1](state=user_action[2])
    elif selecting_user_action == "3":
        log.debug(f"Действие {user_action[0]}")
        user_action[1](path_img=path_img_weather, weather_data=postcard_date_weather_period, show=True)
    elif selecting_user_action == "4":
        log.debug(f"Действие {user_action[0]}")
        user_action[1](weather_data=postcard_date_weather_period)
    return weather_date


log = logging.getLogger('Weather')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("weather.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
fh.setFormatter(formatter)
log.addHandler(fh)

if __name__ == '__main__':
    path_img_weather = Path.cwd() / "weather_img"
    database = connect("sqlite:///weather.db ")
    DATABASE_PROXY.initialize(database)
    DATABASE_PROXY.create_tables([Weather])

    print("Погода в Москве с добавлением прогнозов в БД\n")
    weather_last_week(path_img=path_img_weather)
    start, end = date_period()
    start, end = get_date_period(beginning_period=start, end_period=end)
    db = DatabaseUpdater(weather_data=None, beginning_period=start, end_period=end)
    action = {
        "1": ["Добавить в базу прогноз погоды за этот период", db.period, "saving"],
        "2": ["Получить из базы прогноз погоды за этот период", db.period, "receiving"],
        "3": ["Создание открыток за этот период", db.getting_postcard],
        "4": ["Выведение полученных прогнозов за этот период", db.show_weather],
        "5": ["Поменять период"],
        "6": ["Выход"],
    }

    print("Доступные действия:")
    for key, value in action.items():
        print(f"{key}: {value[0]}")

    choice_user = input("Выберите действие >>> ")
    weather_period = []
    while choice_user != "6":
        if choice_user == "5":
            log.debug(f"Действие {action[choice_user][0]}")
            start, end = date_period()
            start, end = get_date_period(beginning_period=start, end_period=end)
            db = DatabaseUpdater(weather_data=weather_period, beginning_period=start, end_period=end)
        elif choice_user in action:
            weather_period = actions_available_user(selecting_user_action=choice_user, user_action=action[choice_user],
                                                    weather_date=weather_period, db_user_action=db)
        else:
            log.debug(f"Пользователь ввел данные, которых нет в предложенных вариантах {choice_user}")
            print("Попробуйте выбрать другое действие")
        choice_user = input("Выберите действие >>> ")
    log.debug(f"Действие {action[choice_user][0]}")
