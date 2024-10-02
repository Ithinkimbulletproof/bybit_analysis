import pandas as pd
import pandas_ta as ta
import requests

def fetch_historical_data(symbol):
    """Получение исторических данных по криптовалюте."""
    url = f"https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval=1&limit=200"
    response = requests.get(url)

    # Проверка на ошибки
    if response.status_code != 200:
        raise ValueError(
            f"Error fetching data for {symbol}: {response.text}")

    data = response.json()["result"]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["open_time"], unit="s")
    df.set_index("timestamp", inplace=True)
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df

def perform_analysis(symbol):
    """Анализирует монету и возвращает рекомендации по настройкам."""
    df = fetch_historical_data(symbol)

    # Пример анализа: расчет скользящих средних и RSI
    df["SMA20"] = ta.sma(df["close"], length=20)
    df["RSI"] = ta.rsi(df["close"], length=14)

    # На основании анализа выставляем примерные настройки
    if df["RSI"].iloc[-1] < 30:
        settings = {"strategy": "buy", "risk_level": "low"}
    elif df["RSI"].iloc[-1] > 70:
        settings = {"strategy": "sell", "risk_level": "high"}
    else:
        settings = {"strategy": "hold", "risk_level": "medium"}

    return settings, df.tail()  # Возвращаем настройки и последние строки с анализом
