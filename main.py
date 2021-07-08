import json
import logging
import websocket

from parser import Parser

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)

parser = Parser()
args = parser.parse_args()
period = args.periods

interval = '1m'
tickers = [
    'ETHUSDT',
    'BNBBTC',
    'BTCUSDT',
]
candles = {ticker: [] for ticker in tickers}


def on_open(ws):
    params = [ticker.lower() + '@kline_' + interval for ticker in tickers]
    message = {'method': 'SUBSCRIBE', 'params': params, 'id': 1,}
    ws.send(json.dumps(message))
    logging.info('Connected to binance websocket')
    logging.info(f'Waiting for {period} minutes to get SMA results.')


def on_message(ws, message):
    message = json.loads(message)
    if 'result' in message:
        return
    candle = message['k']
    is_candle_closed = candle['x']
    if is_candle_closed:
        symbol = candle['s']
        close = float(candle['c'])
        round_to = str(close)[::-1].find('.')
        candles[symbol].append(close)
        sma = count_sma(candles[symbol], period)
        if sma:
            logging.info(f'{symbol}\t{round(sma, round_to)}')


def count_sma(lst, period):
    if len(lst) != period:
        return
    sum_ = 0
    for el in lst:
        sum_ += el
    lst.pop(0)
    return sum_ / period


def on_close(ws, close_status_code, close_msg):
    logging.info("Connection closed")


def run_websocket():
    ws = websocket.WebSocketApp(
        url='wss://stream.binance.com:9443/ws',
        on_open=on_open,
        on_close=on_close,
        on_message=on_message,)
    ws.run_forever()


if __name__ == '__main__':
    try:
        run_websocket()
    except Exception as e:
        logging.error(e)
        logging.info("Connection failed")
