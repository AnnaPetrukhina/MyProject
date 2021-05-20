from pony import orm
from settings import DB_CONFIG

# psql -U postgres -c "create database tb_chat_bot"
# psql --help
# \! chcp 1251 для преобразование кириллицы
# DROP TABLE table_name;

db = orm.Database()
db.bind(**DB_CONFIG)


class Registration(db.Entity):
    """Данные билета"""
    name = orm.Required(str)
    date_of_departure = orm.Required(str)
    city_of_departure = orm.Required(str)
    arrival_city = orm.Required(str)
    flight = orm.Required(str)
    number_of_seats = orm.Required(str)
    comment = orm.Required(str)
    phone_number = orm.Required(str)
    name_avatar = orm.Required(str)


db.generate_mapping(create_tables=True)
