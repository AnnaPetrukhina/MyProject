
import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler, PicklePersistence)
import handlers

try:
    from settings import TOKEN
except ImportError:
    TOKEN = None
    exit("Скопируйте settings.py.default в settings.py и установите свой токен!")

log = logging.getLogger('ChatBot')


def configure_logger():
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler("bot.log", 'w', 'utf-8', delay=True)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
    fh.setFormatter(formatter)
    log.addHandler(fh)


def main():
    pp = PicklePersistence(filename='ticketbot.txt')
    bot = Updater(TOKEN, persistence=pp, use_context=True)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("help", handlers.help_command))
    dp.add_handler(CommandHandler("city", handlers.show_cities))
    filters = Filters.audio | Filters.photo | Filters.voice | Filters.video | Filters.document
    filters = filters | Filters.location | Filters.contact | Filters.sticker
    re_city = r"\b[а-яА-ЯёЁ]+[-\s]?[а-яА-ЯёЁ]*[-\s]?[а-яА-ЯёЁ]*\b"
    re_date = r"^([1-9]|1[0-9]|2[0-9]|3[0-1])(-)(0[1-9]|1[0-2])(-)20[0-9][0-9]$"
    re_phone = r'\+?[7,8]\s*[-]?\d{3}\s*[-]?\d{3}\s*[-]?\d{2}\s*[-]?\d{2}$'
    re_name = r"|[a-zA-Zа-яА-ЯёЁ]+\s?[A-ZА-ЯЁ]\.[A-ZА-ЯЁ]?\.?"
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start), CommandHandler('ticket', handlers.start)],
        states={
            handlers.CITY_OF_DEPARTURE: [
                MessageHandler(Filters.regex(re_city) & ~Filters.command, handlers.city_of_departure)
            ],
            handlers.CHECK_CITY_OF_DEPARTURE: [
                MessageHandler(Filters.text & ~Filters.command, handlers.check_city_of_departure)
            ],
            handlers.ARRIVAL_CITY: [
                MessageHandler(Filters.regex(re_city) & ~Filters.command, handlers.arrival_city)
            ],
            handlers.CHECK_ARRIVAL_CITY: [
                MessageHandler(Filters.text & ~Filters.command, handlers.check_arrival_city)
            ],
            handlers.METHOD_OF_DATE_SELECTION: [
                MessageHandler(Filters.regex("ввести самому") & ~Filters.command, handlers.date_input),
                MessageHandler(Filters.regex("показать календарь"), handlers.calendar_handler)
            ],
            handlers.DATE_OF_DEPARTURE: [
                CallbackQueryHandler(handlers.inline_handler),
                MessageHandler(Filters.regex(re_date) & ~Filters.command, handlers.date_of_departure),
                MessageHandler(Filters.text & ~Filters.regex(re_date) & ~Filters.command,
                               handlers.not_correct_date_of_departure)
            ],
            handlers.FLIGHT: [MessageHandler(Filters.regex(re_date) & ~Filters.command, handlers.flight)],
            handlers.NUMBER_OF_SEATS: [
                MessageHandler(Filters.regex('1|2|3|4|5') & ~Filters.command, handlers.number_of_seats),
                MessageHandler(Filters.text & ~Filters.command, handlers.not_correct_number_of_seats)],
            handlers.FLIGHT_CALENDAR: [CallbackQueryHandler(handlers.flight_calendar)],
            handlers.NUMBER_OF_SEATS_CALENDAR: [CallbackQueryHandler(handlers.number_of_seats_calendar)],
            handlers.COMMENT: [
                MessageHandler(Filters.regex('Пропустить|пропустить') & ~Filters.command, handlers.exit_comment),
                MessageHandler(Filters.text & ~Filters.command, handlers.comment)
            ],
            handlers.DATA_VALIDATION: [
                MessageHandler(Filters.regex("да|нет") & ~Filters.command, handlers.data_validation)
            ],
            handlers.NAME: [MessageHandler(Filters.regex(re_name) & ~Filters.command, handlers.name)],
            handlers.GENDER: [
                MessageHandler(Filters.regex('мужской|женский') & ~Filters.command, handlers.gender_person)
            ],
            handlers.PHONE_NUMBER: [
                MessageHandler(Filters.regex(re_phone) & ~Filters.command, handlers.phone_number),
                MessageHandler(Filters.text & ~Filters.command, handlers.not_correct_phone_number)
            ],
            handlers.CHECK_PHONE_NUMBER: [
                MessageHandler(Filters.regex("да|нет") & ~Filters.command, handlers.check_phone_number)
            ],
        },
        fallbacks=[MessageHandler(filters, handlers.other_message),
                   CommandHandler('cancel', handlers.cancel),
                   CommandHandler('start', handlers.start),
                   CommandHandler('ticket', handlers.start)],
        name="ticketbot",
        persistent=True
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(filters, handlers.other_message))
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    configure_logger()
    main()
