'''台本ファイルの行の種類を予測し、ラベルを付けて別名保存する
'''

import os
import pickle
from psc_conv import JumanPsc
from psc_conv import model
from juman_settings import JUMAN_COMMAND, JUMAN_OPTION

# 入力ディレクトリ
input_dir = 'script_samples'

# 出力ディレクトリ
output_dir = 'script_predicted'

# 予測に使うモデルのファイル名
model_name = 'model.pkl'

# 最初に出力ディレクトリを空にするか
empty_output_dir = True

# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
output_dir = os.path.join(os.path.dirname(__file__), output_dir)
model_file = os.path.join(os.path.dirname(__file__), model_name)

# 出力ディレクトリがなければ作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 出力ディレクトリを空にする
if empty_output_dir:
    for entry in os.scandir(path=output_dir):
        if entry.is_file():
            os.remove(entry)

# モデルの読み込み
with open(model_file, 'rb') as f:
    tree = pickle.load(f)

juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)

for entry in os.scandir(path=input_dir):
    if not entry.is_file():
        continue

    filename = os.path.basename(entry)
    out_file = os.path.join(output_dir, filename)
    model.give_labels(juman, tree, entry, out_file, normalize=False)
    print(filename)

print('Done')
