from typing import List

from ..openai import get_openai_client

SYSTEM_PROMPT = """
As a professional web researcher, your task is to generate a set of three queries that explore the subject matter more deeply, building upon the initial query and the information uncovered in its search results.

For instance, if the original query was "Starship's third test flight key milestones", your output should follow this format:

Aim to create queries that progressively delve into more specific aspects, implications, or adjacent topics related to the initial query. The goal is to anticipate the user's potential information needs and guide them towards a more comprehensive understanding of the subject matter.
 
Please match the language of the response to the user's language.
"""


def query_suggestor_with_text(messages: List[dict], model: str = 'gpt-3.5-turbo'):
    last_messages = [{
        **message,
        'role': 'user'
    } for message in messages[-1:]]

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + last_messages
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=api_messages
    )
    return response.choices[0].message.content.strip()


if __name__ == '__main__':
    related_queries = query_suggestor_with_text([
        {'role': 'user', 'content': 'su-57\'s performance'}
    ])
    print(related_queries)
