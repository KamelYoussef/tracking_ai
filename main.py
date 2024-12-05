from utils import *
import streamlit as st
import time


# config data
config = load_config("param.yml")

cities = config["cities"]
search_phrases = config["search_phrases"]

#streamlit app
st.title("AI Tracking - Chat gpt")

st.sidebar.header("Summary")
summary_data = []

if st.button("Start"):
    start_time = time.time()
    with st.spinner('Wait for it...'):
        # Generate responses
        texts = [chatgpt(f"{config['prompt']} {city}").content for city in cities]
        save_list_to_txt("responses_chat_gpt.txt", texts)

        # Find matches
        results = find_words_in_texts(texts, search_phrases)

        # Display results and build summary
        for city, result in zip(cities, results):
            st.write(f"Response for : {city}:/n {result['text']}")
            matches = ', '.join(result['matches']) if result['matches'] else "No matches found"
            st.write(f"Matches: {matches}")
            st.write("-" * 50)

            # Append summary data
            summary_data.append({"City": city, "Matches Found": matches})

        # Add summary to sidebar
        if summary_data:
            st.sidebar.table(summary_data)

    elapsed_time = time.time() - start_time

    st.success(f"Process completed in {elapsed_time:.2f} seconds.")
    st.sidebar.metric("Elapsed Time (s)", f"{elapsed_time:.2f}")



