'''複数の台本ファイルを一括で、形態素解析～特徴量抽出までする
'''

import os
from psc_parse import JumanPsc, make_features
from juman_settings import JUMAN_COMMAND, JUMAN_OPTION


# 入力ディレクトリ
input_dir = 'script_samples'

# 出力ディレクトリ
output_dir = 'script_features'

# 教師ラベルファイルのディレクトリ
targets_dir = 'script_targets'

# 最初に出力ディレクトリを空にするか
empty_output_dir = True

# 特徴量を正規化するか
normalize = False

# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
output_dir = os.path.join(os.path.dirname(__file__), output_dir)
targets_dir = os.path.join(os.path.dirname(__file__), targets_dir)

# 特徴量を作る
juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
make_features(juman, input_dir, output_dir, targets_dir,
    empty_output_dir=empty_output_dir, normalize=normalize)
