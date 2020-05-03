'''形態素列のパターンマッチングをするクラスのモジュール
'''

from pyknp import Juman


class MrphMatch(object):
    '''形態素列のパターンマッチングをするクラス
    '''
    
    def __init__(self, mrphs):
        '''コンストラクタ
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        matchings : list
            マッチングに使うメソッドのリスト
        '''
        
        self.mrphs = mrphs
    
    def match(self, idx=0, conds=None):
        '''形態素列の指定位置でパターンマッチングする
        
        Parameters
        ----------
        idx : int
            マッチングを開始する位置
        conds : list
            個々の形態素をマッチングをするメソッドのリスト
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        if conds is None:
            conds = []
        
        # 指定位置以降をマッチングの対象にする
        mrphs = self.mrphs[idx:]
        
        matched = True
        matched_str = ''
        matched_count = 0
        
        for cond in conds:
            result = cond(mrphs)
            if result.matched:
                matched_str += result.matched_str
                matched_count += result.matched_count
                mrphs = mrphs[result.matched_count:]
            else:
                matched = False
                matched_str = ''
                matched_count = 0
                break
        
        matched_str = matched_str.replace('\ ', ' ') # Juman 用
        return MrphMatchResult(matched, matched_str, matched_count)
    
    @classmethod
    def match_space(cls, mrphs):
        '''形態素列の先頭が空白文字1個にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        if mrphs[0].bunrui == '空白':
            return MrphMatchResult(True, mrphs[0].midasi, 1)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_spaces(cls, mrphs):
        '''形態素列の先頭が1個以上の連続する空白文字にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        matched = True
        matched_str = ''
        idx = 0
        
        while idx < len(mrphs):
            if mrphs[idx].bunrui == '空白':
                matched_str += mrphs[idx].midasi
                idx += 1
            else:
                break
        
        if idx > 0:
            return MrphMatchResult(True, matched_str, idx)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_single(cls, mrphs, cond):
        '''形態素列の先頭の1個が条件にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        cond : function
            マッチングをする関数
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        if cond(mrphs[0]):
            return MrphMatchResult(True, mrphs[0].midasi, 1)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_noun(cls, mrphs):
        '''形態素列の先頭の1個が名詞にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.hinsi == '名詞')


class MrphMatchResult(object):
    '''形態素列のパターンをマッチングした結果を表すオブジェクト
    '''
    
    def __init__(self, matched, matched_str, matched_count):
        '''コンストラクタ
        
        Parameters
        ----------
        matched : bool
            マッチしたか
        matched_str : str
            マッチした部分の元の文字列
        matched_count : int
            マッチした部分の形態素の数
        '''
        
        self.matched = matched
        self.matched_str = matched_str
        self.matched_count = matched_count
