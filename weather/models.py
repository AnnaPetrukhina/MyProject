import peewee
from pathlib import Path

path_database = Path.cwd() / "weather.db"
database = peewee.SqliteDatabase(f'{path_database}')


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Weather(BaseTable):
    date = peewee.TextField(unique=True)
    average_temperature = peewee.IntegerField()
    low_temperature = peewee.IntegerField()
    high_temperature = peewee.IntegerField()
    wind = peewee.CharField()
    humidity = peewee.CharField()
    weather_description = peewee.CharField()
