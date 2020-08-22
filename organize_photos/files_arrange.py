# -*- coding: utf-8 -*-


# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk генерация имён файлов в дереве каталогов
#   os.path.dirname возвращает имя директории пути path.
#   os.path.join позволяет совместить несколько путей при помощи присвоенного разделителя
#   os.path.normpath
#   os.path.getctime время создания файла (Windows), время последнего изменения файла (Unix).
#   os.path.getmtime время последнего изменения файла, в секундах.
#   time.gmtime преобразует время, выраженное в секундах с начала эпохи в struct_time
#   os.makedirs создание директории с прмежуточными
#   shutil.copy2 (src, dst, follow_symlinks=True) - копирует содержимое файла src в файл или папку dst
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.
import os
import shutil
import time
from abc import ABC, abstractmethod
from pathlib import Path


class SortingByYear(ABC):

    def __init__(self, path_destination_folder):
        self.path_destination_folder = os.path.normpath(path_destination_folder)
        self.folder_year_month = set()

    @abstractmethod
    def sort(self):
        pass


class SortingByYearFolder(SortingByYear):

    def __init__(self, path_destination_folder, path_folder_to_scan):
        super().__init__(path_destination_folder)
        self.path_folder_to_scan = os.path.normpath(path_folder_to_scan)

    def sort(self):
        for dirpath, dirnames, filenames in os.walk(self.path_folder_to_scan):
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                time_file = os.path.getmtime(file_path)
                norm_time_file = time.gmtime(time_file)
                year_file = norm_time_file.tm_year
                month_file = norm_time_file.tm_mon
                new_path = os.path.join(self.path_destination_folder, str(year_file), str(month_file))
                new_path = os.path.normpath(new_path)
                destination = os.path.join(new_path, file)
                if new_path not in self.folder_year_month:
                    os.makedirs(new_path)
                self.folder_year_month.add(f"{new_path}")
                shutil.copy2(file_path, destination, follow_symlinks=True)


path = Path.cwd()/"icons"
target_folder = Path.cwd()/"icons_by_year_folder"
sorting_folder = SortingByYearFolder(target_folder, path)
sorting_folder.sort()


# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится ктолько к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
