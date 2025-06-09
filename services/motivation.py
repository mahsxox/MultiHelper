import random
import json
import os

def get_random_quote() -> tuple[str, str]:
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'quotes.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        quotes = json.load(f)
    q = random.choice(quotes)
    return q['quote'], q['author']