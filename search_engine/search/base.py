from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SearchResultImage:
    url: str
    description: Optional[str] = None


@dataclass
class SearchResultItem:
    title: str
    url: str
    content: str


@dataclass
class SearchResults:
    query: str
    results: List[SearchResultItem]
    images: List[SearchResultImage]

    @property
    def number_of_results(self) -> int:
        return len(self.results)
