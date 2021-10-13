#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

HOST = ''       # 作成するtサーバのアドレス
PORT = 51234    # 作成するtサーバのポート


# サーバに送られたメッセージをそのまま返送するコールバック関数
async def echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

    # 相手が全てのデータを送信完了するまで
    # 読み取りを続ける
    data = bytes()
    while(not reader.at_eof()):
        data += await reader.read(1024)

    # 受信したデータを表示
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f'Received {message} from {addr}')

    # 返送を送信する
    writer.write(data)
    await writer.drain()

    # 送信終了
    writer.close()


async def main():

    # サーバーを作成
    server = await asyncio.start_server(echo, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f'Ruinning Server {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
