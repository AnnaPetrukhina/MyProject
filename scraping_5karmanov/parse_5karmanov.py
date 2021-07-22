import bs4
from requests_html import HTMLSession
import requests
import re
import csv
import sys


class Parse5Karmanov:

    def __init__(self, url):
        self.url = url
        self.contacts = []
        self.fieldnames = ['city', 'mall_name', 'outlet_id', 'outlet_name',
                           'phone_formatted', 'full_address']
        self.gender = {'Мужская': 'мужской', 'Женская': 'женский'}
        self.shop_information = dict()
        self.information = dict()

    @staticmethod
    def get_html(url):
        html_text = requests.get(url).text
        return bs4.BeautifulSoup(html_text, 'html.parser')

    @staticmethod
    def get_html_js(url):
        session = HTMLSession()
        response = session.get(url)
        response.html.render(timeout=0)
        return response

    def get_out_csv(self):
        writer = csv.DictWriter(sys.stdout, delimiter=',', fieldnames=self.fieldnames)
        writer.writeheader()
        for shop in self.contacts:
            writer.writerow(shop)

    def get_out_txt(self):
        stdout_fileno = sys.stdout
        stdout_fileno.write(str(self.information))
        stdout_fileno.write('\n')

    @staticmethod
    def replace_phone_symbol(phone_string):
        replace_information = {' ': '', '+8': '7', '+': '', '(': '', ')': '', '-': ''}
        for k, v in replace_information.items():
            phone_string = phone_string.replace(k, v)
        return phone_string

    def get_stores(self, list_of_stores):
        list_of_address = list_of_stores.find_all('div', class_="item")
        for store in list_of_address:
            data = []
            address = store.find_next('a', class_="darken").string.strip()
            address_list = address.split(',')
            data.append(address_list[0].strip())
            mall = address_list[1].strip()
            mall.strip('"')
            data.append(mall)
            pattern_postal_code = r'\d{6}'
            outlet_id_data = re.search(pattern_postal_code, address)
            phone = store.find_next('div', class_="phone").find_next('a').string
            phone_string = self.replace_phone_symbol(phone)
            if outlet_id_data:
                outlet_id = outlet_id_data[0] + phone_string
            else:
                outlet_id = phone_string
            data.append(outlet_id)
            self.shop_information.update([(phone_string, outlet_id)])
            data.append('5КармаNов')
            data.append(phone)
            full_address = ''
            for el in address_list[2:]:
                if el != ' ':
                    full_address += el.strip() + " "
            data.append(full_address)
            self.contacts.append(dict(zip(self.fieldnames, data)))

    def get_contacts(self):
        soup = self.get_html(self.url)
        contacts = soup.find('div', class_="location-link-container").find_next("a").get('href')
        soup_contacts = self.get_html(self.url + contacts)
        list_of_stores = soup_contacts.find('div', class_="contacts-stores")
        self.get_stores(list_of_stores)
        self.get_out_csv()

    @staticmethod
    def get_link_catalog(catalog):
        data_link = catalog.find_all('li', class_='')
        links = []
        for link in data_link:
            links.append(startURL + link.find_next('a').get('href'))
        return links

    def get_name_vendor(self, response):
        categories_data = response.html.find('.breadcrumbs__item-name')
        categories = [i.text for i in categories_data[2:]]
        index_categories = categories[0].find(' ')
        gender_categories = self.gender[categories[0][:index_categories]]
        data_name = response.html.find('.preview-text', first=True).text
        data_list = data_name.split('\n')
        name = ''
        vendor_code = ''
        if len(data_list) == 2:
            name = categories[-2] + ' ' + categories[-1]
            vendor_code = data_list[0]
        elif len(data_list) == 3:
            name = data_list[0]
            vendor_code = data_list[1]

        vendor_data = response.html.find('.brand__link', first=True)
        if vendor_data is None:
            vendor = categories[-1]
        else:
            vendor = vendor_data.text
        return categories, name, vendor, vendor_code, gender_categories

    @staticmethod
    def get_price(response):
        price_data = response.html.find('.price')
        prices = set()
        for price in price_data:
            price = price.text
            if price != '':
                index = price.rfind(' ')
                price_str = price[:index].replace(' ', '')
                prices.add(int(price_str))
        prices = list(prices)
        price = prices[0]
        old_price = 'None'
        if len(prices) != 1:
            if prices[0] > prices[1]:
                old_price, price = prices[0], prices[1]
            else:
                old_price, price = prices[1], prices[0]
        return price, old_price

    @staticmethod
    def get_properties(response):
        properties_name_data = response.html.find('.properties__title')
        properties_name = [name.text.strip() for name in properties_name_data]
        properties_value_data = response.html.find('.properties__value')
        properties_value = [name.text.strip() for name in properties_value_data]
        properties = dict(zip(properties_name, properties_value))
        country_of_origin = properties['Страна производства']
        material = properties['Состав']
        seasonality = properties['Сезонность']
        size_data = response.html.find('.cnt')
        sizes = [size.text.strip() for size in size_data[1:]]
        model_data = properties['Артикул производителя / Штрихкод']
        index = model_data.find(' /')
        model = model_data[:index].strip()
        id_group = model_data[index + 2:].strip()
        return country_of_origin, material, seasonality, sizes, model, id_group

    def get_pictures(self, response):
        pictures_html = response.html.find('.owl-stage-outer', first=True).html
        pictures_soup = bs4.BeautifulSoup(pictures_html, 'html.parser')
        pictures_data = pictures_soup.find_all('img')
        return [self.url + picture.get('src') for picture in pictures_data]

    def get_presence_shop(self, response):
        presence_html = response.html.find('.js-store-scroll', first=True).html
        presence_soup = bs4.BeautifulSoup(presence_html, 'html.parser')
        outlets = []
        presence_data = presence_soup.find_all('div', class_='store_phone')
        for phone_shop in presence_data:
            index_phone = phone_shop.string.find(':')
            phone_string = phone_shop.string[index_phone + 1:].strip()
            replace_information = {' ': '', '+8': '7', '+': '', '(': '', ')': '', '-': ''}
            for k, v in replace_information.items():
                phone_string = phone_string.replace(k, v)
            try:
                outlets.append(self.shop_information[phone_string])  # телефон иногда отличается
            except KeyError:
                continue
        return outlets

    @staticmethod
    def get_id(response):
        id_html = response.html.find('.product-info ', first=True).html
        id_soup = bs4.BeautifulSoup(id_html, 'html.parser')
        id_data = id_soup.find_all('span', itemprop="offers")
        id_information = set()
        for i in id_data:
            url_size = i.find('a', itemprop="url").get('href')
            index_url = url_size.find('=') + 1
            id_information.add(url_size[index_url:])
        return list(id_information)

    def product_information(self, link):
        response = self.get_html_js(link)
        index_link = link.rfind('/')
        link = link[:index_link]
        categories, name, vendor, vendor_code, gender_categories = self.get_name_vendor(response)
        description = response.html.find('.content', first=True).text
        price, old_price = self.get_price(response)
        color = response.html.find('.val', first=True).text
        country_of_origin, material, seasonality, sizes, model, id_group = self.get_properties(response)
        pictures = self.get_pictures(response)
        id_list = self.get_id(response)
        outlets = self.get_presence_shop(response)

        for i in range(0, len(sizes)):
            params = dict(Материал=material, Возраст="Взрослый", Пол=gender_categories, Сезон=seasonality, цвет=color,
                          размер=sizes[i])
            self.information = {
                "shop_info": {"url": "https://5karmanov.ru", "company": "5karmanov",
                              "currencies": [["RUR", "1"]], "name": "5karmanov"},
                "offer": {
                    "available": "true",
                    "picture": pictures,
                    "vendorCode": vendor_code, "vendor": vendor, "name": name,
                    "url": link, "price": price, "old_price": old_price,
                    "outlets": outlets,
                    "param": params, "currencyId": "RUR", "model": model,
                    "group_id": id_group, "id": id_list[i],
                    "categories": categories, 'description': description
                }
            }
            self.get_out_txt()

    def get_items(self, product):
        for link_items in product:
            link_product = link_items.find_next('a').get('href')
            self.product_information(self.url + link_product)

    def get_advertisement(self, link):
        soup_section = self.get_html(link + '/?SHOWALL=&SHOWALL_1=1')
        try:
            items = soup_section.find('div', class_='top_wrapper')
            product = items.find_all('div', class_='item-title')
            self.get_items(product)
        except Exception as exp:
            soup_section = self.get_html(link)
            pages = soup_section.find('div', class_='module-pagination')
            count_page = pages.find_next('span', class_='point_sep').find_next('a', class_='dark_link').contents[0]
            for page in range(1, int(count_page) + 1):
                soup_section = self.get_html(link + f'?PAGEN_1={page}')
                items = soup_section.find('div', class_='top_wrapper')
                product = items.find_all('div', class_='item-title')
                self.get_items(product)

    def get_catalog(self):
        soup = self.get_html(self.url)
        catalog = soup.find_all('ul', class_="menu-wrapper")
        # female = catalog[1] male = catalog[2]
        female_link = self.get_link_catalog(catalog[1])
        male_link = self.get_link_catalog(catalog[2])
        for link in female_link:
            self.get_advertisement(link)
        for link in male_link:
            self.get_advertisement(link)


if __name__ == '__main__':
    startURL = 'https://5karmanov.ru'
    parse_5karmanov = Parse5Karmanov(startURL)
    parse_5karmanov.get_contacts()
    parse_5karmanov.get_catalog()
