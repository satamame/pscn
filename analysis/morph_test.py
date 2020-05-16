'''複数ファイルを、形態素解析できるか一括でテストする。
'''

#%%
import os
from datetime import datetime
from juman_psc import JumanPsc


# 入力ディレクトリ
input_dir = 'script_rawdata'

# ログ出力ファイル
log_file = 'morph_test.log'

# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
log_file = os.path.join(os.path.dirname(__file__), log_file)

juman = JumanPsc()

#%%
def morph_file(file):
    '''テキストファイル内の各行について形態素解析エラーを返すジェネレータ
    
    Parameters
    ----------
    file: str
        ファイル名
    
    Returns
    -------
    yield: str
        形態素解析できなかった行についてのエラー
    '''
    
    with open(file, encoding='utf_8_sig') as f:
        for i, l in enumerate(f.readlines()):
            line = l.rstrip()
            
            try:
                mrphs = juman.analysis(line).mrph_list()
            except Exception as e:
                yield f'Error: Line {i + 1} cannot be analyzed.'


#%%
# 出力ファイルをクリア
if os._exists(log_file):
    os.remove(log_file)

# エラーカウント
err_count = 0

# 入力ディレクトリ内をループ
for entry in os.scandir(path=input_dir):
    
    # ファイルでなければスキップ
    if not entry.is_file():
        continue
    
    # 入力ファイル名
    inf = os.path.join(input_dir, entry.name)
    
    # テキストファイルでなければスキップ
    if os.path.splitext(inf)[-1] != '.txt':
        continue
    
    # 出力ファイルを追記モードでオープン
    outf = open(log_file, mode='a', encoding='utf-8')
    
    # ファイルごとの処理開始ログ
    log = datetime.now().strftime('%m-%d %H:%M:%S') + ' ' + entry.name
    print(log)
    outf.write(log + '\n')
    
    for error in morph_file(inf):
        print(error)
        outf.write(error + '\n')
        err_count += 1
    
    # 出力ファイルを閉じる
    outf.close()

print('Done.')
print(f'{err_count} error(s) found.')


# %%
