import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
import json
import re
import requests
import urllib


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
You are an advanced AI assistant designed to support an open-source contribution platform by parsing user-submitted prompts and extracting structured filters to refine project recommendations. Users may describe what they are looking for in a project—including preferred or excluded technologies, tools, and project difficulty levels—either explicitly or implicitly. Your role is to accurately infer and extract relevant information, even when it's not directly stated.

You must identify and categorize the following from the user's prompt:

-**Programming languages**
-**Frameworks and libraries (Like React, Flask, Streamlit, Next.js, Node, Django, etc)**
-**Tools**
-**Project difficulty level (Beginner, Intermediate, Advanced, or None)**
-**Other relevant tags, keywords, or filters (e.g., domains like "machine learning", "climate", or "frontend", or preferences like "no corporate repos")**
---

Examples:

Prompt: "Looking for beginner-friendly Django bugs"
→
{{
  "languages": ["Python"],
  "frameworks":["Django"]
  "difficulty": "Beginner",
  "other_filters": ["bug"]
}}

Prompt: "I want React projects that don't use Redux"
→
{{
  "languages": [],
  "frameworks":["React"]
  "difficulty": "Intermediate",
  "other_filters": ["no Redux", "simple state"]
}}

Prompt: "I'm good with JavaScript and want to contribute to React or Vue projects that use TypeScript. I'd prefer if they avoid Redux or complicated state management. Something that involves UI improvements or animations would be cool. Please nothing with GraphQL."
→
{{
  "languages": ["JavaScript", "TypeScript"],
  "frameworks": ["React", "Vue"],
  "difficulty": "Intermediate",
  "other_filters": ["UI", "animations", "no Redux", "no complex state", "no GraphQL"]
}}

Prompt: "Looking for beginner-friendly Python repos, preferably Flask or Django, but I’m more into fixing bugs or writing tests than building new features. Don't want anything with machine learning — just basic backend stuff, maybe API routes or authentication flows."
→
{{
  "languages": ["Python"],
  "frameworks": ["Flask", "Django"],
  "difficulty": "Beginner",
  "other_filters": ["bug", "testing", "backend", "API", "authentication", "no machine learning"]
}}

Prompt: "I want to work on projects related to data visualization using D3.js or Plotly. I'm intermediate in JavaScript and okay with some Python. Would be nice if the issues involve improving dashboards or interactive charts. Not interested in setting up servers or CI/CD pipelines."
→
{{
  "languages": ["JavaScript", "Python"],
  "frameworks": ["D3.js", "Plotly"],
  "difficulty": "Intermediate",
  "other_filters": ["data visualization", "dashboards", "interactive charts", "no servers", "no CI/CD"]
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

    languages = parsed_prompt.get("languages",None)
    frameworks_libraries = parsed_prompt.get("frameworks and libraries",None)
    tools = parsed_prompt.get("tools",None)
    difficulty = parsed_prompt.get("difficulty", None)
    filters = parsed_prompt.get("other_filters", None)
    
    
    #print(f"Languages:\n{languages}")
    #print(f"Frameworks:\n{frameworks_libraries}")
    #print(f"Tools:\n{tools}")
    #print(f"Filters:\n{filters}")

    return languages, frameworks_libraries, tools, difficulty, filters

def build_issue_query(languages, frameworks, tools, difficulty, filters):
    query_parts = []

    # Add languages
    for lang in languages:
        query_parts.append(f"language:{lang}")

    # Clean and join frameworks, tools, filters
    all_labels = []

    if frameworks:
        clean_frameworks = [fw.replace(" ", "-") for fw in frameworks]
        for framework in clean_frameworks:
            all_labels.append(framework)

    if tools:
        clean_tools = [tool.replace(" ", "-") for tool in tools]
        for tool in clean_tools:
            all_labels.append(tool)

    if filters:
        clean_filters = [filt.replace(" ", "-") for filt in filters]
        for filter in clean_filters:
            all_labels.append(filter)

    if all_labels:
        label_string = ",".join(all_labels)
        query_parts.append(f"label:{label_string}")


    # Add difficulty label
    if difficulty:
        if difficulty.lower() == "beginner":
            query_parts.append('label:"good first issue"')
        elif difficulty.lower() == "intermediate":
            query_parts.append('label:"help wanted"')

    # Final query
    query = " ".join(query_parts)
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://api.github.com/search/issues?q={encoded_query}"
    return query, url 


def fetch_issues_from_github(query_url):
    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(query_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])
    else:
        return {"error": f"GitHub API error {response.status_code}: {response.text}"}

def find_github_issues(user_input):
    # Parse the prompt
    languages, frameworks, tools, difficulty, filters = get_filters(user_input)

    # Build query
    query, query_url = build_issue_query(languages, frameworks, tools, difficulty, filters)

    # Fetch results
    results = fetch_issues_from_github(query_url)

    return results
