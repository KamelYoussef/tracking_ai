from utils import *


config = load_config("param.yml")

cities = config["cities"]
search_phrases = config["search_phrases"]

texts = [chatgpt(f"{config['prompt']} {city}") for city in cities]

save_list_to_txt("responses_chat_gpt.txt", texts)
texts = read_list_from_txt("responses_chat_gpt.txt")

results = find_words_in_texts(texts, search_phrases)

for result in results:
    print(f"Text: {result['text']}")
    print(f"Matches: {', '.join(result['matches']) if result['matches'] else 'No matches found'}")
    print("-" * 50)
