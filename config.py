import os
from dotenv import load_dotenv, find_dotenv


# Загрузка переменных окружения из файла.env
# Если файла.env нет, то окружение не загружается и приложение завершается с сообщением об ошибке.
if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

# Токен API кинопоиска
API_KEY = os.getenv("API_KEY")
# Токен бота можно получить через @BotFather в Telegram
TOKEN = os.getenv("TOKEN")


# Массив символов для исключения из поиска
STOP_SYMBOLS = ['&', '|', '*', '?', "'", '"', '`', '[', ']', '(', ')', '$', '<', '>', '{', '}',
                                    '^', '#', '\\', '/', '%', '!', ':']

# Функция для фильтрации символов из имени файла
def filter_symbols(name):
    # Удаление символов из имени файла
    for symbol in STOP_SYMBOLS:
        if symbol in name:
            name = name.replace(symbol, ' -') \
                if symbol == ':' \
                else name.replace(symbol, '')
    return name


TAGS = {
    'UHD': False,
    'BluRay': False,
    'Blu-Ray': False,
    'DVDRip-AVC': False,
    'HDDVD': False,
    'HDTV': False,
    'BDRip': False,
    'Remux': False,
    'WEB-DL': False,
    'IMAX': False,
    '720p': False,
    '1080p': False,
    '2160p': False,
    '1920x1080': False,
    '3840x2160': False,
    'Criterion.Collection': False,
    'Criterion Collection': False,
    'Theatrical.Cut': False,
    'Theatrical Cut': False,
    'Directors.Cut': False,
    'Directors Cut': False,
    'AI Upscale': False,
    'Remastered': False,
    'Open Matte': False,
    'DTS': False,
    'SDR': False,
    'HDR': False,
    'DV': False,
    'x264': False,
    'h264': False,
    'Rus': False,
    'Eng': False,
    '20th.Anniversary': False,
    '4K': False,
    'DDP5.1': False,
    'Extended Cut': False,
    'Extended.Cut': False,
    'DTS-HD': False,
    'Atmos': False,
    'TrueHD': False,
    'DoVi': False,
    'Dolby Vision': False,
    'HYBRID': False,
    'Hybrid': False
}

# Базовый Запрос поиска по названию фильма
SEARCH_BY_NAME_QUERY = {
    "url": "https://api.kinopoisk.dev/v1.4/movie/search",
    "query_params": {
        "page": 1,
        "limit": 1,
    },
    "headers": {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    },
}

# Базовый Запрос поиска по жанру и стране
BASE_SEARCH_QUERY = {
    "url": "https://api.kinopoisk.dev/v1.4/movie",
    "query_params": {
        "page": 1,
        "limit": 15,
        "selectFields": [
            "id",
            "name",
            "alternativeName",
            "budget",
            # "fees",
            "description",
            "rating",
            "year",
            "type",
            # "facts",
            "genres",
            "ageRating",
            "countries",
            "poster",
            # "similarMovies",
            # "sequelsAndPrequels",
            # "persons",
        ],
        "notNullFields": [
            "id",
            "name",
            "alternativeName",
            "description",
            "year",
            "rating.kp",
            "ageRating",
            "budget.value",
            "budget.currency",
            "genres.name",
            "countries.name",
            "poster.url",

        ],
        "type": ["animated-series", "anime", "cartoon", "movie", "tv-series"],
        # "budget.value": "1000 - 9000000",
    },
    "headers": {
        "accept": "application/json",
        "X-API-KEY": API_KEY,
    },
}


# Путь к корневой директории приложения
def root_path():
    return os.path.abspath(os.sep)


def return_film_info(input_card: dict) -> str:
    # Define the root directory and the image file name
    root_dir = '..'
    image_file = 'background.jpg'

    # Construct the full path to the image file
    image_path = '/'.join([root_dir, 'IMG', image_file])
    try:
        budget = input_card.get("budget").get("value")
        currency = input_card.get("budget").get("currency")
    except AttributeError:
        budget_string = ""
    else:
        budget_string = f"<p>Бюджет: <b>{budget:,} {currency}</b></p>"
    text = (
        f'<!DOCTYPE html>\n'
        f'<html>\n'
        f'<head>\n'
        f'<meta charset="utf-8">\n'
        f'<title>{input_card.get("name")}</title>\n'
        f'<style>\n'
        f'body {{\n'
        f'    background-image: url({image_path});\n'
        f'    background-repeat: no-repeat;\n'
        f'    background-position: center center;\n'
        f'    background-attachment: fixed;\n'
        f'    background-size: cover;\n'
        f'    color: white;\n'
        f'    font-family: Arial, sans-serif;\n'
        f'    padding: 20px;\n'
        f'    text-align: center;\n'
        f'}}\n'
        f'div.container {{\n'
        f'    display: flex;\n'
        f'}}\n'
        f'div.left {{\n'
        f'    flex: 1;\n'
        f'    text-align: center;\n'
        f'}}\n'
        f'div.right {{\n'
        f'    flex: 1;\n'
        f'    text-align: left;\n'
        f'}}\n'
        f'h1, h2 {{\n'
        f'    color: yellow;\n'
        f'}}\n'
        f'a {{\n'
        f'    color: lightblue;\n'
        f'    text-decoration: none;\n'
        f'}}\n'
        f'a:hover {{\n'
        f'    color: white;\n'
        f'    text-decoration: underline;\n'
        f'}}\n'
        f'</style>\n'
        f'</head>\n'
        f'<body>\n'
        f'\n'
        f'<div class="container">\n'
        f'    <div class="left">\n'
        f'        <p><img width = "500" src="{input_card.get("poster").get("url")}" alt="Постер фильма"></p>\n'
        f'    </div>\n'
        f'    <div class="right">\n'
        f'        <br>\n'
        f'        <h1>Информация о фильме</h1>\n'
        f'        <br>\n'
        f'        <p>Название:  <b><a href="{input_card.get("poster").get("url")}">{input_card.get("name")}</a></b></p>\n'
        f'        <p>Оригинальное название: <u>{input_card.get("alternativeName")}</u></p>\n'
        f'        <p>Год: <b>{input_card.get("year")}</b></p>\n'
        f'        {budget_string}\n'
        f'        <p>Возрастной рейтинг: <b>{input_card.get("ageRating")}+</b></p>\n'
        f'        <p>Рейтинг Кинопоиска: <b>{round(input_card.get("rating").get("kp"), 1)}</b></p>\n'
        f'        <p>Жанры: <b>{", ".join(genre.get("name") for genre in input_card.get("genres"))}</b></p>\n'
        f'        <p>Страны: <b>{", ".join(country.get("name") for country in input_card.get("countries"))}</b></p>\n'
        f'        <br>\n'
        f'        <h2>Описание</h2>\n'
        f'        <br>\n'
        f'        <p><i>{input_card.get("description")}</i></p>\n'
        f'    </div>\n'
        f'</div>\n'
        f'<br>\n'
        f'</body>\n'
        f'</html>'
    )
    return text

