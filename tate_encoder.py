# ---------------------------------------------------- #
#
# tate chat 内での通信で
# 送受信するデータのエンコード・デコードを行うコード
#
# 大まかな内容は以下のような構造になっている
# - バージョン番号                  1 byte
# - セッション番号                  8 byte
# - コンテンツ全体のサイズ(byte)    8 byte
# - コンテンツ                      any
#
# コンテンツは以下のような構造になっている
# - 命令id                      2 byte
# - 命令ごとの値                 any (encode関数の contents生成部分で要確認)
# ---------------------------------------------------- #


VERSION = 1
VERSION_BYTES = (1).to_bytes(1, byteorder='big')    # バージョン番号

NO_COMMAND_ID = 0
SERVER_REPLY_ID = 1
CLIREQ_PUSH_ID = 2
CLIREQ_POP_ID = 3


def encode_server_reply(session: int, message: str):
    bmessage = message.encode()

    # contents生成
    contents = bytes()
    contents += (SERVER_REPLY_ID).to_bytes(2, byteorder='big')  # 命令番号
    contents += len(bmessage).to_bytes(8, byteorder='big')       # メッセージサイズ
    contents += bmessage                                # メッセージ内容

    # データ生成
    data = bytes()
    data += VERSION_BYTES                                   # バージョン番号
    data += session.to_bytes(8, byteorder='big')            # セッション番号
    data += len(contents).to_bytes(8, byteorder='big')      # コンテンツ全体のサイズ
    data += contents                                        # コンテンツ

    return data


def encode_clireq_push(session: int, id: int, message: str):
    bmessage = message.encode()

    # contents生成
    contents = bytes()
    contents += (CLIREQ_PUSH_ID).to_bytes(2, byteorder='big')  # 命令番号
    contents += id.to_bytes(8, byteorder='big')               # メッセージ番号
    contents += len(bmessage).to_bytes(8, byteorder='big')    # メッセージサイズ
    contents += bmessage                                      # メッセージ内容

    # データ生成
    data = bytes()
    data += VERSION_BYTES                                   # バージョン番号
    data += session.to_bytes(8, byteorder='big')            # セッション番号
    data += len(contents).to_bytes(8, byteorder='big')      # コンテンツ全体のサイズ
    data += contents                                        # コンテンツ

    return data


def encode_clireq_pop(session: int, id: int):

    # contents生成
    contents = bytes()
    contents += (CLIREQ_POP_ID).to_bytes(2, byteorder='big')  # 命令番号
    contents += id.to_bytes(8, byteorder='big')               # メッセージ番号

    # データ生成
    data = bytes()
    data += VERSION_BYTES                                   # バージョン番号
    data += session.to_bytes(8, byteorder='big')            # セッション番号
    data += len(contents).to_bytes(8, byteorder='big')      # コンテンツ全体のサイズ
    data += contents                                        # コンテンツ

    return data


def decode_all(data: bytes):

    # 共通部分の解読
    version = int.from_bytes(data[0:1], byteorder='big')  # バージョン番号
    session = int.from_bytes(data[1:9], byteorder='big')  # セッション番号
    if(version != VERSION):
        return (session, NO_COMMAND_ID)                 # バージョンが違うやつは読むのやめとく
    size = int.from_bytes(data[9:17], byteorder='big')   # コンテンツ全体のサイズ
    contents = data[17:17+size]                             # コンテンツ
    command = int.from_bytes(contents[0:2], byteorder='big')  # 命令番号

    # 命令ごとの解読
    if(command == SERVER_REPLY_ID):
        message_size = int.from_bytes(
            contents[2:10], byteorder='big')      # メッセージサイズ
        # メッセージ内容
        message = contents[10:10+message_size].decode()
        return (session, command, message)
    elif(command == CLIREQ_PUSH_ID):
        message_id = int.from_bytes(
            contents[2:10], byteorder='big')         # メッセージ番号
        message_size = int.from_bytes(
            contents[10:18], byteorder='big')      # メッセージサイズ
        # メッセージ内容
        message = contents[18:18+message_size].decode()
        return (session, command, message_id, message)
    elif(command == CLIREQ_POP_ID):
        message_id = int.from_bytes(
            contents[2:10], byteorder='big')    # メッセージ番号
        return (session, command, message_id)
    print('bb')
    return (session, NO_COMMAND_ID)
