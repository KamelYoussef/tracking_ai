from utils import *
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def load_and_validate_config(config_path):
    """
    Load and validate the configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Loaded configuration dictionary.

    Raises:
        RuntimeError: If the configuration is invalid or cannot be loaded.
    """
    try:
        config = load_config(config_path)
        required_keys = ['locations', 'search_phrases', 'products']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}")
        return config
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {str(e)}")


def process_product_location(product, location, search_phrases):
    """
    Generate a prompt, get AI response, and find matches in the response.

    Args:
        product (str): Product name.
        location (str): Location name.
        search_phrases (list): List of search phrases.

    Returns:
        dict: Dictionary containing product, location, match details, and AI response.
    """
    try:
        prompt = f"give me the best {product} insurance companies in {location}"
        ai_response = chatgpt(prompt).content
        matches = find_words_in_texts(ai_response, search_phrases, product, location)
        return {
            "product": product,
            "location": location,
            "ai_response": ai_response,
            **matches
        }
    except Exception as e:
        return {
            "product": product,
            "location": location,
            "ai_response": "",
            "error": str(e)
        }


def main():
    config_path = "param.yml"
    config = load_and_validate_config(config_path)

    results = []
    ai_responses = []  # List to collect all AI responses

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_product_location, product, location, config["search_phrases"]
            )
            for product in config["products"]
            for location in config["locations"]
        ]

        # Collect results and AI responses as tasks complete
        for future in futures:
            result = future.result()
            # Exclude ai_response from DataFrame
            result_data = {key: value for key, value in result.items() if key != 'ai_response'}
            results.append(result_data)  # Append without AI response
            if result.get("ai_response"):
                ai_responses.append(
                    f"Product: {result['product']}, Location: {result['location']}\n{result['ai_response']}\n"
                )

    # Save AI responses to a text file
    with open("ai_responses.txt", "w") as f:
        f.writelines(ai_responses)

    # Convert results to a DataFrame for better readability and storage
    df = pd.DataFrame(results)
    print(df)
    df.to_csv("results.csv", index=False)


if __name__ == "__main__":
    main()
