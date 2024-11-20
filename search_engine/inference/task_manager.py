import json
from pprint import pprint
from typing import List, Dict, Optional

from ..openai import get_openai_client

next_action_schema = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": ["proceed", "inquire"],
            "description": "The next action to take"
        },
        "reason": {
            "type": "string",
            "description": "Explanation for why this action was chosen"
        }
    },
    "required": ["action", "reason"]
}

system_prompt = """
As a professional web researcher, your primary objective is to fully comprehend the user's query, conduct thorough web searches to gather the necessary information, and provide an appropriate response.
To achieve this, you must first analyze the user's input and determine the optimal course of action. You have two options at your disposal:
1. "proceed": If the provided information is sufficient to address the query effectively, choose this option to proceed with the research and formulate a response.
2. "inquire": If you believe that additional information from the user would enhance your ability to provide a comprehensive response, select this option. You may present a form to the user, offering default selections or free-form input fields, to gather the required details.
Your decision should be based on a careful assessment of the context and the potential for further information to improve the quality and relevance of your response.
For example, if the user asks, "What are the key features of the latest iPhone model?", you may choose to "proceed" as the query is clear and can be answered effectively with web research alone.
However, if the user asks, "What's the best smartphone for my needs?", you may opt to "inquire" and present a form asking about their specific requirements, budget, and preferred features to provide a more tailored recommendation.
Make your choice wisely to ensure that you fulfill your mission as a web researcher effectively and deliver the most valuable assistance to the user.
"""


def task_manager(messages: List[dict], model: str = 'gpt-4-turbo') -> Optional[Dict]:
    client = get_openai_client()
    full_messages = [{"role": "system", "content": system_prompt}]
    full_messages.extend(messages)

    functions = [{
        "name": "determine_action",
        "description": "Determine the next action based on user input",
        "parameters": next_action_schema
    }]
    response = client.chat.completions.create(
        model=model,
        messages=full_messages,
        functions=functions,
        function_call={"name": "determine_action"}
    )

    message = response.choices[0].message
    return {
        'answer': message.content,
        'function_call': json.loads(message.function_call.arguments) if message.function_call else None
    }


if __name__ == '__main__':
    pprint(task_manager(
        messages=[
            {"role": "user", "content": "What are the key features of the latest iPhone model?"},
            # {"role": "user", "content": "What's the best smartphone for me?"},
        ],
    ))
