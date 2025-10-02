"""
Filename: script.py
Author: Joseph Milliken
Date: 2025-10-01
Description:
    The-cron-report: Daily job to gather all your 
        informational needs for the day. 

Dependencies:
    - Refer to requirements.txt
"""
import os
import requests
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

load_dotenv()

def get_yesterdays_headlines(n = 3, country = "us", q = "news"):
    """
    Get the top n headlines from yesterday's news
        using the newsapi from newsapi.org.

    Args:
        n : Desired number of articles to be retrieved. 
        country : Desired country where the news is being covered.
        q : Desired query or keyword searches. 

    Returns:
        The n headlines from the country using the q keywords or phrases.
        May prematurely return 

    Raises:
        ValueError if the API key is missing in the enviornment variables.
        RuntimeError if the API's endpoint response is not ok (status = error) 
        
    """

    today = date.today()
    yesterday = today - timedelta(days=1)
    print(f"Top Headlines from Yesterday: {yesterday} \n")

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY: 
        raise ValueError("NEWS_API_KEY missing in enviornment variables.")

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey" : NEWS_API_KEY,
        "q" : q,
        "from": str(yesterday),
        "to": str(yesterday),
        "sortBy": "popularity",
        "language": "en",
        "pageSize": n,
        "country": country
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        error_msg = data.get("message", "Unknown error")
        raise RuntimeError(f"Error fetching news... {error_msg}")
    
    headlines = []
    for article in data["articles"]:
        title = article["title"]
        source = article["source"]["name"]
        url = article["url"]
        headlines.append(f"{title} ({source})\n{url}\n")

    return "\n".join(headlines)

if __name__ == "__main__":
    print(get_yesterdays_headlines())
