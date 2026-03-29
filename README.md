# 🗂️ AI File Organiser

An AI-powered file organiser that automatically sorts your folders by file type, date, and AI-detected project topic — built with Groq's Llama 3.3 and a simple GUI.

## Features
- AI detects what project/topic each file belongs to from its filename
- Sorts into `Type/Date/Topic/` subfolders
- Duplicate detection with MD5 hashing — asks what to do with each one
- Clean GUI with folder picker and live log

## Setup
1. Clone the repo and navigate into it
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your Groq API key: `GROQ_API_KEY=your_key_here`
4. Run: `python organiser.py`

Get a free Groq API key at [console.groq.com](https://console.groq.com)

## Tech Stack
Python, Tkinter, LangChain, Groq (Llama 3.3 70B)

## ⚠️ Note
Test on a copy of your folder first before running on anything important.

## Licence
MIT
