from utils import *
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def load_and_validate_config(config_path):
    try:
        config = load_config(config_path)
        required_keys = ['locations', 'search_phrases', 'products']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}")
        return config
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {str(e)}")


config = load_and_validate_config("param.yml")

results = []

for product in config["products"]:
    for location in config["locations"]:
        prompt = f"give me the best {product} insurance companies in {location}"
        ai_response = chatgpt(prompt).content
        matches = find_words_in_texts(ai_response, config["search_phrases"], product, location)
        results.append(matches)

print(results)
