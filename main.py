from logging import config, getLogger
from utils.logger import user_config
import aiohttp
import asyncio
from os import path, getcwd, name as os_name
from config import SEARCH_BY_NAME_QUERY
from app.app import rename_files





async def main():
    # Ваш код здесь
    logger.info("Событие 'main' обработано")
    main_path = getcwd()
    # Ввод пути к папке с фильмами
    while True:
        try:
            main_path = path.normpath(input("Введите путь к папке с фильмами: "))
        except OSError:
            logger.warning(f"Ошибка при получении пути к папке")
            await asyncio.sleep(1)
            continue
        else:
            break
    create_folder = input("Сортировать по жанрам? [1] или [0]: ").strip()
    # Создание aiohttp-сессии
    async with aiohttp.ClientSession() as session:
        await rename_files(session, main_path, SEARCH_BY_NAME_QUERY, create_folder)


if __name__ == "__main__":
    # Настройка логирования с использованием конфигурации
    config.dictConfig(user_config)
    # Получение root логгера
    logger = getLogger()
    try:
        # Установка политики событийного цикла для Windows, если используется операционная система Windows
        if os_name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        logger.info("...Приложение запущено")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановка приложения...")
