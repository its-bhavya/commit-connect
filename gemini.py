import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
import json
import re

load_dotenv(find_dotenv())
genai_api_key = os.getenv("gemini_api")
genai.configure(api_key=genai_api_key)

def parse_user_prompt(text):
    """
    Parses user input using Gemini to extract languages, difficulty, and other filters.
    Returns a dictionary or error message.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        prompt = f"""
You are an AI assistant for an open source contribution website that extracts structured filters from user prompts. The output you return will used to filter what projects we recommend the user. The user prompt might also include what they **do not** want in their contribution projects. 

Given this prompt:
"{text}"

Return ONLY a JSON object with the fields:
- "languages": [list of programming languages used],
- "frameworks and libraries": [list of programming frameworks or libraries used],
- "tools": [list of tools used]
- "difficulty": "Beginner" | "Intermediate" | "Advanced" | None,
- "other_filters": [list of useful tags or keywords]
- "exclude":[list of languages, frameworks, libraries, tools, other things to NOT use]

No markdown or explanation. Only the JSON.
"""

        response = model.generate_content(prompt)
        result = response.text.strip()

        # Extract the JSON block from the response using regex
        match = re.search(r"\{[\s\S]*\}", result)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            return {
                "error": "No JSON object found in the response.",
                "raw_response": result
            }

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": locals().get("result", "No result")
        }
