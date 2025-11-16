# AI-News-Telegram-Bot
![Telegram Bot Image](https://www.webopedia.com/wp-content/uploads/2024/10/what-is-a-telegram-bot-cover-2.webp)
[![GitHub Stars](https://img.shields.io/github/stars/adelabbaszare/AI-News-Telegram-Bot?style=social)](https://github.com/adelabbaszare/AI-News-Telegram-Bot)
![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://t.me/)

A Telegram bot written in Python that fetches news and posts them in a channel or chat.  
This repository contains the initial version of `news_bot.py` and is ready for you to configure and run.

---

## 📋 Table of Contents

- [Features](#features)
- [Folder & File Structure](#folder--file-structure)   
- [Prerequisites](#prerequisites)  
- [Setup](#setup)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

- Fetch news from a specified source (RSS feed, API, or custom)  
- Post the news into a Telegram channel or chat via the Bot API  
- Simple, minimal setup for quick deployment  
- Ready to extend (topics, languages, intervals, formatting)

---

## Folder & File Structure
```bash
AI-News-Telegram-Bot/
│
├─ news_bot_en.py            # main bot script (English)
├─ news_bot_fa.py            # main bot script (Persian)
├─ requirements.txt          # list of dependencies
├─ send_links.txt            # created at runtime to track already-sent article links (to prevent send duplicate articles)
├─ .env                      # configuration variables
└─ README.md                 # this file
```

---

## Prerequisites

- Python **3.13+**
- A Telegram Bot token from [@BotFather](https://t.me/BotFather)  
- Access to a news source: RSS feed URL or news-API  
- `pip` and a virtual environment for package isolation  

---

## Setup
1. Clone the repository:
```bash
git clone https://github.com/adelabbaszare/AI-News-Telegram-Bot.git
cd AI-News-Telegram-Bot
```
2. (Recommended) Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
3. Install dependencies (if you have a requirements.txt):
```bash
pip install -r requirements.txt
```

## Configuration
You need to set up your bot token and optionally the news source API key.
1. Create a .env file at the project root.

2. Add the following example variables:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEG­RAM_CHAT_ID=@YourChannel Or ChatID
NEWS_API_KEY=your_api_key_if_any
```

3. In your news_bot.py, make sure you load those environment/config values. For example:
```python
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NEWS_SOURCE = os.getenv("NEWS_SOURCE_URL")
API_KEY = os.getenv("NEWS_API_KEY")
```
4. Update any other config in news_bot.py (e.g., polling interval, number of items per post, message formatting) as needed.


## Usage
Once configured, simply run:
```python
python news_bot.py
```
The bot will fetch news from the source, format it, and send it to the specified Telegram chat/channel.
If you want to stop it: press `Ctrl + C`.


## Contributing
Feel free to contribute! Here’s how:
- Fork the repository
- Create a new branch: ``git checkout -b feature/your-feature-name``
- Make your changes, test thoroughly
- Commit your changes with a meaningful message: `e.g., feat: add Persian language support`
- Push to your fork and open a Pull Request
- Please ensure code style, error handling, and documentation are maintained.


## License
This project is open source and available under the MIT License. See the LICENSE
 file for details.


## Contact / Support
If you encounter issues or have suggestions, please open an issue in this repository or contact Adel.
Happy coding🚀
