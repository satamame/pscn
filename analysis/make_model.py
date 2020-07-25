import os
from sklearn.metrics import accuracy_score, classification_report
from psc_conv import get_dataset, make_model, PscClass


# 教師ラベルファイルのディレクトリ
targets_dir = 'script_targets'

# 特徴量ファイルのディレクトリ
features_dir = 'script_features'

# 特定のラベルのみ検証する場合の設定 (すべてのラベルを使うなら空にする)
active_classes = {
    # PscClass.DIRECTION.value,
    # PscClass.DIALOGUE.value,
    # PscClass.EMPTY.value,
}
# それ以外のラベルを何として扱うか
default_class = PscClass.COMMENT.value

# 決定木の深度
max_depth = 10

# 相対パスを絶対パスに
targets_dir = os.path.join(os.path.dirname(__file__), targets_dir)
features_dir = os.path.join(os.path.dirname(__file__), features_dir)

# データセットを取得 (複数の台本の特徴量が統合される)
targets, features = get_dataset(targets_dir, features_dir)

# 特定のラベルのみ検証する設定なら、それを適用する
if active_classes:
    targets = [t if t in active_classes else default_class for t in targets]

# 決定木を作る
tree = make_model(targets, features, max_depth=max_depth)

# テストデータで予測する (今は学習データと同じ)
predicted = tree.predict(features)

# 精度を確認する
report = classification_report(targets, predicted)
print(report)
score = accuracy_score(targets, predicted)
print(f'Score: {score}')


# TODO: 精度が十分であればモデルを保存する処理を追加

