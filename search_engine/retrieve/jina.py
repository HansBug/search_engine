import os
from pprint import pprint

import requests

CONTENT_CHARACTER_LIMIT = 10000


def fetch_jina_reader_data(url: str):
    headers = {
        "Accept": "application/json",
        "X-With-Generated-Alt": "true"
    }
    if os.environ.get('JINA_API_KEY'):
        headers['Authorization'] = f'Bearer {os.environ["JINA_API_KEY"]}'
    response = requests.get(
        f"https://r.jina.ai/{url}",
        headers=headers
    )
    json_data = response.json()
    if not json_data.get("data") or len(json_data["data"]) == 0:
        return None
    content = json_data["data"]["content"][:CONTENT_CHARACTER_LIMIT]
    return {
        "title": json_data["data"]["title"],
        "content": content,
        "url": json_data["data"]["url"]
    }


if __name__ == '__main__':
    pprint(fetch_jina_reader_data('https://www.python.org/about/gettingstarted/'))
