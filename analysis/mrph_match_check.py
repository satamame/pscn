'''形態素列マッチングを単品で実行して確認する
'''

from psc_conv import JumanPsc, MrphMatch
from juman_settings import *


juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)

line = '  　男「ようこそ皆さん、私の名前はジョニー。今日は私のリサイタルショーにおいで下さってありがとうございます。今宵、しばし皆様の時間を拝借して、私の歌をお聞きください。では、まずはこの歌から」'
# line = '    男  '

mrphs = juman.analysis(line).mrph_list()

mrph_match = MrphMatch(mrphs)

result = mrph_match.match(
    ptn = [
        MrphMatch.match_spaces,
        MrphMatch.match_noun,
        MrphMatch.match_left_bracket,
    ]
)

print(f'マッチ判定: {result.matched}')
print(f'マッチ範囲文字列: {result.matched_str}')
print(f'マッチ範囲内形態素数: {result.matched_count}')
if len(mrphs) >= result.matched_count:
    print(f'後続単語: {mrphs[result.matched_count].midasi}')
