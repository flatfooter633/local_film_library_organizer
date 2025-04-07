from json import load
from os.path import join, isfile
from os import getcwd, makedirs

# Путь к конфигурационному файлу
file_path = join(getcwd(), "utils", "logging_config.json")

# Загрузка конфигурации из JSON-файла
with open(file_path, "r", encoding="utf8") as config_file:
    user_config = load(config_file)

# Путь к лог-файлу
log_file_path = join(getcwd(), "log", "data.log")

# Проверка существования лог-файла
if not isfile(log_file_path):
    # Если лог-файл не существует, создание папки и файла
    makedirs(join(getcwd(), "log"))
    with open(log_file_path, "w", encoding="utf8") as log_file:
        log_file.write("")


# Логирование сообщений
# logger.debug('Это сообщение отладки')
# logger.info('Это информационное сообщение')
# logger.warning('Это предупреждение')
# logger.error('Это сообщение об ошибке')
# logger.critical('Это критическое сообщение')
