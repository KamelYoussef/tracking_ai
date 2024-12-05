from utils import *
import streamlit as st
import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

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
st.title("AI Tracking - Chat GPT")

# Sidebar summary
st.sidebar.header("Summary")
summary_data = []

# Start button for processing
if st.button("Start"):
    start_time = time.time()
    with st.spinner('Processing... This might take some time.'):

        # Generate responses (no caching or progress bar)
        texts = generate_responses(config['cities'], config['prompt'])
        save_list_to_txt("responses_chat_gpt.txt", texts)

        # Find matches
        results = process_responses(texts, config["search_phrases"])

        # Display results and build summary
        summary_data = display_results(config["cities"], results)

        # Add summary to sidebar
        if summary_data:
            df = pd.DataFrame(summary_data)
            st.sidebar.dataframe(df, use_container_width=True)

    elapsed_time = time.time() - start_time

    st.success(f"Process completed in {elapsed_time:.2f} seconds.")
    st.sidebar.metric("Elapsed Time (s)", f"{elapsed_time:.2f}")

    # Provide downloadable file of the responses
    st.sidebar.download_button("Download Responses", data="\n".join(texts), file_name="responses_chat_gpt.txt")
