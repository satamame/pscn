'''台本ファイルの行の種類を予測するためのモジュール
'''

import os
import re
from sklearn.tree import DecisionTreeClassifier
from . import PscClass, features_in_lines
from .features import ft_keys


def get_dataset(targets_dir, features_dir):
    '''教師ラベルと、対応する特徴量データを取得する
    
    Parameters
    ----------
    targets_dir : str
        教師ラベルファイルのディレクトリ
    features_dir : str
        特徴量ファイルのディレクトリ
    
    Returns
    -------
    targets : list
        教師ラベル (str) のリスト
    features : list
        特徴量 (list) のリスト
    '''
    
    targets = []
    features = []
    
    for entry in os.scandir(path=targets_dir):
        if not entry.is_file():
            continue
        
        # 特徴量データのファイル名
        basename = os.path.basename(entry).split('.', 1)[0]
        features_fname = os.path.join(features_dir, basename + '.csv')
        
        # 特徴量データがなければ、その教師ラベルはスキップ
        if not os.path.isfile(features_fname):
            continue
        
        # 教師ラベルファイルからラベルを取得
        with open(entry, encoding='utf_8_sig') as f:
            # 各行の空白文字以降を切り捨てた文字列を取得
            lines = f.readlines()
        labels = [re.split(r'\s', l, 1)[0] for l in lines]
        
        # 特徴量ファイルから対応する特徴量を取得
        with open(features_fname, encoding='utf_8_sig') as f:
            lines = [l.rstrip() for l in f.readlines()]
        fts = [l.split(',') for l in lines]
        
        # 少ない方の数に合わせる (エラーでも良いが)
        count = min(len(labels), len(fts))
        targets.extend(labels[:count])
        features.extend(fts[:count])
    
    # 教師ラベルを数値に変換 (未定義ならコメントとする)
    targets = [PscClass[t].value if t in PscClass._member_names_
        else PscClass.COMMENT.value
        for t in targets]
    
    return targets, features


def make_model(targets, features, max_depth):
    '''教師ラベルと、対応する特徴量データから決定木モデルを作成する
    
    Parameters
    ----------
    targets : list
        教師ラベル (str) のリスト
    features : list
        特徴量 (list) のリスト
    max_depth : int
        決定木の最大深度
    
    Returns
    -------
    tree : DecisionTreeClassifier
        決定木モデル
    '''
    
    # 決定木を学習させる
    tree = DecisionTreeClassifier(max_depth=max_depth)
    tree.fit(features, targets)
    
    return tree


def predict(juman, tree, lines, normalize=False):
    '''決定木モデルを使って台本の各行の種類を予測する
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    tree : DecisionTreeClassifier
        予測に使う決定木モデル
    lines : list
        行 (str) のリスト
    normalize : bool
        正規化するかどうか
    
    Yields
    ------
    label : PscClass
        各行の種類
    '''
    
    # 登場人物見出しが出た後か
    charsheadline_used = 0
    # 柱 (レベル1) が出た後か
    h1_used = 0
    # ト書きが出た後か
    direction_used = 0
    # セリフが出た後か
    dialogue_used = 0
    # 前の行のラベル
    prev_label = -1

    features = features_in_lines(juman, lines, normalize=normalize)
    for i, ft in enumerate(features):
        # 特徴量から取り出し順に値を取り出したリスト
        vals = [ft[k] for k in ft_keys]

        # 前の行の予測結果を使って特徴量を追加
        vals.append(prev_label == PscClass.CHARACTER.value)
        vals.append(prev_label == PscClass.CHARACTER_CONTINUED.value)
        vals.append(prev_label == PscClass.DIRECTION.value)
        vals.append(prev_label == PscClass.DIRECTION_CONTINUED.value)
        vals.append(prev_label == PscClass.DIALOGUE.value)
        vals.append(prev_label == PscClass.DIALOGUE_CONTINUED.value)
        vals.append(prev_label == PscClass.COMMENT.value)
        vals.append(prev_label == PscClass.COMMENT_CONTINUED.value)

        # ここまでの予測結果を使って特徴量を追加
        vals.append(charsheadline_used)
        vals.append(h1_used)
        vals.append(direction_used)
        vals.append(dialogue_used)

        # 予測する
        labels = tree.predict([vals])
        label = labels[0]
        yield label
        
        # 次ループ以降のための特徴量の更新
        if label == PscClass.CHARSHEADLINE.value:
            charsheadline_used = 1
        if label == PscClass.H1.value:
            h1_used = 1
        if label == PscClass.DIRECTION.value:
            direction_used = 1
        if label == PscClass.DIALOGUE.value:
            dialogue_used = 1
        prev_label = label


def give_labels(juman, tree, in_file, out_file, normalize=False):
    '''台本ファイルに予測したラベルをつけて保存する
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    tree : DecisionTreeClassifier
        予測に使う決定木モデル
    in_file : str
        入力ファイル名
    out_file : str
        出力ファイル名
    normalize : bool
        正規化するかどうか
    '''
    
    # 入力ファイルから行を取り出す
    with open(in_file, encoding='utf_8_sig') as in_f:
        lines = [l for l in in_f.readlines()]

    # 各行から行の種類を予測して文字列のジェネレータにする
    classes = predict(juman, tree, lines, normalize=normalize)
    labels = (PscClass(c).name for c in classes)
        
    # 出力ファイルにラベル付きの行を書き出す
    with open(out_file, 'w', encoding='utf_8_sig') as out_f:
        for line, label in zip(lines, labels):
            out_f.write(label + '\t' + line)
