import re
from pyknp import Juman


class JumanPsc(Juman):
    '''JUMAN++ を台本解析用に拡張したサブクラス

    JUMAN++ でエラーになる文字列を極力エラーにならないよう形態素解析する。
    '''
    
    # 無効な文字
    invalid_chars = ['\x1a']
    
    # 文末文字のパターン
    end_pattern = r'[。？?！!]'
    
    def juman_lines(self, input_str):
        '''形態素解析するメソッドのオーバーライド
        '''
        
        # 無効な文字を削除する。
        for c in JumanPsc.invalid_chars:
            input_str = input_str.replace(c, '')
        
        # 連続しない半角スペースを全角スペースにする
        input_str = re.sub(r'(?<!\s) (?!\s)', '　', input_str)
        
        # 空白文字の直後に小さい「つ」があったら、空白文字と「っ」の間で分割
        matchObj = re.search(r'\sっ', input_str)
        if matchObj:
            # 空白文字までと「っ」以降に分ける。
            s1 = input_str[:matchObj.start() + 1]
            s2 = input_str[matchObj.start() + 1:]
            
            # それぞれ形態素解析して、結果をつなげて返す。
            return self.juman_lines(s1) + self.juman_lines(s2)
        
        # 4096バイトを超えるなら、文末文字 (「。」等) で分割して形態素解析する。
        if len(input_str.encode()) > 4096:
            # 文末文字を探す。
            matchObj = re.search(JumanPsc.end_pattern, input_str)
            
            # 見つかったら分割して形態素解析してつなげて返す。
            if matchObj:
                s1 = input_str[:matchObj.start() + 1]
                s2 = input_str[matchObj.start() + 1:]
                return self.juman_lines(s1) + self.juman_lines(s2)
        
        # 分割処理しない (できない) 場合は継承元に渡す。
        return super().juman_lines(input_str)
