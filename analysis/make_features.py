'''台本ファイルから各行の特徴量を作る
'''

#%%
import os
from juman_psc import JumanPsc
from mrph_match import MrphMatch, MRPH_MTCH_PTN

# 入力ディレクトリ (ディレクトリごと処理する場合)
input_dir = 'line_start_samples'

# 入力ファイル (ファイル単位で処理する場合)
input_file = 'script_samples_2/000001.txt'

# 出力ディレクトリ
output_dir = 'line_start_features'

#%%
# 相対パスを絶対パスに
input_dir = os.path.join(os.path.dirname(__file__), input_dir)
input_file = os.path.join(os.path.dirname(__file__), input_file)
output_dir = os.path.join(os.path.dirname(__file__), output_dir)

juman = JumanPsc()


#%%
def params_in_line(line):
    '''行からパラメタを取り出す'''
    
    params = {}
    mrphs = juman.analysis(line).mrph_list()
    mrph_match = MrphMatch(mrphs)
    
    # パターンマッチング
    ptns = ('0001', '0002', '0003', '0004', '0005')
    # パラメタの初期値
    matched_str = ''
    succeeding_mrph = None
    
    for ptn in ptns:
        mrph_ptn = MRPH_MTCH_PTN[ptn]
        match_result = mrph_match.match(mrph_ptn)
        
        # マッチしたかどうかをパラメタにする (キーはパターン番号)
        params[ptn] = match_result.matched
        # マッチしなかったら次のパターンへ
        if not match_result.matched:
            continue
        
        # マッチした部分の文字列を取っておく
        matched_str = match_result.matched_str
        
        # 後続単語を取っておく
        if len(mrphs) >= match_result.matched_count:
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
        params['symbol_follows'] = None
        params['interj_follows'] = None
    
    # 行頭の空白文字の数
    match_result = mrph_match.match((MrphMatch.match_spaces,))
    params['leading_spc'] = match_result.matched_count
    
    return params


# %%
def features_in_file(fname, normalize=False):
    '''ファイルから行ごとの特徴量を取り出す
    
    Parameters
    ----------
    fname : str
        ファイル名
    normalize : bool
        正規化するかどうか
    
    Returns
    -------
    line_features : list
        特徴量の辞書の、行数分のリスト
    '''
    
    # パターン名
    ptns = ('0001', '0002', '0003', '0004', '0005')
    
    # 行ごとの特徴量
    line_features = []
    # 行ごとのパラメタ
    line_params = []
    # パターンごとのマッチした行数
    ptn_line_count = {}
    # 文字列ごとのマッチした行数
    str_line_count = {}
    # 行頭の空白の数ごとの行数
    spc_line_count = {}
    
    with open(fname, encoding='utf_8_sig') as f:
        for i, l in enumerate(f.readlines()):
            line = l.rstrip()
            param = params_in_line(line)
            line_params.append(param)
            
            feature = {}
            
            # パラメタのうち、そのまま特徴量となるものを、まずは追加
            
            # パターンマッチング
            for ptn in ptns:
                feature[ptn] = 1 if param[ptn] else 0
            
            # パターンの後続単語がセリフっぽい記号か
            feature['symbol_follows'] = 1 if param['symbol_follows'] else 0
            
            # パターンの後続単語が感動詞か
            feature['interj_follows'] = 1 if param['interj_follows'] else 0
            
            # 行頭の空白文字の数
            leading_spc = param['leading_spc']
            # 正規化するなら、10で割って最大値1.0で切り捨て
            if normalize:
                leading_spc = min(leading_spc / 10, 1.0)
            feature['leading_spc'] = leading_spc
            
            # 行ごとの特徴量のリストに追加
            line_features.append(feature)
            
            # ファイル全体の集計用の辞書を更新する
            
            # パターンごとのマッチした行数
            for ptn in [p for p in ptns if feature[p]]:
                if ptn in ptn_line_count.keys():
                    ptn_line_count[ptn] += 1
                else:
                    ptn_line_count[ptn] = 1
            
            # 文字列ごとのマッチした行数
            matched_str = param['matched_str']
            if matched_str in str_line_count.keys():
                str_line_count[matched_str] += 1
            else:
                str_line_count[matched_str] = 1
            
            # 行頭の空白の数ごとの行数 (キーは正規化前の値)
            leading_spc = param['leading_spc']
            if leading_spc in spc_line_count.keys():
                spc_line_count[leading_spc] += 1
            else:
                spc_line_count[leading_spc] = 1
    
    # ファイル全体の行数
    line_cnt = len(line_features)
    
    # ファイル全体で集計したデータから特徴量を追加する
    for i, lf in enumerate(line_features):
        # この行と同じパターンにマッチした行数
        matched_ptn = ''
        for ptn in ptns:
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
    
    return line_features


# %%
file_features = features_in_file(input_file, normalize=True)


# %%
