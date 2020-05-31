'''各ファイルが JumanPsc を使って形態素解析可能かを検査する
'''

import os
from psc_conv import JumanPsc, mrph_test_dir
from juman_settings import *


# 入力ディレクトリ
input_dir = 'script_rawdata'

# ログ出力ファイル
log_file = 'mrph_test.log'

# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
log_file = os.path.join(os.path.dirname(__file__), log_file)

# 入力ディレクトリ内のファイルが形態素解析可能か調べる
juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
mrph_test_dir(juman=juman, input_dir=input_dir, log_file=log_file)
