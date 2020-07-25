'''形態素列のパターンマッチングをするためのモジュール
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
            負の数なら末尾からマッチングする
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        if ptn is None:
            ptn = []
        
        # 検索の向き
        direction = 1 if idx >= 0 else -1
        
        # マッチングの対象を切り取る
        if idx > 0:
            # 開始位置が1以上なら先頭を切り取る
            mrphs = self.mrphs[idx:]
        elif idx < -1:
            # 開始位置が-2以下なら末尾を切り取る
            mrphs = self.mrphs[:idx + 1]
        else:
            # 開始位置が0または-1なら切り取らない
            mrphs = self.mrphs
        
        matched = True
        matched_str = ''
        matched_count = 0
        
        for cond in ptn:
            result = cond(mrphs, direction)
            if result.matched:
                # 次の位置はマッチした形態素数 x 検索の向き
                idx = result.matched_count * direction
                
                if direction > 0:
                    matched_str += result.matched_str
                    mrphs = mrphs[idx:]
                else:
                    matched_str = result.matched_str + matched_str
                    mrphs = mrphs[:idx]
                
                matched_count += result.matched_count
            else:
                matched = False
                matched_str = ''
                matched_count = 0
                break
        
        matched_str = matched_str.replace('\ ', ' ') # JUMAN++ では不要
        return MrphMatchResult(matched, matched_str, matched_count)
    
    @classmethod
    def match_single(cls, mrphs, cond, direction=1):
        '''形態素列の先頭/末尾の1個が条件にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        cond : function
            マッチングをするメソッド
        direction : int
            1なら先頭、-1なら末尾を調べる
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        # 形態素列が空ならマッチしない
        if len(mrphs) < 1:
            return MrphMatchResult(False, '', 0)
        
        # マッチングの対象となる形態素
        mrph = mrphs[0] if direction > 0 else mrphs[-1]
        
        # マッチングして結果を返す
        if cond(mrph):
            return MrphMatchResult(True, mrph.midasi, 1)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_repeat(cls, mrphs, cond, direction=1):
        '''形態素列の先頭の1個以上が条件にマッチするか調べる
        
        Parameters
        ----------
        mrphs : list
            マッチングの対象となる形態素列
        cond : function
            マッチングをするメソッド
        direction : int
            1なら先頭、-1なら末尾から調べる
        
        Returns
        -------
        result : MrphMatchResult
            マッチングの結果
        '''
        
        matched = True
        matched_str = ''
        
        # idx は、direction が1なら先頭からの、-1なら末尾からの位置
        idx = 0
        
        while idx < len(mrphs):
            mrph = mrphs[idx] if direction > 0 else mrphs[-idx - 1]
            if cond(mrph):
                if direction > 0:
                    matched_str += mrph.midasi
                else:
                    matched_str = mrph.midasi + matched_str
                idx += 1
            else:
                break
        
        if idx > 0:
            return MrphMatchResult(True, matched_str, idx)
        else:
            return MrphMatchResult(False, '', 0)
    
    @classmethod
    def match_space(cls, mrphs, direction=1):
        '''形態素列の先頭が空白文字1個にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.bunrui == '空白',
            direction)
    
    @classmethod
    def match_spaces(cls, mrphs, direction=1):
        '''形態素列の先頭が1個以上の連続する空白文字にマッチするか調べる
        '''
        return cls.match_repeat(mrphs, lambda mrph: mrph.bunrui == '空白',
            direction)
    
    @classmethod
    def match_noun(cls, mrphs, direction=1):
        '''形態素列の先頭の1個が名詞にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.hinsi == '名詞',
            direction)
    
    @classmethod
    def match_nouns(cls, mrphs, direction=1):
        '''形態素列の先頭が1個以上の連続する名詞にマッチするか調べる
        '''
        return cls.match_repeat(mrphs, lambda mrph: mrph.hinsi == '名詞',
            direction)
    
    @classmethod
    def match_left_bracket(cls, mrphs, direction=1):
        '''形態素列の先頭の1個が左鉤括弧にマッチするか調べる
        '''
        return cls.match_single(mrphs, lambda mrph: mrph.genkei == '「',
            direction)


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


# TODO: パターンに、先頭からか末尾からかを含める

# マッチングパターン集
MRPH_MTCH_PTN = {
    # (空白+) (名詞) "「" で始まる
    '0001': {
        'ptn': (
            MrphMatch.match_spaces,
            MrphMatch.match_noun,
            MrphMatch.match_left_bracket,
        ),
        'idx': 0
    },

    # (名詞) "「" で始まる
    '0002': {
        'ptn': (
            MrphMatch.match_noun,
            MrphMatch.match_left_bracket,
        ),
        'idx': 0
    },

    # (名詞+) (空白+) "「" で始まる
    '0003': {
        'ptn': (
            MrphMatch.match_nouns,
            MrphMatch.match_spaces,
            MrphMatch.match_left_bracket,
        ),
        'idx': 0
    },

    # (名詞+) (空白) で始まる
    '0004': {
        'ptn': (
            MrphMatch.match_nouns,
            MrphMatch.match_space,
        ),
        'idx': 0
    },

    # (名詞) (空白+) で始まる
    '0005': {
        'ptn': (
            MrphMatch.match_noun,
            MrphMatch.match_spaces,
        ),
        'idx': 0
    },

    # (空白) (名詞) (空白+) で始まる
    '0006': {
        'ptn': (
            MrphMatch.match_space,
            MrphMatch.match_noun,
            MrphMatch.match_spaces,
        ),
        'idx': 0
    }
}
