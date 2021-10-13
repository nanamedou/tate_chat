#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

HOST = 'localhost'  # ホストのアドレス
PORT = 51234        # ホストのポート

# メッセージを特定のアドレスポートに送信する
async def post_message(message):
    # 接続を確立する
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # メッセージを送信し、その後送信終了
    writer.write(message)
    await writer.drain()
    writer.close()

    # 相手が全てのデータを送信完了するまで
    # 受信を続ける
    data = bytes()
    while(not reader.at_eof()):
        data += await reader.read(1024)

    # 受信したデータを表示
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f'Received {message} from {addr}')


async def main():
    # 入力されたメッセージを送信する
    message = input('メッセージを入力:').encode()
    await post_message(message)


while True:
    asyncio.run(main())
