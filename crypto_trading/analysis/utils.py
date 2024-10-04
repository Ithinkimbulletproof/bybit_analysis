import pandas as pd
import pandas_ta as ta
import requests


def convert_symbol(symbol):
    """Преобразование символов для использования с Bybit."""
    symbol_mapping = {
        "BTCUSDT": "BTCUSDT",
        "ETHUSDT": "ETHUSDT",
        "USDT": "USDT",
        "TON": "TONUSDT",
        "NOT": "NOTUSDT",
        "HMSTR": "HMSTRUSDT",
        "DOGS": "DOGSUSDT",
        "CATS": "CATSUSDT",
    }
    return symbol_mapping.get(symbol, symbol)


def fetch_historical_data_bybit(symbol):
    """Получение исторических данных с Bybit для криптовалюты."""
    url = f"https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval=1"
    response = requests.get(url)

    if (
        response.status_code != 200
        or "ret_code" in response.json()
        and response.json()["ret_code"] != 0
    ):
        raise ValueError(f"Error fetching data for {symbol}: {response.text}")

    data = response.json()["result"]
    df = pd.DataFrame(
        data, columns=["open_time", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["open_time"], unit="s")
    df.set_index("timestamp", inplace=True)
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df


def perform_analysis(symbol):
    """Анализирует монету и возвращает рекомендации по настройкам."""
    symbol = convert_symbol(symbol)

    df = fetch_historical_data_bybit(symbol)

    df["SMA20"] = ta.sma(df["close"], length=20)
    df["RSI"] = ta.rsi(df["close"], length=14)

    if df["RSI"].iloc[-1] < 30:
        settings = {"strategy": "buy", "risk_level": "low"}
    elif df["RSI"].iloc[-1] > 70:
        settings = {"strategy": "sell", "risk_level": "high"}
    else:
        settings = {"strategy": "hold", "risk_level": "medium"}

    return settings, df.tail()
