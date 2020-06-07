import unittest
from juman_psc import JumanPsc
from mrph_match import MrphMatch, MRPH_MTCH_PTN
from .juman_settings import *


class TestMatchSpace(unittest.TestCase):
    '''空白文字をマッチングする関数と、それを使った MrphMatch のテスト
    '''
    
    def test_single_space(self):
        '''文頭にある単品の空白文字をマッチングする
        '''
        
        juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
        
        s = ' '
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match((MrphMatch.match_space,))
        
        self.assertTrue(result.matched)
        self.assertEqual(result.matched_str, '　')
        self.assertEqual(result.matched_count, 1)
    
    def test_single_space_reverse(self):
        '''文末にある単品の空白文字をマッチングする
        '''
        
        juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
        
        s = 'ひとつ '
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match((MrphMatch.match_space,), -1)
        
        self.assertTrue(result.matched)
        self.assertEqual(result.matched_str, '　')
        self.assertEqual(result.matched_count, 1)
    
    def test_double_space(self):
        '''文頭にある連続する空白文字をマッチングする
        '''
        
        juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
        
        s = '  '
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match((MrphMatch.match_spaces,))
        
        self.assertTrue(result.matched)
        self.assertEqual(result.matched_str, '　　')
        self.assertEqual(result.matched_count, 2)
    
    def test_double_space_reverse(self):
        '''文末にある連続する空白文字をマッチングする
        '''
        
        juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
        
        s = 'ふたつ  '
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match((MrphMatch.match_spaces,), -1)
        
        self.assertTrue(result.matched)
        self.assertEqual(result.matched_str, '　　')
        self.assertEqual(result.matched_count, 2)


class TestMatchPattern(unittest.TestCase):
    '''MrphMatch を使って形態素列パターンをマッチングするテスト
    '''
    
    def test_pattern_0001(self):
        '''(空白+) (名詞) "「" で始まる文字列をマッチングする
        '''
        
        juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)
        
        s = ' 男「あ'
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match(**MRPH_MTCH_PTN['0001'])
        
        self.assertTrue(result.matched)
        self.assertEqual(result.matched_str, '　男「')
        self.assertEqual(result.matched_count, 3)
        
        s = '  男「あ'
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match(**MRPH_MTCH_PTN['0001'])
        
        self.assertTrue(result.matched)
        self.assertEqual(result.matched_str, '　　男「')
        self.assertEqual(result.matched_count, 4)
        
        s = '男「あ'
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match(**MRPH_MTCH_PTN['0001'])
        
        self.assertFalse(result.matched)
        self.assertEqual(result.matched_str, '')
        self.assertEqual(result.matched_count, 0)
        
        s = ' 男'
        mrph_match = MrphMatch(juman.analysis(s).mrph_list())
        result = mrph_match.match(**MRPH_MTCH_PTN['0001'])
        
        self.assertFalse(result.matched)
        self.assertEqual(result.matched_str, '')
        self.assertEqual(result.matched_count, 0)
