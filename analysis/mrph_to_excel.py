'''サンプルファイルの各行を形態素解析して表を作る。
'''

import os
import pandas as pd
import openpyxl
from psc_parse import JumanPsc
from juman_settings import *


# 入力ディレクトリ
input_dir = 'line_start_samples'

# 出力ファイル名
output_file = 'line_start_analysis.xlsx'

# 先頭から何単語まで解析するか
word_count = 10

# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
output_file = os.path.join(os.path.dirname(__file__), output_file)

juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)


def mrph_line(line, word_count=0):
    '''与えられた文の先頭を形態素解析して返すジェネレータ
    
    Parameters
    ----------
    count: int
        解析対象とする先頭からの単語数
    
    Returns
    -------
    yield: dict
        見出し, 原形, 品詞, 品詞細分類, 活用形
    '''
    
    # 形態素解析
    result = juman.analysis(line).mrph_list()
    
    # count の指定がなければ全単語を対象とする
    count = len(result) if word_count == 0 else word_count
    
    # 先頭から count 個の単語について、結果を返す
    for mrph in result:
        
        # print("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
        #         % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
        
        yield {
            'midasi': mrph.midasi,        # 見出し
            'genkei': mrph.genkei,        # 原形
            'hinsi': mrph.hinsi,          # 品詞
            'bunrui': mrph.bunrui,        # 品詞細分類
            'katuyou2': mrph.katuyou2,    # 活用形
        }
        
        count -= 1
        if count < 1:
            break


def mrph_file(file, word_count=0):
    '''テキストファイル内の各行を形態素解析して返すジェネレータ
    
    Parameters
    ----------
    file: str
        ファイル名
    
    Returns
    -------
    yield: dic
        行の原文, 形態素解析の結果
    '''
    with open(file, encoding='utf-8') as f:
        for l in f.readlines():
            line = l.rstrip()
            yield{
                'line': line,
                'mrph': list(mrph_line(line, word_count))
            }


# 解析済みのデータを溜めていくリスト
lines = []

# 入力ディレクトリの内容
for entry in os.scandir(path=input_dir):
    # ファイルでなければスキップ
    if not entry.is_file():
        continue
    
    # ファイル名
    file = os.path.join(input_dir, entry.name)
    
    # テキストファイルでなければスキップ
    if not os.path.splitext(file)[-1] == '.txt':
        continue
    
    for l in mrph_file(file, word_count):
        line = []
        # 各行の最初の要素は原文
        line.append(l['line'])
        # その後に解析結果が続く
        for m in l['mrph']:
            mrph = []
            # 各解析結果は (見出し, 原形, 品詞, 品詞細分類, 活用形) の改行区切り
            mrph.append(m['midasi'])
            mrph.append(m['genkei'])
            mrph.append(m['hinsi'])
            mrph.append(m['bunrui'])
            mrph.append(m['katuyou2'])
            line.append('\n'.join(mrph))
        
        # 解析済みのデータをリストに追加
        lines.append(line)


# Excel に保存

df = pd.DataFrame(lines)
df.to_excel(output_file)
print('Done.')
