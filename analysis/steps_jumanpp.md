# JUMAN++ を Windows でビルド

## 参考

- [Juman++v2をWindowsでビルドする - TadaoYamaokaの日記](https://tadaoyamaoka.hatenablog.com/entry/2019/07/26/232720)
- [NLP準備運動 : 分かち書き環境の構築 Mecab , Juman++ver2 - Qiita](https://qiita.com/yosh_s/items/9aa42a15b50382cce266)

## Visual Studio のインストール

1. Visual Studio Community 2017 のインストーラをダウンロードする。
    - [Downloads - My Visual Studio](https://my.visualstudio.com/Downloads?q=visual%20studio%202017)
1. インストーラを起動する。
1. 「ユニバーサル Windows プラットフォーム開発」と「C++ によるデスクトップ開発」を選択してインストール。

## JUMAN++ のソースの取得

1. GitHub の `Releases` を開く。
    - [Releases · ku-nlp/jumanpp](https://github.com/ku-nlp/jumanpp/releases)
1. `2.0.0-rc3` の `Assets` を展開する。
1. `jumanpp-2.0.0-rc3.tar.xz` をダウンロードして展開する。

## ビルド

展開したディレクトリに入って、以下のコマンドを実行する。

```
mkdir cmake-build-dir
cd cmake-build-dir
cmake -G "Visual Studio 15 2017 Win64" ..
MSBuild jumanpp.sln /t:build /p:Configuration=RelWithDebInfo;Platform="x64"
```

## Config

展開したディレクトリ直下の `model` ディレクトリで以下の操作をする。
- `jumandic.conf.in` を `jumandic.conf` にリネームする。
- `jumandic.conf` を編集して、1行目の "=" 以降を同じディレクトリにある `jumandic.jppmdl` のフルパスにする。

## 動作確認

展開したディレクトリ\cmake-build-dir\src\jumandic\RelWithDebInfo へ移動する。
- そこに `jumanpp_v2.exe` がある。

以下のようにコマンドを実行する。

```
chcp 65001
echo 形態素解析したい文字列 | jumanpp_v2 --config=..\..\..\..\model\jumandic.conf
```

## どこからでも実行可能にする

1. `C:\ProgramData\jumanpp` フォルダを作り、そこへ動作確認した `juman_v2.exe` をコピーする。
    - パスにスペースを含むと上手く行かなかったので、`Program Files` フォルダは使わない。
1. `model` サブディレクトリを作って、そこへ `jumandic.conf` と `jumandic.jppmdl` をコピーする。
1. コピーした `jumandic.conf` を編集して、1行目の "=" 以降をコピーした `jumandic.jppmdl` のフルパスにする。
    ```
    --model=C:\ProgramData\jumanpp\model\jumandic.jppmdl
    ```
1. `juman_v2.exe` と同じディレクトリに `jumanpp.bat` を作る。
    ```
    jumanpp
    ├─ model
    │   ├─ jumandic.conf    # コピー&編集したファイル
    │   └─ jumandic.jppmdl  # コピーしたファイル
    │   
    ├─ jumanpp.bat          # 新規作成したファイル
    └─ jumanpp_v2.exe       # コピーしたファイル
    ```
1. `jumanpp.bat` に以下の内容を書く。
    ```
    @echo off
    jumanpp_v2 --config=C:\ProgramData\jumanpp\model\jumandic.conf %*
    ```
1. システムの Path に `C:\ProgramData\jumanpp` を追加する。

### 動作確認

適当なディレクトリから以下を実行する。
```
chcp 65001
echo 形態素解析したい文字列 | jumanpp
```

## Python から使う

`pyknp` が .bat ファイルをコマンドとして認識しないので、Juman のインスタンスを作る時、以下のようにする。

```python
juman = Juman(command='jumanpp_v2',
    option='--config=C:\ProgramData\jumanpp\model\jumandic.conf')
```
