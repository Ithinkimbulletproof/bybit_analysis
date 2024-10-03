import pandas as pd
import pandas_ta as ta
import requests

def convert_symbol(symbol):
    """Преобразование символов для использования с Kraken."""
    symbol_mapping = {
        'BTCUSDT': 'XXBTZUSD',
        'ETHUSDT': 'XETHZUSD',
        'USDT': 'USDTZUSD',
        'TON': 'TONUSDT',
        'NOT': 'NOTUSDT',
        'HMSTR': 'HMSTRUSDT',
        'DOGS': 'DOGSUSDT',
        'CATS': 'CATSUSDT',
    }
    return symbol_mapping.get(symbol, symbol)  # Если нет совпадения, возвращаем исходный символ

def fetch_historical_data_kraken(symbol):
    """Получение исторических данных с Kraken для криптовалюты."""
    url = f"https://api.kraken.com/0/public/OHLC?pair={symbol}&interval=1"
    response = requests.get(url)

    # Проверка на ошибки
    if response.status_code != 200 or 'error' in response.json() and response.json()['error']:
        raise ValueError(
            f"Error fetching data for {symbol}: {response.text}")

    data = response.json()['result'][symbol]
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    df['timestamp'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    return df

def perform_analysis(symbol):
    """Анализирует монету и возвращает рекомендации по настройкам."""
    # Преобразуем символ перед запросом данных
    symbol = convert_symbol(symbol)

    # Получаем исторические данные
    df = fetch_historical_data_kraken(symbol)

    # Пример анализа: расчет скользящих средних и RSI
    df['SMA20'] = ta.sma(df['close'], length=20)
    df['RSI'] = ta.rsi(df['close'], length=14)

    # На основании анализа выставляем примерные настройки
    if df['RSI'].iloc[-1] < 30:
        settings = {'strategy': 'buy', 'risk_level': 'low'}
    elif df['RSI'].iloc[-1] > 70:
        settings = {'strategy': 'sell', 'risk_level': 'high'}
    else:
        settings = {'strategy': 'hold', 'risk_level': 'medium'}

    return settings, df.tail()  # Возвращаем настройки и последние строки с анализом
