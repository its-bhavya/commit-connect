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
You must infer the user's intent even if they don't explicitly say the filter.

Given a prompt like:
"I want React projects that don't use complex state management"

You should include:
"other_filters": ["simple state", "no Redux"]

---

Examples:

Prompt: "Looking for beginner-friendly Django bugs"
→
{{
  "languages": ["Python", "Django"],
  "difficulty": "Beginner",
  "other_filters": ["bug"]
}}

Prompt: "I want React projects that don't use Redux"
→
{{
  "languages": ["React"],
  "difficulty": "Intermediate",
  "other_filters": ["no Redux", "simple state"]
}}

Given this prompt:
"{text}"

Return ONLY a JSON object with the fields:
- "languages": [list of programming languages used],
- "frameworks and libraries": [list of programming frameworks or libraries used],
- "tools": [list of tools used]
- "difficulty": "Beginner" | "Intermediate" | "Advanced" | None,
- "other_filters": [list of useful tags or keywords]

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


def get_filters(text:str):
    """
    Once the prompt has been parsed, this function extracts and returns all the fields and filters.
    """
    parsed_prompt = parse_user_prompt(text=text)

    languages = parsed_prompt['languages']
    frameworks_libraries = parsed_prompt["frameworks and libraries"]
    tools = parsed_prompt['tools']
    difficulty = parsed_prompt['difficulty']
    filters = parsed_prompt['other_filters']
    
    
    #print(f"Languages:\n{languages}")
    #print(f"Frameworks:\n{frameworks_libraries}")
    #print(f"Tools:\n{tools}")
    #print(f"Filters:\n{filters}")

    return languages, frameworks_libraries, tools, difficulty, filters