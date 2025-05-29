import yfinance as yf

def fetch_stock_snapshot(ticker_list):
    summary = {}
    for code in ticker_list:
        ticker = yf.Ticker(code)
        try:
            closing = ticker.history(period="2d")['Close']
            delta = closing.iloc[-1] - closing.iloc[-2]
            summary[code] = {
                "latest_close": closing.iloc[-1],
                "change": round(delta, 2),
                "earnings_date": str(ticker.calendar.columns[0]) if not ticker.calendar.empty else "N/A"
            }
        except Exception as err:
            summary[code] = {"error": str(err)}
    return summary
