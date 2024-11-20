import json
from datetime import datetime
from pprint import pprint
from typing import List, Dict, Any

from ..openai import get_openai_client
from ..retrieve import fetch_jina_reader_data
from ..search import serper_search

# 设置系统提示
SYSTEM_PROMPT = """
As a professional search expert, you possess the ability to search for any information on the web.
For each user query, utilize the search results to their fullest potential to provide additional information and assistance in your response.
If there are any images relevant to your answer, be sure to include them as well.
Aim to directly address the user's question, augmenting your response with insights gleaned from the search results.
"""

_TOOLS_SCHEMA = [
    {
        "name": "serper_search",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "max_results": {"type": "integer", "description": "Maximum number of results to return"},
                "search_depth": {"type": "string", "enum": ["basic", "advanced"], "description": "Depth of search"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "fetch_jina_reader_data",
        "description": "Fetch data from a URL using Jina Reader",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch data from"}
            },
            "required": ["url"]
        }
    },
]

TOOLS = {
    'serper_search': serper_search,
    'fetch_jina_reader_data': fetch_jina_reader_data,
}


def researcher(messages: List[dict], model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    full_response = ''
    tool_results = []

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_prompt = f"{SYSTEM_PROMPT} Current date and time: {current_date}"

    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        functions=_TOOLS_SCHEMA,
        # max_steps=5,
    )

    for choice in response.choices:
        if choice.message.function_call:
            function_call = choice.message.function_call
            parameters = json.loads(function_call.arguments)
            tool_response = TOOLS[function_call.name](**parameters)
            tool_results.append(tool_response)

        if 'content' in choice.message:
            full_response += choice.message['content']

    return {"text": full_response, "tool_results": tool_results}


# Example usage
if __name__ == '__main__':
    pprint(researcher([
        {"role": "user", "content": "Tell me about Python programming."}
    ]))
