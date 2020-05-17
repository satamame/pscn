#%%
import os
import re
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from psc_settings import psc_classes


#%%
# 教師ラベルファイルのディレクトリ
targets_dir = 'script_targets'

# 特徴量ファイルのディレクトリ
features_dir = 'script_features'

# 決定木の深度
max_depth = 10


#%%
# 相対パスを絶対パスに
targets_dir = os.path.join(os.path.dirname(__file__), targets_dir)
features_dir = os.path.join(os.path.dirname(__file__), features_dir)

def get_dataset(targets_dir, features_dir):
    '''教師ラベルと、対応する特徴量データを取得する
    '''
    
    targets = []
    features = []
    
    for entry in os.scandir(path=targets_dir):
        if not entry.is_file():
            continue
        
        # 特徴量データのファイル名
        basename = os.path.basename(entry).split('.', 1)[0]
        features_fname = os.path.join(features_dir, basename + '.csv')
        
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
    
    return targets, features


#%%
# 教師ラベルと特徴量を取得
targets, features = get_dataset(targets_dir, features_dir)

# 教師ラベルを数値に変換
targets = [psc_classes.index(t) for t in targets]

# 教師ラベルは、「セリフの1行目か、そうでないか」に限定する
dlg_id = psc_classes.index('DIALOGUE')
targets = [t if t == dlg_id else 0 for t in targets]

#%%
# 決定木を学習させる
clf = DecisionTreeClassifier(max_depth=max_depth)
clf.fit(features, targets)

#%%
# 精度を確認する
predicted = clf.predict(features)
score = accuracy_score(targets, predicted)
print(f'Score: {score}')

# TODO: 精度が十分であればモデルを保存する処理を追加


# %%
