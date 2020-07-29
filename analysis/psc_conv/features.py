'''台本ファイルから各行の特徴量を作るためのモジュール
'''

import os
import re
from . import MrphMatch, MRPH_MTCH_PTN

# パターンマッチングに使うパターン名 (とりあえず全部)
ptn_ids = tuple(MRPH_MTCH_PTN.keys())

# features_in_file() で作った特徴量の取り出し順
ft_keys = ptn_ids + (       # パターンマッチング
    'symbol_follows',       # パターンの後続単語がセリフっぽい記号か
    'interj_follows',       # パターンの後続単語が感動詞か
    'is_first_line',        # 最初の行か
    'is_last_line',         # 最後の行か
    'is_empty',             # 空または空白文字のみか
    'ends_w_bracket',       # 最後が '」'か
    'sentence_ends',        # 最後が文末文字 (。？?！!) か
    'states_charsheadline', # 「登場人物」を含むか
    'leading_spc',          # 行頭の空白文字の数
    'leading_spc_delta',    # 行頭の空白文字の数の増減
    'prev_is_empty',        # 前の行が空または空白文字のみか
    'prev_ends_w_bracket',  # 前の行の最後が '」'か
    'prev_sentence_ends',   # 前の行の最後が文末文字 (。？?！!) か
    'ptn_line_count',       # この行と同じパターンにマッチした行数
    'str_line_count',       # この行と同じ文字列にパターンマッチした行数
    'spc_line_count',       # この行と行頭の空白の数が同じ行の数
    'bracket_line_rate',    # ファイル全体の '「' を含む行の割合
)


def params_in_line(juman, line):
    '''行からパラメタを取り出す
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    line: str
        対象となる行の文字列
    
    Returns
    -------
    params: dict
        line から取り出したパラメタ
    '''
    
    params = {}
    mrphs = juman.analysis(line).mrph_list()
    mrph_match = MrphMatch(mrphs)
    
    # パターンマッチングパラメタを作る
    matched = False
    
    # パラメタの初期値
    matched_str = ''
    succeeding_mrph = None
    
    for ptn in ptn_ids:
        # 2つ以上のパターンにマッチしないようにする
        if matched:
            params[ptn] = False
            continue
        
        # マッチングする
        mrph_ptn = MRPH_MTCH_PTN[ptn]
        match_result = mrph_match.match(**mrph_ptn)
        
        # マッチしたかどうかをパラメタにする (キーはパターン番号)
        params[ptn] = match_result.matched
        
        # マッチしなかったら次のパターンへ
        if not match_result.matched:
            continue
        
        # マッチした場合
        matched = True
        
        # マッチした部分の文字列を取っておく
        matched_str = match_result.matched_str
        
        # 後続単語を取っておく
        if len(mrphs) > match_result.matched_count:
            succeeding_mrph = mrphs[match_result.matched_count]
    
    params['matched_str'] = matched_str
    params['succeeding_mrph'] = succeeding_mrph
    
    if succeeding_mrph:
        # 後続単語がセリフっぽい記号か
        symbol_follows = succeeding_mrph.midasi in ['…', '・', '！', '!']
        params['symbol_follows'] = symbol_follows
        # 後続単語が感動詞か
        interj_follows = succeeding_mrph.hinsi == '感動詞'
        params['interj_follows'] = interj_follows
    else:
        params['symbol_follows'] = False
        params['interj_follows'] = False
    
    # 空行か
    params['is_empty'] = not line.strip()
    
    # 行頭の空白文字の数
    match_result = mrph_match.match((MrphMatch.match_spaces,))
    params['leading_spc'] = match_result.matched_count
    
    # 最後が '」'か
    if len(mrphs) > 0:
        params['ends_w_bracket'] = (mrphs[-1].genkei == '」')
    else:
        params['ends_w_bracket'] = False
    
    # 最後が文末文字か
    if len(mrphs) > 0:
        params['sentence_ends'] = (
            mrphs[-1].midasi in ['。', '？', '?', '！', '!'])
    else:
        params['sentence_ends'] = False
    
    # 「登場人物」を含むか
    params['states_charsheadline'] = ('登場人物' in line)
    
    # '「' を含むか
    params['has_bracket'] = ('「' in line)
    
    return params


def features_in_lines(juman, lines, normalize=False):
    '''台本の各行の特徴量を取り出す
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    lines : list
        行 (str) のリスト
    normalize : bool
        正規化するかどうか
    
    Returns
    -------
    line_features : list
        特徴量の辞書の、行数分のリスト
    '''

    # 行ごとの特徴量
    line_features = []
    # 行ごとのパラメタ
    line_params = []
    
    # 最後に処理した行が空行か
    last_is_empty = True
    # 最後に処理した行の最後が '」' か
    last_ends_w_bracket = False
    # 最後に処理した行の最後が文末文字 (。？?！!) か
    last_sentence_ends = True
    # 最後に処理した行の行頭の空白文字数
    last_leading_spc = 0
    
    # パターンごとのマッチした行数
    ptn_line_count = {}
    # 文字列ごとのマッチした行数
    str_line_count = {}
    # 行頭の空白の数ごとの行数
    spc_line_count = {}
    # '「' を含む行の数
    bracket_line_count = 0
    
    for i, l in enumerate(lines):
        line = l.rstrip()
        params = params_in_line(juman, line)
        line_params.append(params)
        
        feature = {}
        
        # パラメタのうち、そのまま特徴量となるものを、まずは追加
        
        # パターンマッチング
        for ptn in ptn_ids:
            feature[ptn] = int(params[ptn])
        
        # パターンの後続単語がセリフっぽい記号か
        feature['symbol_follows'] = int(params['symbol_follows'])
        
        # パターンの後続単語が感動詞か
        feature['interj_follows'] = int(params['interj_follows'])
        
        # 最初の行か
        feature['is_first_line'] = int(i == 0)
        
        # 最後の行か
        feature['is_last_line'] = '0'  # ループを出てからセットし直す
        
        # 空または空白文字のみか
        feature['is_empty'] = int(params['is_empty'])
        
        # 最後が '」'か
        feature['ends_w_bracket'] = int(params['ends_w_bracket'])
        
        # 最後が文末文字 (。？?！!) か
        feature['sentence_ends'] = int(params['sentence_ends'])
        
        # 「登場人物」を含むか
        feature['states_charsheadline'] = int(
            params['states_charsheadline'])
        
        # 行頭の空白文字の数
        leading_spc = params['leading_spc']
        # 正規化するなら、10で割って最大値1.0で切り捨て
        if normalize:
            leading_spc = min(leading_spc / 10, 1.0)
        feature['leading_spc'] = leading_spc
        
        # 行頭の空白文字の数の増減
        if i == 0:
            delta = 0
        else:
            delta = params['leading_spc'] - last_leading_spc
        feature['leading_spc_delta'] = delta
        last_leading_spc = params['leading_spc']
        
        # 前の行が空行か
        feature['prev_is_empty'] = int(last_is_empty)
        last_is_empty = params['is_empty']
        
        # 前の行の最後が '」'か
        feature['prev_ends_w_bracket'] = int(last_ends_w_bracket)
        last_ends_w_bracket = params['ends_w_bracket']
        
        # 前の行の最後が文末文字 (。？?！!) か
        feature['prev_sentence_ends'] = int(last_sentence_ends)
        last_sentence_ends = params['sentence_ends']
        
        # ここまでの特徴量を、行ごとの特徴量のリストに追加
        line_features.append(feature)
        
        # ファイル全体の集計用の辞書を更新する
        
        # パターンごとのマッチした行数
        for ptn in [p for p in ptn_ids if feature[p]]:
            if ptn in ptn_line_count.keys():
                ptn_line_count[ptn] += 1
            else:
                ptn_line_count[ptn] = 1
        
        # 文字列ごとのマッチした行数
        matched_str = params['matched_str']
        if matched_str in str_line_count.keys():
            str_line_count[matched_str] += 1
        else:
            str_line_count[matched_str] = 1
        
        # 行頭の空白の数ごとの行数 (キーは正規化前の値)
        leading_spc = params['leading_spc']
        if leading_spc in spc_line_count.keys():
            spc_line_count[leading_spc] += 1
        else:
            spc_line_count[leading_spc] = 1
    
        # ファイル全体の '「' を含む行の数をカウント
        if params['has_bracket']:
            bracket_line_count += 1

    # ファイル全体の行数
    line_cnt = len(line_features)
    
    # ファイル全体の '「' を含む行の割合
    bracket_line_rate = bracket_line_count / line_cnt
    
    # 最後の行に is_last_line をセットする
    line_features[line_cnt - 1]['is_last_line'] = '1'
    
    # ファイル全体で集計したデータから特徴量を追加する
    for i, lf in enumerate(line_features):
        # この行と同じパターンにマッチした行数
        matched_ptn = ''
        for ptn in ptn_ids:
            if lf[ptn] == 1:
                matched_ptn = ptn
                break
        if matched_ptn in ptn_line_count.keys():
            lf['ptn_line_count'] = ptn_line_count[matched_ptn]
            # 正規化するなら、全行数で割る
            if normalize:
                lf['ptn_line_count'] /= line_cnt
        else:
            lf['ptn_line_count'] = 0
        
        # この行と同じ文字列にパターンマッチした行数
        matched_str = line_params[i]['matched_str']
        if (matched_str
                and matched_str in str_line_count.keys()):
            lf['str_line_count'] = str_line_count[matched_str]
            # 正規化するなら、全行数で割る
            if normalize:
                lf['str_line_count'] /= line_cnt
        else:
            lf['str_line_count'] = 0
        
        # この行と行頭の空白の数が同じ行の数
        leading_spc = line_params[i]['leading_spc']
        if leading_spc in spc_line_count.keys():
            lf['spc_line_count'] = spc_line_count[leading_spc]
            # 正規化するなら、全行数で割る
            if normalize:
                lf['spc_line_count'] /= line_cnt
        else:
            lf['spc_line_count'] = 0
        
        # ファイル全体の '「' を含む行の割合
        lf['bracket_line_rate'] = bracket_line_rate
    
    return line_features


def features_in_file(juman, fname, normalize=False):
    '''ファイルから行ごとの特徴量を取り出す
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    fname : str
        ファイル名
    normalize : bool
        正規化するかどうか
    
    Returns
    -------
    line_features : list
        特徴量の辞書の、行数分のリスト
    '''
    
    with open(fname, encoding='utf_8_sig') as f:
        lines = [l for l in f.readlines()]
    return features_in_lines(juman, lines, normalize=normalize)


def make_features(juman, input_dir, output_dir, targets_dir,
        empty_output_dir=True, normalize=False):
    '''入力ディレクトリ内のファイルから特徴量を抽出する
    
    特徴量を作るのに、前の行のラベルが必要になるので、教師ラベルも読み込む
    
    Parameters
    ----------
    juman: JumanPsc
        形態素解析に使う JumanPsc のインスタンス
    input_dir: str
        入力ディレクトリのパス
    output_dir: str
        出力ディレクトリのパス
    targets_dir: str
        教師ラベルファイルのディレクトリのパス
    empty_output_dir: bool
        出力ディレクトリを最初に空にするか
    normalize: bool
        数値の特徴量を正規化するか
    '''
    # 出力ディレクトリがなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 出力ディレクトリを空にする
    if empty_output_dir:
        for entry in os.scandir(path=output_dir):
            if entry.is_file():
                os.remove(entry)

    # 入力ディレクトリ内のファイルについて、特徴量を作成
    for entry in os.scandir(path=input_dir):
        if not entry.is_file():
            continue
        
        # ファイル名から拡張子を削除したもの
        fname = os.path.basename(entry).split('.', 1)[0]
        
        # 教師ラベルを取得しておく
        target_f = os.path.join(targets_dir, fname + '.txt')
        with open(target_f, encoding='utf_8_sig') as f:
            # 各行の空白文字以降を切り捨てた文字列を取得
            lines = f.readlines()
        labels = [re.split(r'\s', l, 1)[0] for l in lines]
        
        # 出力
        out_f = os.path.join(output_dir, fname + '.csv')
        with open(out_f, 'w') as f:
            # 登場人物見出しが出た後か
            charsheadline_used = '0'
            # 柱 (レベル1) が出た後か
            h1_used = '0'
            # ト書きが出た後か
            direction_used = '0'
            # セリフが出た後か
            dialogue_used = '0'
            
            features = features_in_file(juman, entry, normalize=normalize)
            for i, ft in enumerate(features):
                # 特徴量から取り出し順に値を取り出したリスト
                vals = [str(ft[k]) for k in ft_keys]
                
                # 前の行の教師ラベルを使って特徴量を追加
                prev_label = labels[i - 1] if i > 0 else ''
                vals.append(str(int(prev_label == 'CHARACTER')))
                vals.append(str(int(prev_label == 'CHARACTER_CONTINUED')))
                vals.append(str(int(prev_label == 'DIRECTION')))
                vals.append(str(int(prev_label == 'DIRECTION_CONTINUED')))
                vals.append(str(int(prev_label == 'DIALOGUE')))
                vals.append(str(int(prev_label == 'DIALOGUE_CONTINUED')))
                vals.append(str(int(prev_label == 'COMMENT')))
                vals.append(str(int(prev_label == 'COMMENT_CONTINUED')))
                
                # ここまでの教師ラベルを使って特徴量を追加
                vals.append(charsheadline_used)
                vals.append(h1_used)
                vals.append(direction_used)
                vals.append(dialogue_used)
                
                # カンマ区切りにして出力
                l = ','.join(vals)
                f.write(l + '\n')
                
                # 次ループ以降のための特徴量の更新
                if labels[i] == 'CHARSHEADLINE':
                    charsheadline_used = '1'
                if labels[i] == 'H1':
                    h1_used = '1'
                if labels[i] == 'DIRECTION':
                    direction_used = '1'
                if labels[i] == 'DIALOGUE':
                    dialogue_used = '1'
        
        print(fname)

    print('Done.')
