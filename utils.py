from openai import OpenAI
import re
import yaml
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"))


def chatgpt(question):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return completion.choices[0].message


def find_words_in_texts(texts, search_phrases):
    results = []
    for text in texts:
        matches = []
        for phrase in search_phrases:
            # Check if the phrase exists in the text
            if re.search(rf'\b{re.escape(phrase)}\b', text, re.IGNORECASE):
                matches.append(phrase)
        results.append({"text": text, "matches": matches})
    return results


def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


def save_list_to_txt(filename, data_list):
    """
    Save a list of strings to a text file, each item on a new line.

    Parameters:
        filename (str): Name of the file to save the list to.
        data_list (list): List of strings to save.

    Returns:
        None
    """
    with open(filename, "w") as file:
        for item in data_list:
            file.write(f"{item}\n")


def read_list_from_txt(filename):
    """
    Read the contents of a text file into a list of strings, each line representing an item.

    Parameters:
        filename (str): Name of the file to read from.

    Returns:
        list: List of strings read from the file.
    """
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]
