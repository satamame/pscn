'''複数の台本ファイルを一括で、形態素解析～特徴量抽出までする
'''

import os
from psc_conv import JumanPsc, make_features
from juman_settings import *


# 入力ディレクトリ
input_dir = 'script_samples'

# 出力ディレクトリ
output_dir = 'script_features'

# 最初に出力ディレクトリを空にするか
empty_output_dir = True

# 特徴量を正規化するか
normalize = False

# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
output_dir = os.path.join(os.path.dirname(__file__), output_dir)

# 特徴量を作る
juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
make_features(juman, input_dir, output_dir,
    empty_output_dir=empty_output_dir, normalize=normalize)
