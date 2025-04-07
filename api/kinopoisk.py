from logging import getLogger
import aiohttp
import asyncio

# Получение логгера
logger = getLogger("api_logger")


async def get_movies(session, url, headers, query_params):
    try:
        async with session.get(url, headers=headers, params=query_params) as response:
            if response.status != 200:
                raise Exception(
                    f"Ошибка HTTP-запроса. Запрос не выполнен с кодом состояния {response.status}"
                )
            result = await response.json()
            if result.get("total") > 0:
                logger.info("Информация о фильмах загружена")
                return result.get("docs")
            else:
                raise Exception(
                    "Фильмы, соответствующие указанным параметрам, не найдены."
                )
    except Exception as e:
        logger.error(f"Ошибка получения информации: {e}")
        return None


async def selection_of_movies(
        session, query_dict: dict, add_to_query: dict = None, query_name: str = None, budget: str = None
):
    if query_name is not None:
        query_dict["query_params"]["query"] = query_name
    elif add_to_query is not None:
        query_dict["query_params"]["limit"] = add_to_query.get("limit")
        query_dict["query_params"]["countries.name"] = add_to_query.get("countries")
        query_dict["query_params"]["year"] = add_to_query.get("years")
        query_dict["query_params"]["rating.kp"] = add_to_query.get("ratings")
        query_dict["query_params"]["ageRating"] = add_to_query.get("age_ratings")
        query_dict["query_params"]["genres.name"] = add_to_query.get("genre")
    elif budget is not None:
        query_dict["query_params"]["budget.value"] = budget
    url = query_dict.get("url")
    query_params = query_dict.get("query_params")
    headers = query_dict.get("headers")
    logger.info(f"Запрос на получение информации о фильмах: {url}")
    return await get_movies(session, url, headers, query_params)


async def http_session_start(
        query: dict, add_to_query: dict = None, query_name: str = None, budget: str = None
):
    # Создание aiohttp-сессии
    async with aiohttp.ClientSession() as session:
        # Запрос на получение информации о фильмах по базовому запросу
        result = await asyncio.create_task(
            selection_of_movies(session, query, add_to_query, query_name, budget)
        )
    return result
