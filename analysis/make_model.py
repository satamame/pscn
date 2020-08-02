import os
import pickle
from sklearn.metrics import accuracy_score, classification_report
from psc_conv import JumanPsc, model
from psc_conv import get_dataset, make_model, PscClass
from juman_settings import JUMAN_COMMAND, JUMAN_OPTION


# 教師ラベルファイルのディレクトリ
targets_dir = 'script_targets'

# 特徴量ファイルのディレクトリ
features_dir = 'script_features'

# モデルの保存ファイル名
model_name = 'model.pkl'

# 特徴量を正規化しているか
normalize = False

# テスト用の台本ファイル (教師ラベルファイルに対応) のディレクトリ
scripts_dir = 'script_samples'

# 特定のラベルのみ検証する場合の設定 (すべてのラベルを使うなら空にする)
active_classes = {
    # PscClass.DIRECTION.value,
    # PscClass.DIALOGUE.value,
    # PscClass.EMPTY.value,
}
# それ以外のラベルを何として扱うか
default_class = PscClass.COMMENT.value

# 決定木の深度
max_depth = 20

# 相対パスを絶対パスに
targets_dir = os.path.join(os.path.dirname(__file__), targets_dir)
features_dir = os.path.join(os.path.dirname(__file__), features_dir)
scripts_dir = os.path.join(os.path.dirname(__file__), scripts_dir)

# データセットを取得 (複数の台本の特徴量が統合される)
targets, features = get_dataset(targets_dir, features_dir)

# 特定のラベルのみ検証する設定なら、それを適用する
if active_classes:
    targets = [t if t in active_classes else default_class for t in targets]

# 決定木を作る
tree = make_model(targets, features, max_depth=max_depth)

# テストデータで予測する (今は学習データと同じ)
# predicted = tree.predict(features)

# 精度検証に使うファイル名のリストを作る
test_files = []
for entry in os.scandir(path=targets_dir):
    if not entry.is_file():
        continue
    
    # 教師ラベルと同じファイル名の特徴量データがあるか
    basename = os.path.basename(entry).split('.', 1)[0]
    features_fname = os.path.join(features_dir, basename + '.csv')
    
    # 特徴量データがなければ、その教師ラベルはスキップ
    if not os.path.isfile(features_fname):
        continue

    test_files.append(basename)

# 学習に使ったのと同じデータで予測してみる
juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
predicted = []
for basename in test_files:
    filename = os.path.join(scripts_dir, basename + '.txt')

    # 台本データがなければスキップ
    if not os.path.isfile(filename):
        continue

    # 各行から行の種類を予測する
    with open(filename, encoding='utf_8_sig') as in_f:
        lines = [l for l in in_f.readlines()]
    classes = model.predict(juman, tree, lines, normalize=normalize)
    predicted.extend(list(classes))

# 精度を確認する
report = classification_report(targets, predicted)
print(report)
score = accuracy_score(targets, predicted)
print(f'Score: {score}')

# モデルを保存する
model_file = os.path.join(os.path.dirname(__file__), model_name)
with open(model_file, 'wb') as f:
    pickle.dump(tree, f)
print(f'Model saved as {model_name}.')
