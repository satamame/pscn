# フォルダ構成

## スクリプト

- juman_check.py
    - JumanPsc の形態素解析を単品の文字列で試すスクリプト。
- juman_settings.py
    - JumanPsc の初期値を定義している。
- make_features.py
    - 複数の台本ファイルを一括で、形態素解析～特徴量抽出までする。
    - 形態素解析不可能なファイルについては、エラーになった行をレポートする。
- mrph_match_check.py
    - MrphMatch の形態素マッチングを単品の文字列で試すスクリプト。
- mrph_test.py
    - 各ファイルが JumanPsc を使って形態素解析可能かを検査するスクリプト。
    - 形態素解析不可能なファイルについては、エラーになった行をレポートする。
- mrph_to_excel.py
    - サンプルファイルの各行を形態素解析して表を作るスクリプト。

## フォルダ

- script_rawdata/
    - 生の台本データ (txt) を入れておくフォルダ。
    - 形態素解析可能と分かったデータは、`script_samples/` に移す。
- script_samples/
    - 特徴量の取り出し元となる台本ファイル (txt) を入れておくフォルダ。
- script_features/
    - 台本ごとの特徴量ファイル (csv) を保存するフォルダ。
- script_targets/
    - 教師ラベルファイル (txt) を入れておくフォルダ。
    - `script_features` フォルダと同名のファイル同士が対応する。

# 解析手順

## 台本データの準備

1. 台本のテキストファイルを `script_rawdata/` に入れておく。
1. `morph_test.py` を実行する。
1. エラーが出なかったら、すべてのファイルを `script_samples/` に移す。
1. エラーが出たら、データまたはスクリプトを修正する。
    1. データのみ修正した場合
        - エラーが出なかったファイルを `script_samples/` に移す。
    1. スクリプトを修正した場合
        - `script_samples/` にあるファイルを `script_rawdata/` に戻す。
1. すべてのファイルが `script_samples/` に入るまで2～4を繰り返す。

## 特徴量の取り出し

1. "台本データの準備" の手順を実施して、台本データが `script_samples/` にあるようにする。
1. `make_features.py` を実行する。
1, 各台本に対応する特徴量ファイルが、`script_features/` に作成される。

## 教師データの準備

教師データは、台本の各行の先頭に「行の種類」を付加したテキストファイルです。  
行頭に「行の種類」+ \t を記述します。  
「行の種類」だけでも良いです (\t 以降は無視されるという仕様)。

1. 教師データは、`script_targets/` に入れておく。
1. 教師データに対応する特徴量データが、同じファイル名で `script_samples/` に存在すること。

行の種類は、以下の文字列です。

- "TITLE"
- "AUTHOR"
- "CHARSHEADLINE"
- "CHARACTER"
- "H1"
- "H2"
- "H3"
- "DIRECTION"
- "DIALOGUE"
- "ENDMARK"
- "COMMENT"
- "EMPTY"
- "CHARACTER_CONTINUED"
- "DIRECTION_CONTINUED"
- "DIALOGUE_CONTINUED"
- "COMMENT_CONTINUED"
