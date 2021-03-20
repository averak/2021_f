import sys
import websocket
import _thread
import json


def on_message(ws, message):
    # 今はこの関数の中でmessageの加工を行っている。
    print('--- RECV MSG. --- ')
    print(message)


def on_error(ws, error):
    print('--- ERROR --- ')
    print(error)


def on_close(ws):
    print('--- DISCONNECTED --- ')


def on_open(ws):
    print('--- CONNECTED --- ')
    ws.send('{"method": "PROXY","from": "DOOR","select": "3"}')
    _thread.start_new_thread(run, ())


def run():
    while True:
        try:
            params: dict = {
                "method": "PROXY",
                "from": "DOOR",
                "select": input("input : ") or "3" ,
            }
            print(json.dumps(params))
            ws.send(json.dumps(params))
        except KeyboardInterrupt:
            break


url = 'ws://hack.inatatsu.com:8000/'
# websocket.enableTrace(True)
ws = websocket.WebSocketApp(url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
ws.run_forever()
