#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import tate_encoder as tenc

HOST = 'localhost'  # ホストのアドレス
PORT = 51234        # ホストのポート


# メッセージを特定のアドレスポートに送信する
async def post_message(req):
    # 接続を確立する
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # メッセージを送信し、その後送信終了
    writer.write(req)
    writer.write_eof()
    await writer.drain()

    # 相手が全てのデータを送信完了するまで
    # 受信を続ける
    data = bytes()
    while(not reader.at_eof()):
        data += await reader.read(1024,)

    # 読み取ったデータをデコード
    codes = tenc.decode_all(data)
    if(codes[1] == tenc.SERVER_REPLY_ID):
        message = codes[2]
    else:
        message = 'Err'

    # 受信したデータを表示
    addr = writer.get_extra_info('peername')
    print(f'Received {codes} from {addr}')
    print(message)

    writer.close()


async def main():
    session = 0
    while True:
        session += 1

        mode = int(input('モード0-1>'))

        if(mode == 0):
            message = input('メッセージを入力>')
            req = tenc.encode_clireq_push(session, session, message)
        elif(mode == 1):
            message_id = int(input('メッセージ番号>'))
            req = tenc.encode_clireq_pop(session, message_id)
        else:
            continue

        await post_message(req)

asyncio.run(main())
