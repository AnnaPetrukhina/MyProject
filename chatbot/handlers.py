import logging
from datetime import datetime
from random import choice
from pony.orm import db_session

from fuzzywuzzy import process
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup)
from telegram import ParseMode
from telegram.ext import ConversationHandler

import telegramcalendar
from models import Registration
from settings import CITIES, FLIGHT_SCHEDULE
from dispatcher import getting_date
from generate_ticket import make_ticket

CITY_OF_DEPARTURE, CHECK_CITY_OF_DEPARTURE, ARRIVAL_CITY, CHECK_ARRIVAL_CITY, = range(4)
METHOD_OF_DATE_SELECTION, DATE_OF_DEPARTURE, FLIGHT, NUMBER_OF_SEATS, COMMENT, = range(4, 9)
DATA_VALIDATION, PHONE_NUMBER, CHECK_PHONE_NUMBER = range(9, 12)
FLIGHT_CALENDAR, NUMBER_OF_SEATS_CALENDAR, NAME, GENDER = range(12, 16)

GIRL = [
    "jenni", "jolee", "jabala", "jaqueline", "jocelyn", "jane", "josephine", "jess", "julie", "jazebelle",
    "jodi", "jana", "jeane", "jeri"
]
BOY = [
    "jake", "josh", "james", "jai", "jed", "jude", "jerry", "jon", "joe", "jia", "jack", "jacques", "jean", "jordan"
]

# Enable logging
log = logging.getLogger('ChatBot')


def show_cities(update, context):
    """
    Отправка пользователю списка возможных городов
    """
    log.info("Выбрано показать города")
    text = "Возможные города:"
    for city in CITIES:
        text += f"\n{city}"
    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML)


def calendar_handler(update, context):
    """
    Отображение календаря на экране
    """
    log.info("Выбрано показать календарь")
    update.message.reply_text("пожалуйста, выберите дату: ", reply_markup=telegramcalendar.create_calendar())
    return DATE_OF_DEPARTURE


def check_date_calendar(update, context, date):
    """
    Вывод ближайших дат
    """
    context.user_data['date_of_departure'] = date.strftime("%d-%m-%Y")
    dates = getting_date(
        flight_date=context.user_data['date_of_departure'],
        departure_city=context.user_data['city_of_departure'],
        arrival_city=context.user_data['arrival_city']
    )
    context.user_data['flight'] = dates[1]
    proposed = [some_of_date for some_of_date in chunks(lst=dates[0], count=2)]
    button = []
    for i, lst_dates in enumerate(proposed):
        button.append([])
        for date_flight in lst_dates:
            button[i].append(InlineKeyboardButton(f"{date_flight}", callback_data=str(date_flight)))
    reply_markup = InlineKeyboardMarkup(button)
    update.callback_query.edit_message_text(
        text=f"Вы выбрали {context.user_data['date_of_departure']}\n"
        f"Ближайшие даты:", reply_markup=reply_markup
    )


def inline_handler(update, context):
    """
    Обработка нажатия кнопок на календаре и вывод пользователю ближайших рейсов к введенной дате
    """
    log.info("отображение календаря")
    query = update.callback_query  # данные которые приходят после нажатия кнопки
    selected, date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        query.edit_message_text(
            text="Вы выбрали %s" % (date.strftime("%d-%m-%Y"))
        )
        now = datetime.now()
        log.info(f"выбрана дата {date}, сегодня {now}")
        if date > now:
            log.info(f"{date} > {now}")
            check_date_calendar(update, context, date)
            return FLIGHT_CALENDAR
        else:
            log.info(f"{date} < {now}")
            query.edit_message_text(f"На вчера купить билет нельзя!")
            return DATE_OF_DEPARTURE


def flight_calendar(update, context):
    """
    Обработка нажатия выбронной даты и выбор пользователя количества мест
    """
    log.info("выбор даты ближайшего рейса")
    query = update.callback_query
    context.user_data['date_of_departure'] = query.data
    button = []
    for i in range(1, 6):
        button.append(InlineKeyboardButton(f"{i}", callback_data=str(i)))
    reply_markup = InlineKeyboardMarkup([button])
    query.edit_message_text(text=f"Выберите количество мест", reply_markup=reply_markup)
    return NUMBER_OF_SEATS_CALENDAR


def number_of_seats_calendar(update, context):
    """
    Обработка нажатия на кнопку выбора мест и предложениие пользователю ввести комментарий
    """
    log.info("выбор количества мест")
    query = update.callback_query
    context.user_data['number_of_seats'] = query.data
    query.edit_message_text(text=f"Оставьте комментарий или введите пропустить")
    return COMMENT


def help_command(update, context):
    """
    Обработка команды help
    """
    log.info(f"получена команда /help")
    button = InlineKeyboardButton(text='Сообщение разработчику', url='https://t.me/AnnaPetrukhina')
    replay_keyboard = InlineKeyboardMarkup.from_button(button)
    update.message.reply_text(
        'Введите /start или /ticket, чтобы начать.\n Затем выполняй команды бота.\n '
        'Посмотреть список городов /city. Закончить заказ билетов команду /cancel',
        reply_markup=replay_keyboard
    )


def other_message(update, context):
    """
    Обработка не текстовых сообщений. При получении такого сообщения завершение разговора
    """
    log.info(f"получено сообщение неизвестного типа {update.message}")
    content_type = {
        'audio': update.message.audio, 'photo': update.message.photo, 'voice': update.message.voice,
        'video': update.message.video, 'document': update.message.document,
        'location': update.message.location, 'contact': update.message.contact, 'sticker': update.message.sticker
    }
    for k, v in content_type.items():
        if v:
            log.info(f"получено сообщение неизвестного типа {k}")
    update.message.reply_text(f"Я не знаю что ответить. Введите /start или /ticket, чтобы начать.")
    return ConversationHandler.END


def cancel(update, context):
    """
    Обработка команды отмена
    """
    log.info(f"получена команда отмена")
    update.message.reply_text("Введите /start или /ticket, чтобы начать заново")
    return ConversationHandler.END


def start(update, context):
    """"
    Обработка команды старт
    """
    log.info(f"получена команда /start")
    update.message.reply_text(
        'Привет! Я бот. Я помогаю подобрать рейс. Для начала введите город отправления\n'
        + 'Получить помощь /help. Посмотреть список городов /city'
    )
    return CITY_OF_DEPARTURE


def guess_city(city):
    """
    Сравнение введенного города с городами, в которых есть рейсы
    """
    guess = []
    find_cities = process.extract(city, CITIES, limit=len(CITIES))
    for find_city in find_cities:
        if find_city[1] > 50 and len(city) - 2 <= len(find_city[0]) <= len(city) + 2:
            guess.append(find_city[0])
    log.info(f"города похожие на ввод пользователя {guess}")
    return guess


def keyboard(update, proposed, text):
    """
    Создание временной клавиатуры для вывода текста и кнопок
    """
    reply_keyboard = [proposed]
    update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )


def check_city_of_departure(update, context):
    """
    Получение результотов проверки города отправления.
    """
    text = update.message.text
    log.info(f"проверка города отправления. Пользователь выбрал {text}")
    if text == "Моего города нет":
        update.message.reply_text(f"Введите город отправления.")
        return CITY_OF_DEPARTURE
    else:
        context.user_data['city_of_departure'] = text
        update.message.reply_text(f"Введен город отправления {text}.")
        update.message.reply_text(f"Введите город прибытия.")
        return ARRIVAL_CITY


def city_of_departure(update, context):
    """
    Получение города отправления и его проверка.
    """
    log.info(f"получен город вылета {update.message.text}")
    text = update.message.text.capitalize()
    if text in CITIES:
        context.user_data['city_of_departure'] = text
        update.message.reply_text(f"Введен город отправления {text}.")
        update.message.reply_text(f"Введите город прибытия.")
        return ARRIVAL_CITY
    else:
        proposed_cites = guess_city(text)
        if len(proposed_cites) == 0:
            update.message.reply_text(f"Введите город отправления.")
            return CITY_OF_DEPARTURE
        else:
            proposed_cites.append("Моего города нет.")
            keyboard(update, proposed_cites, text="Ваш город отправления?")
            return CHECK_CITY_OF_DEPARTURE


def check_arrival_city(update, context):
    """
    Проверка города прибытия
    """
    text = update.message.text
    log.info(f"проверка города прибытия. Пользователь выбрал {text}")
    if text == "Моего города нет":
        update.message.reply_text(f"Введите город прибытия.")
        return ARRIVAL_CITY
    else:
        context.user_data['arrival_city'] = text
        update.message.reply_text(f"Введен город прибытия {text}.")
        if connection_between_cities(context):
            proposed = ["показать календарь", "ввести самому"]
            keyboard(update, proposed, text="Вы хотите ввести дату или выбрать на календаре?")
            return METHOD_OF_DATE_SELECTION
        else:
            log.info(
                f"Между городами {context.user_data['city_of_departure']} и {context.user_data['arrival_city']} "
                f"нет рейсов!"
            )
            update.message.reply_text(
                f"Между городами {context.user_data['city_of_departure']} и "
                f"{context.user_data['arrival_city']} нет рейсов! "
                f"Если хотите попробовать снова, введите /start или /ticket."
            )
            return ConversationHandler.END


def arrival_city(update, context):
    """
    Получение города прибытия
    """
    log.info(f"получен город прилета {update.message.text}")
    text = update.message.text.capitalize()
    if text in CITIES:
        context.user_data['arrival_city'] = text
        update.message.reply_text(f"Введен город прибытия {text}.")
        if connection_between_cities(context):
            proposed = ["показать календарь", "ввести самому"]
            keyboard(update, proposed, text="Вы хотите ввести дату или выбрать на календаре?")
            return METHOD_OF_DATE_SELECTION
        else:
            log.info(
                f"Между городами {context.user_data['city_of_departure']} и {context.user_data['arrival_city']} "
                f"нет рейсов!"
            )
            update.message.reply_text(
                f"Между городами {context.user_data['city_of_departure']} и "
                f"{context.user_data['arrival_city']} нет рейсов! "
                f"Если хотите попробовать снова, введите /start или /ticket"
            )
            return ConversationHandler.END
    else:
        proposed_cites = guess_city(text)
        if len(proposed_cites) == 0:
            update.message.reply_text(f"Введите город прибытия.")
            return ARRIVAL_CITY
        else:
            proposed_cites.append("Моего города нет.")
            keyboard(update, proposed_cites, text="Ваш город прибытия?")
            return CHECK_ARRIVAL_CITY


def connection_between_cities(context):
    """
    Проверка наличия рейсов между городами
    """
    city_departure = context.user_data['city_of_departure']
    city_arrival = context.user_data['arrival_city']
    if city_arrival in FLIGHT_SCHEDULE[city_departure]:
        log.info(f"между городами {city_departure} и {city_arrival} есть рейсы")
        return True
    else:
        log.info(f"между городами {city_departure} и {city_arrival} нет рейсов")
        return False


def date_input(update, context):
    """
    Ввод даты пользователем
    """
    log.info(f"пользователь сам введет дату")
    update.message.reply_text(f"Введите дату отправления.")
    return DATE_OF_DEPARTURE


def calendar(update, context):
    """
    Выбор даты с календаря
    """
    log.info(f"пользователь выберет дату на календаре")
    update.message.reply_text(
        "Пожалуйста, выберите дату: ", reply_markup=telegramcalendar.create_calendar()
    )


def chunks(lst, count):
    """
    Разбиение списка на несколько частей
    """
    start_lst = 0
    for i in range(count + 1):
        stop = start_lst + len(lst[i::count + 1])
        yield lst[start_lst:stop]
        start_lst = stop


def date_of_departure(update, context):
    """
    Получение даты введенной пользователем. Предложение пользователю ближайших дат
    """
    log.info(f"получена желаемая дата вылета {update.message.text}")
    now = datetime.now()
    date_flight = datetime.strptime(update.message.text, '%d-%m-%Y')
    if date_flight > now:
        context.user_data['date_of_departure'] = update.message.text
        update.message.reply_text(f"Введена дата отправления {update.message.text}.")
        dates = getting_date(
            flight_date=context.user_data['date_of_departure'],
            departure_city=context.user_data['city_of_departure'],
            arrival_city=context.user_data['arrival_city']
        )
        context.user_data['flight'] = dates[1]
        proposed = [some_of_date for some_of_date in chunks(lst=dates[0], count=2)]
        update.message.reply_text(
            "Ближайшие даты:",
            reply_markup=ReplyKeyboardMarkup(proposed, resize_keyboard=True, one_time_keyboard=True)
        )
        return FLIGHT
    else:
        update.message.reply_text(f"На вчера купить билет нельзя!")
        return DATE_OF_DEPARTURE


def not_correct_date_of_departure(update, context):
    """
    Ответ пользователю, что введена некорректная дата
    """
    log.info(f"получено некорректное время вылета {update.message.text}")
    update.message.reply_text(
        f"Введена некорректная дата отправления {update.message.text}! "
        f"Дата должна быть в формате день-месяц-год (4 цифры)."
    )
    update.message.reply_text(f"Введите дату отправления.")
    return DATE_OF_DEPARTURE


def flight(update, context):
    """
    Получение даты рейса и предложение польхователю введения количества мест
    """
    log.info(f"получен дата вылета {update.message.text}")
    context.user_data['date_of_departure'] = update.message.text
    proposed = ["1", "2", "3", "4", "5"]
    keyboard(update, proposed, text="Выберите количество мест от 1 до 5.")
    return NUMBER_OF_SEATS


def number_of_seats(update, context):
    """
    Получение количества мест и предложение пользователю лставить комментарий
    """
    log.info(f"получено количество мест {update.message.text}")
    context.user_data['number_of_seats'] = update.message.text
    proposed = ["Пропустить"]
    keyboard(update, proposed, text="Напишите комментарий или нажмите кнопку пропустить этот шаг.")
    return COMMENT


def not_correct_number_of_seats(update, context):
    """
    Ответ пользователю, что введено некорректное число мест
    """
    log.info(f"получено некорректное количество мест {update.message.text}")
    update.message.reply_text(f"Введено некорректное количество мест. Надо ввести от 1 до 5 или выбрать на клавиатуре!")
    return NUMBER_OF_SEATS


def data_verification(update, context):
    """
    Предложение пользователю проверить введенные данные
    """
    log.info(f"проверка введенных данных")
    reply_keyboard = [["да", "нет"]]
    text = """Выбранный рейс:
            <b>Город отправления:</b> {city_of_departure}
            <b>Город назначения:</b> {arrival_city}
            <b>Дата отправления:</b> {date_of_departure}
            <b>Рейс:</b> {flight}
            <b>Количество мест:</b> {number_of_seats}
            <b>Комментарий:</b> {comment}""".format(**context.user_data)
    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True))


def exit_comment(update, context):
    """
    Пропуск комментария
    """
    log.info(f"комментария нет")
    context.user_data['comment'] = "нет комментария"
    data_verification(update, context)
    return DATA_VALIDATION


def comment(update, context):
    """
    Получение комментария
    """
    log.info(f"получен комментарий {update.message.text}")
    context.user_data['comment'] = update.message.text
    data_verification(update, context)
    return DATA_VALIDATION


def data_validation(update, context):
    """
    Проверка данных введенных пользователем
    """
    if update.message.text == "да":
        log.info(f"данные введены верно")
        update.message.reply_text("Введите Фамилию Имя Отчество (инициалы с точкой).")
        return NAME
    else:
        log.info(f"в данных есть ошибка")
        update.message.reply_text("Введите /start или /ticket, чтобы начать заново.")
        return ConversationHandler.END


def name(update, context):
    """
    Получение ФИО клиента
    """
    log.info(f"получен фИО {update.message.text}")
    context.user_data["name"] = update.message.text
    proposed = ["мужской", "женский"]
    keyboard(update, proposed, text="Выберите ваш пол.")
    # update.message.reply_text("Введите ваш пол")
    return GENDER


def gender_person(update, context):
    """
    Получение пола клиента
    """
    log.info(f"получен пол {update.message.text}")
    person = choice(BOY) if update.message.text == "мужской" else choice(GIRL)
    context.user_data["name_avatar"] = person
    update.message.reply_text("Введите номер телефона.")
    return PHONE_NUMBER


def phone_number(update, context):
    """
    Получение номера телефона
    """
    log.info(f"получен номер телефона {update.message.text}")
    update.message.reply_text(f"Введен номер телефона {update.message.text}.")
    context.user_data['phone_number'] = update.message.text
    proposed = ["да", "нет"]
    keyboard(update, proposed, text="Это правильный телефон?")
    return CHECK_PHONE_NUMBER


def not_correct_phone_number(update, context):
    """
    Ответ пользователю, что введен некорректный телефон
    """
    log.info(f"получен некорректный номер телефона {update.message.text}")
    update.message.reply_text(
        f"Введен некорректный номер телефона {update.message.text}! "
        f"Телефон должен содержать 11 цифр (начинаться с 8 или +7)."
    )
    update.message.reply_text(f"Введите номер телефона.")
    return PHONE_NUMBER


@db_session
def check_phone_number(update, context):
    """
    Проверка номера телефона пользователя и занесение данных в БД
    """
    if update.message.text == "да":
        log.info(f"получен верный номер телефона")
        update.message.reply_text(f"Спасибо, {context.user_data['name']}! Ожидайте звонка. Ваш билет.")
        image_ticket = make_ticket(
            fio=context.user_data['name'], from_=context.user_data["city_of_departure"],
            to=context.user_data["arrival_city"], date=context.user_data["date_of_departure"],
            person=context.user_data["name_avatar"]
        )
        context.bot.send_photo(chat_id=update.message.chat.id, photo=open(image_ticket, 'rb'))
        Registration(
            name=context.user_data['name'],
            date_of_departure=context.user_data["date_of_departure"],
            city_of_departure=context.user_data["city_of_departure"],
            arrival_city=context.user_data["arrival_city"],
            flight=context.user_data["flight"],
            number_of_seats=context.user_data["number_of_seats"],
            comment=context.user_data["comment"],
            phone_number=context.user_data["phone_number"],
            name_avatar=context.user_data["name_avatar"]
        )
        return ConversationHandler.END
    else:
        log.info(f"получен неверный номер телефона")
        update.message.reply_text("Введите номер телефона.")
        return PHONE_NUMBER
