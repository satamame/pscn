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

# モデルの読み込み
with open(model_file, 'rb') as f:
    tree = pickle.load(f)

# 動作確認用データ

lines = [
    "プロローグ",
    "",
    "　　　　　　　　　　おもむろに音楽。",
    "　　　　　　　　　　『惑星--木星--』",
    "　　　　　　　　　　舞台上には数人の人。",
    "　　　　　　　　　　はるか遠くを見つめる目。",
    "　　　　　　　　　　感動的なシーンだ。",
    "　　　　　　　　　　音楽クライマックス。",
    "　　　　　　　　　　あわせるように溶暗。",
    "　　　　　　　　　　幕。",
    "",
    "　　　　　　　　　　明かりが付くとカーテンコール。",
    "　　　　　　　　　　全員並んでいる。",
    "代表「えー、本日は、劇団○○公演『セルフコントロール』に御来場いただきましてありがとうございます。僭越ながら、キャストの紹介をいたしたいと思います。」",
    "　　　　　　　　　　キャスト紹介。",
    "代表「本日は、本当にありがとうございました。」",
    "全員「ありがとうございました。」",
    "　　　　　　　　　　暗転。",
]
juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
labels = model.predict(juman, tree, lines, normalize=False)
print([l for l in labels])
