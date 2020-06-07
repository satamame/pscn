'''台本の行の種類の定義
'''

from enum import Enum


class PscClass(Enum):
    '''台本の行の種類
    '''
    
    TITLE = 0                   # 題名
    AUTHOR = 1                  # 著者名
    CHARSHEADLINE = 2           # 登場人物見出し
    CHARACTER = 3               # 登場人物
    H1 = 4                      # 柱 (レベル1)
    H2 = 5                      # 柱 (レベル2)
    H3 = 6                      # 柱 (レベル3)
    DIRECTION = 7               # ト書き
    DIALOGUE = 8                # セリフ
    ENDMARK = 9                 # エンドマーク
    COMMENT = 10                # コメント
    EMPTY = 11                  # 空行
    CHARACTER_CONTINUED = 12    # 登場人物の2行目以降
    DIRECTION_CONTINUED = 13    # ト書きの2行目以降
    DIALOGUE_CONTINUED = 14     # セリフの2行目以降
    COMMENT_CONTINUED = 15      # コメントの2行目以降
