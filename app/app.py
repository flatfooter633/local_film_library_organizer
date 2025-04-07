from api.kinopoisk import selection_of_movies
from os import listdir, path, rename, makedirs
from logging import getLogger
from config import TAGS, filter_symbols, return_film_info
import asyncio
import httplib2

logger = getLogger("app")


async def download_film_info(session, query, files_list):
    movies_cards = list()
    for file_name in files_list:
        if file_name.endswith((".mp4", ".avi", ".mkv", ".ts")):
            # Запрос на получение информации о фильмах по базовому запросу
            movie_card = await asyncio.create_task(
                selection_of_movies(session, query_dict=query, query_name=file_name)
            )
            if isinstance(movie_card, list):
                movies_cards.append((file_name, movie_card[0]))
            else:
                logger.info(f"Фильм '{file_name}' не найден.")
    return movies_cards


async def rename_files(
        session,
        folder_path: str,
        query: dict,
        create_folder: str
):
    # Get a list of all files in the folder
    files_list = listdir(folder_path)
    movies_cards = await download_film_info(session, query, files_list)

    if isinstance(movies_cards, list):
        for file_name, movie_card in movies_cards:
            middle_name = '.'.join([keyword for keyword in TAGS if keyword in file_name])
            suffix = "mkv" if file_name.endswith(".mkv") else "avi" if file_name.endswith(".avi") else "mp4"
            suffix_name = "ts" if file_name.endswith(".ts") else suffix
            if isinstance(movie_card, dict):
                try:
                    # Определение основного названия фильма
                    movie_name = movie_card.get("alternativeName")
                    if len(movie_name) < 1:
                        movie_name = movie_card.get("name")

                    # Окончательная инфа для названия
                    movie_name = filter_symbols(movie_name)
                    movie_year = movie_card.get("year")
                    movie_genre = movie_card.get("genres")[0].get("name")
                    movie_poster = movie_card.get("poster").get("url")
                except IndexError:
                    logger.warning("Не удалось получить информацию о фильме")
                    continue
                # Формируем имя фильма
                new_file_name = f"{movie_name}.{movie_year}.{middle_name}.{suffix_name}"

                try:
                    if create_folder == "1":
                        # Создание папки для жанра
                        dir_name = path.join(folder_path, movie_genre)
                        if not path.isdir(dir_name):
                            makedirs(path.join(folder_path, movie_genre))
                            logger.info(f"Создаем каталог жанра: {movie_genre}")
                    else:
                        dir_name = folder_path
                    # Создание папки для фильма
                    file_dir = path.join(dir_name, f"{movie_name} - {movie_year}")
                    if not path.isdir(file_dir):
                        makedirs(file_dir)
                        logger.info(f"Создаем каталог: {movie_name} - {movie_year}")
                except OSError as e:
                    logger.error(f"Ошибка создания каталогов: {e}")
                    continue

                # Переименование файла
                try:
                    rename(path.join(folder_path, file_name), path.join(file_dir, new_file_name))
                except FileExistsError:
                    logger.warning(f"Файл с таким именем уже существует: {new_file_name}")
                else:
                    # Сохранение изображения фильма в JPEG-формате
                    image_path = path.join(file_dir, 'cover.jpg')
                    try:
                        h = httplib2.Http('.cache')
                        response, content = h.request(movie_poster)
                    except AttributeError:
                        logger.error(f"Ошибка загрузки изображения постера для фильма: {new_file_name}")
                    else:
                        with open(image_path, 'wb') as img:
                            img.write(content)
                            logger.info(f"Постер сохранен по адресу: {image_path}")

                    # Сохранение текстового описания фильма в HTML-файле
                    text_file_name = f"{movie_name}.{movie_year}.{middle_name}.html"
                    text_file_path = path.join(file_dir, text_file_name)
                    with open(text_file_path, "w", encoding="utf8") as text_file:
                        text_file.write(return_film_info(movie_card))
                        logger.info(f"Описание фильма сохранено по адресу: {text_file_path}")

                    logger.info(f"Фильм [{file_name}] переименован в [{new_file_name}]")
            else:
                logger.info(f"Фильм '{file_name}' не найден.")

