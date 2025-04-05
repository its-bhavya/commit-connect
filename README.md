# 🚀 Commit-Connect

> *Empowering developers to dive into open source with confidence.*

**Commit-Connect** is an intelligent platform designed to help developers discover open-source repositories and issues tailored to their technical skills and interests. By integrating GitHub authentication, AI-based prompt understanding, and smart filtering, the platform provides a seamless experience to identify meaningful contribution opportunities.

---

## ✨ Key Features

- 🔐 **GitHub Authentication** using Personal Access Token
- 🧠 **AI Prompt Understanding** powered by Gemini API
- 🧰 **Skill-Based Recommendations** based on user repositories
- 🔍 **Advanced Filtering** (stars,forks,recent_updated, issue type)
- 📊 **Sorted Language Extraction** from GitHub profiles
- ⚡ **Streamlit-based Interactive Interface**

---

## ⚙️ Tech Stack

| Category        | Technologies Used                             |
|------------------|-----------------------------------------------|
| **Frontend**     | Streamlit                          |
| **Backend**      | Python, GitHub REST API                       |
| **AI Integration** | Gemini API by Google                        |
| **Authentication** | GitHub PAT (Personal Access Token)         |
| **Others**       | JSON         |

---

## 🧠 How It Works

1. **User Authentication** via GitHub Personal Access Token.
2. Platform **analyzes repositories** to extract top programming languages.
3. The platform fetches and filters GitHub repositories and issues based on user preferences and skills.
4. Users can input **natural language prompts** (e.g., "Looking for web dev issues").
5. Gemini API interprets the prompt to **enhance query context**.
6. GitHub repositories and issues are **fetched and filtered** based on preferences.
7. Developers receive **personalized suggestions** to start contributing instantly.

---

## 📁 Project Structure

.
├── .devcontainer/             # Development container configuration
├── .streamlit/                # Streamlit configuration files
│   ├── config.toml
│   └── secrets.toml
├── presentations/             # Project presentation materials
├── resources/images/          # UI background and design images
│   ├── BackgroundImage.jpg
│   └── Home Background Image.jpg
├── utils/                     # Utility modules
│   ├── __init__.py
│   └── github_api.py
├── venv/                      # Virtual environment (excluded from version control)
│   └── __init__.py
├── .gitignore                 # Git ignore rules
├── app.py                     # Main application entry point
├── auth.py                    # Handles GitHub authentication
├── gemini.py                  # Gemini API integration for prompt analysis
├── pyproject.toml             # Python project configuration
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── test_auth.py               # Unit tests for auth module
├── test_user_profile.py       # Unit tests for user profile functionalities




---

## 🎬 Demo Video

> Get a quick walkthrough of Commit-Connect in action!
> 
[![Watch Demo](https://img.shields.io/badge/Watch-Demo-red?style=for-the-badge&logo=google-drive)](https://drive.google.com/drive/folders/1LqvGvj5dxSUWDqA3ai6ZpwTj0Pe9t4pG)

🔗 [Watch on YouTube](https://www.youtube.com/watch?v=PGghOtSOTbE)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://commit-connect.streamlit.app/)


## 👥 Team

| Name      | Responsibilities                          |
|-----------|--------------------------------------------|
| **Aakriti Sharma**   | UI/UX Design, Frontend Design|
| **Bhavya**    | GEMINI API Integration,Prompt Engineering|
| **Deepti Yadav**    | Backend Development, GitHub API Integration |

We are a team of passionate developers committed to making open source accessible and impactful.

---


## 🙌 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Gemini API](https://ai.google.dev/)
- [GitHub REST API](https://docs.github.com/en/rest)

---

> _“Every open-source journey begins with a single commit — let Commit-Connect guide the way.”_



