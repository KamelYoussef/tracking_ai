import streamlit as st
import time
import pandas as pd

# Streamlit display
st.title("AI Search Tracker")

# Load the DataFrame from the CSV file
try:
    df = pd.read_csv("results.csv")
    st.write("Here are the results :")
    st.dataframe(df)  # Display the DataFrame
except FileNotFoundError:
    st.error("The results were not found.")
except Exception as e:
    st.error(f"Error loading: {str(e)}")
