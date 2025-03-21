import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_sharing_url(url: str) -> dict:
    """
    Отправляет POST-запрос к Яндекс.Сервису для получения ссылки на статью

    :param url: URL исходной статьи
    :return: Ответ сервера в формате JSON
    :raises: HTTPError при статус-коде не 200
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Authorization": f"OAuth {os.getenv('TOKEN_YA')}"
    }

    payload = {"article_url": url}

    result = requests.post(
        "https://300.ya.ru/api/sharing-url",
        headers=headers,
        json=payload
    )

    result.raise_for_status()
    return result.json()


def parse_document(url: str) -> tuple[str, str]:
    """
    Отправляет GET-запрос к Яндекс.Сервису для получения сгенерированного текста

    :param url: sharing_url статьи
    :return: title и article text в виде строк
    """
    result = requests.get(url)
    result.encoding = result.apparent_encoding
    soup = BeautifulSoup(result.text, "lxml")
    title = soup.find("h1", class_="title").text
    short_story = " " + soup.find("meta", attrs={"name": "description"})["content"]
    return title, short_story


def do(url: str) -> tuple[str, str]:
    result: dict = get_sharing_url(url)
    return parse_document(result["sharing_url"])


def is_url_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


if __name__ == "__main__":
    response = get_sharing_url("https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F")
    print(response["sharing_url"])
    print(parse_document(response["sharing_url"]))
