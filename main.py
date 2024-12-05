from utils import *
import streamlit as st
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np

# Load and validate configuration with error handling
def load_and_validate_config(config_path):
    try:
        config = load_config(config_path)
        required_keys = ['cities', 'search_phrases', 'prompt']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            st.error(f"Missing configuration keys: {', '.join(missing_keys)}")
            st.stop()
        return config
    except Exception as e:
        st.error(f"Error loading configuration: {str(e)}")
        st.stop()

# Function to generate responses in parallel using ThreadPoolExecutor
def generate_responses(cities, prompt):
    with ThreadPoolExecutor() as executor:
        try:
            results = list(executor.map(lambda city: chatgpt(f"{prompt} {city}").content, cities))
            return results
        except Exception as e:
            st.error(f"Error generating responses: {str(e)}")
            return []

# Function to process responses and find matches
def process_responses(texts, search_phrases):
    try:
        return find_words_in_texts(texts, search_phrases)
    except Exception as e:
        st.error(f"Error processing responses: {str(e)}")
        return []

# Function to display results and build summary in a more readable way
def display_results(cities, results):
    summary = []
    for city, result in zip(cities, results):
        st.subheader(f"Response for {city}:")
        st.write(result['text'])

        # Display matches or a message if none found
        matches = ', '.join(result['matches']) if result['matches'] else "No matches found"
        st.write(f"Matches: {matches}")
        st.write("-" * 50)

        summary.append({"City": city, "Matches Found": matches})
    return summary

# Load and validate configuration
config = load_and_validate_config("param.yml")

# Streamlit app UI
st.title("Tracking Report")


report = None
# Sidebar
st.sidebar.header("AI Tracking")
with st.sidebar:
    ai_tool = st.radio(
        "Choose AI Tool",
        ["CHAT_GPT", "PERPLEXITY", "GEMINI"],
        index=None,
    )

    types = st.radio(
        "Choose Insurance Product",
        ["HOME", "HEALTH", "CARS"],
        index=None,
    )

    if st.button("Generate Report"):
        report = pd.DataFrame(
            np.random.randn(10, 5), columns=("col %d" % i for i in range(5))
        )

st.table(report)
