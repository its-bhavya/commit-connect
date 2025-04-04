import google.generativeai as genai  # Gemini API
import streamlit as st
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("gemini_api")

# Set up Gemini
genai.configure(api_key=gemini_api_key)

