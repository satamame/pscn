'''JumanPsc の形態素解析を単品の文字列で試す
'''

from psc_parse import JumanPsc
from juman_settings import JUMAN_COMMAND, JUMAN_OPTION


juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)

s = '今日もいい天気'

try:
    mrphs = juman.analysis(s)

    for mrph in mrphs:
        print(f'"{mrph.midasi}"')              # 見出し
        print(f'  genkei:   {mrph.genkei}')    # 原形
        print(f'  hinsi:    {mrph.hinsi}')     # 品詞
        print(f'  bunrui:   {mrph.bunrui}')    # 品詞細分類
        print(f'  katuyou2: {mrph.katuyou2}')  # 活用形

except Exception as e:
    print(e)
