import requests
from bs4 import BeautifulSoup

def extract_latest_news(ticker_symbol):
    base_url = f"https://finance.yahoo.com/quote/{ticker_symbol}/"
    
    try:
        response = requests.get(base_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.find_all('h3', limit=3)
        
        news = [headline.get_text(strip=True) for headline in headlines]
        return news if news else ["No headlines found."]
        
    except Exception as e:
        return [f"Error fetching news: {str(e)}"]
