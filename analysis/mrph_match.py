'''形態素列のパターンマッチングをするクラスのモジュール
'''

class MrphMatch(object):
    '''形態素列のパターンマッチングをするクラス
    '''
    
    def __init__(self, mrphs):
        '''コンストラクタ
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        '''
        
        self.mrphs = mrphs
    
    def match(self, ptn=None, idx=0):
        '''形態素列の指定位置でパターンマッチングする
        
        Parameters
        ----------
        ptn : list
            マッチングに使うメソッドのリスト
        idx : int
            マッチングを開始する位置
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        if ptn is None:
            ptn = []
        
        # 指定位置以降をマッチングの対象にする
        mrphs = self.mrphs[idx:]
        
        matched = True
        matched_str = ''
        matched_count = 0
        
        for cond in ptn:
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
        
        matched_str = matched_str.replace('\ ', ' ') # JUMAN++ では不要
        return MrphMatchResult(matched, matched_str, matched_count)
    
    @classmethod
    def match_single(cls, mrphs, cond):
        '''形態素列の先頭の1個が条件にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        cond : function
            マッチングをするメソッド
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        if len(mrphs) > 0 and cond(mrphs[0]):
            return MrphMatchResult(True, mrphs[0].midasi, 1)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_repeat(cls, mrphs, cond):
        '''形態素列の先頭の1個以上が条件にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        cond : function
            マッチングをするメソッド
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        matched = True
        matched_str = ''
        idx = 0
        
        while idx < len(mrphs):
            if cond(mrphs[idx]):
                matched_str += mrphs[idx].midasi
                idx += 1
            else:
                break
        
        if idx > 0:
            return MrphMatchResult(True, matched_str, idx)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_space(cls, mrphs):
        '''形態素列の先頭が空白文字1個にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.bunrui == '空白')
    
    @classmethod
    def match_spaces(cls, mrphs):
        '''形態素列の先頭が1個以上の連続する空白文字にマッチするか調べる
        '''
        return cls.match_repeat(mrphs, lambda mrph: mrph.bunrui == '空白')
    
    @classmethod
    def match_noun(cls, mrphs):
        '''形態素列の先頭の1個が名詞にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.hinsi == '名詞')
    
    @classmethod
    def match_nouns(cls, mrphs):
        '''形態素列の先頭が1個以上の連続する名詞にマッチするか調べる
        '''
        return cls.match_repeat(mrphs, lambda mrph: mrph.hinsi == '名詞')
    
    @classmethod
    def match_left_corner_bracket(cls, mrphs):
        '''形態素列の先頭の1個が左鉤括弧にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.genkei == '「')


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
            マッチした部分の元の文字列 (またはそれを全角にしたもの)
        matched_count : int
            マッチした部分の形態素の数
        '''
        
        self.matched = matched
        self.matched_str = matched_str
        self.matched_count = matched_count


# マッチングパターン集
MRPH_MTCH_PTN = {
    # (空白+) (名詞) "「"
    '0001' : (
        MrphMatch.match_spaces,
        MrphMatch.match_noun,
        MrphMatch.match_left_corner_bracket,
    ),

    # (名詞) "「"
    '0002' : (
        MrphMatch.match_noun,
        MrphMatch.match_left_corner_bracket,
    ),

    # (名詞+) (空白)
    '0003' : (
        MrphMatch.match_nouns,
        MrphMatch.match_space,
    ),

    # (名詞) (空白+)
    '0004' : (
        MrphMatch.match_noun,
        MrphMatch.match_spaces,
    ),

    # (空白) (名詞) (空白+)
    '0005' : (
        MrphMatch.match_space,
        MrphMatch.match_noun,
        MrphMatch.match_spaces,
    ),
}
