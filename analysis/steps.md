# 手順メモ

## JUMAN のインストール

- http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN
- JUMAN Ver.7.0 (Windows 64bit版) をダウンロードする。
- インストーラを実行してインストール。
- `C:\Program Files\juman` にパスを通しておく。
    - VSCode の Python Interactive で実行する時、パスを通してから VSCode を起動する。

- JUMAN++ は今のところ Linux のみ
    - http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN++

## PyKNP のインストール

- https://pyknp.readthedocs.io/en/latest/

```
> pipenv install pyknp
```

## PyKNP を Windows 向けに修正

**JUMAN++ を使うなら、この修正はしてはいけない**

- (参考) http://chuckischarles.hatenablog.com/entry/2019/09/12/150505
- PyKNP version: 0.4.1
- pyknp/juman/process.py
- class Subprocess

```python
    def query(self, sentence, pattern, encoding="ms932"): # この行
        assert(isinstance(sentence, six.text_type))
        self.process.stdin.write(sentence.encode(encoding)+six.b('\n')) # この行
        self.process.stdin.flush()
        result = ""
        while True:
            line = self.stdouterr.readline().rstrip().decode(encoding) # この行
            if re.search(pattern, line):
                break
            result = "%s%s\n" % (result, line)
        return result
```

## JUMAN++ を使う場合

`steps_jumanpp.md` を参照。
