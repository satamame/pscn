'''テキストファイルが形態素解析可能か調べるためのモジュール
'''

import os
from datetime import datetime


def mrph_test_file(juman, file):
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


def mrph_test_dir(juman=None, input_dir=None, log_file=None):
    '''ディレクトリ内のファイルが形態素解析可能か調べる
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    input_dir: str
        調べるファイルが入っているディレクトリのパス
    log_file: str
        出力するログ・ファイルのパス
    '''
    
    # 出力ファイルをクリア
    if os.path.exists(log_file):
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
        
        for error in mrph_test_file(juman, inf):
            print(error)
            outf.write(error + '\n')
            err_count += 1
        
        # 出力ファイルを閉じる
        outf.close()
    
    print('Done.')
    print(f'{err_count} error(s) found.')
