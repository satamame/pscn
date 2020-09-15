'''台本データを入力して行の種類を出力する

python predict_file(in_file, out_file, normalize)

Parameters
----------
in_file : str
    入力ファイル名
out_file : str
    出力ファイル名
normalize : str
    特徴量が正規化されたモデルを使うなら '--normalize'
'''

import os
import sys
import pathlib
import pickle

from psc_parse import JumanPsc, model
from juman_settings import JUMAN_COMMAND, JUMAN_OPTION


def main():
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    normalize = False
    if len(sys.argv) > 3 and sys.argv[3] == '--normalize':
        normalize = True
    
    # 引数のファイル名を絶対パスに変換
    in_path = pathlib.Path(in_file)
    out_path = pathlib.Path(out_file)
    in_file = str(in_path.resolve())
    out_file = str(out_path.resolve())
    
    juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
    model_file = os.path.join(os.path.dirname(__file__), 'model.pkl')

    with open(model_file, 'rb') as f:
        tree = pickle.load(f)
    
    model.give_labels(juman, tree, in_file, out_file, normalize=normalize)


if __name__ == "__main__":
    main()
