import os
from pprint import pprint
from typing import List, Optional

import requests

from .base import SearchResults, SearchResultImage, SearchResultItem


def serper_search(
        query: str,
        max_results: int = 10,
        search_depth: str = 'basic',
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None
) -> SearchResults:
    api_key = os.environ.get('SERPER_API_KEY')
    if not api_key:
        raise EnvironmentError('SERPER_API_KEY is not set in the environment variables')

    payload = {
        "q": query,
        "num": max_results,
        "type": "search"
    }
    if search_depth == 'advanced':
        payload.update({
            "timeframe": "year",
        })
    if include_domains:
        payload["site"] = include_domains
    if exclude_domains:
        payload["exclude_sites"] = exclude_domains

    response = requests.post(
        'https://google.serper.dev/search',
        json=payload,
        headers={
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
    )
    response.raise_for_status()
    data = response.json()

    return SearchResults(
        query=query,
        results=[
            SearchResultItem(
                title=item.get('title', ''),
                url=item.get('link', ''),
                content=item.get('snippet', '')
            ) for item in data.get('organic', [])
        ],
        images=[
            SearchResultImage(url=img.get('imageUrl', ''), description=img.get('title', ''))
            for img in data.get('images', [])
        ],
    )


if __name__ == '__main__':
    results = serper_search(
        query="Python programming",
        max_results=5,
        search_depth='advanced'
    )
    print('Results:')
    pprint(results.results)
    print()
    print()

    print('Images:')
    pprint(results.images)
    print()
    print()
