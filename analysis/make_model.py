import os
from sklearn.metrics import accuracy_score
from psc_conv import get_dataset, make_model, PscClass


# 教師ラベルファイルのディレクトリ
targets_dir = 'script_targets'

# 特徴量ファイルのディレクトリ
features_dir = 'script_features'

# 決定木の深度
max_depth = 10

# 相対パスを絶対パスに
targets_dir = os.path.join(os.path.dirname(__file__), targets_dir)
features_dir = os.path.join(os.path.dirname(__file__), features_dir)

# データセットを取得
targets, features = get_dataset(targets_dir, features_dir)

# 教師ラベルは、「セリフの1行目か、そうでないか」に限定する
# dlg_id = PscClass.DIALOGUE.value
# targets = [t if t == dlg_id else 0 for t in targets]

# 決定木を作る
tree = make_model(targets, features, max_depth=max_depth)

# 精度を確認する
predicted = tree.predict(features)
score = accuracy_score(targets, predicted)
print(f'Score: {score}')

# TODO: 精度が十分であればモデルを保存する処理を追加

