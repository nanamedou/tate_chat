#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import tate_encoder as tenc

HOST = ''       # 作成するtサーバのアドレス
PORT = 51234    # 作成するtサーバのポート

chat_data = dict()  # チャットの内容を保存する辞書


# 発言番号と内容を保存する
def push_message(id, message):
    chat_data[id] = message


# 発言番号から内容を取り出して削除する
def pop_message(id):
    message = chat_data[id]
    chat_data.pop(id)
    return message


# サーバに送られたメッセージをそのまま返送するコールバック関数
async def server_callback(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):

    # 相手が全てのデータを送信完了するまで
    # 読み取りを続ける
    data = bytes()
    while(not reader.at_eof()):
        data += await reader.read(1024)

    # 読み取ったデータをデコード
    codes = tenc.decode_all(data)

    # 受信したデータを表示
    addr = writer.get_extra_info('peername')
    print(f'Received {codes} from {addr}')

    # 返信するデータを生成する
    if(codes[1] == tenc.CLIREQ_PUSH_ID):
        push_message(codes[2], codes[3])
        message = f'Your message accepted! id={codes[2]}'
    elif(codes[1] == tenc.CLIREQ_POP_ID):
        message = pop_message(codes[2])
    else:
        message = 'Unknown command!'

    reply = tenc.encode_server_reply(codes[0], message)

    # 返送を送信する
    writer.write(reply)
    await writer.drain()

    # 送信終了
    writer.close()


async def main():

    # サーバーを作成
    server = await asyncio.start_server(server_callback, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f'Ruinning Server {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
