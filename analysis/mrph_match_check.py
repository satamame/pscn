'''形態素列マッチングを単品で実行して確認する
'''

from psc_conv import JumanPsc, MrphMatch, MRPH_MTCH_PTN
from juman_settings import *


juman = JumanPsc(command=JUMAN_COMMAND, option=JUMAN_OPTION)

# line = '  　男「ようこそ皆さん、私の名前はジョニー。今日は私のリサイタルショーにおいで下さってありがとうございます。今宵、しばし皆様の時間を拝借して、私の歌をお聞きください。では、まずはこの歌から」'
line = '女「男　 イヌ'

mrphs = juman.analysis(line).mrph_list()

mrph_match = MrphMatch(mrphs)

# kwargs = {
#     'ptn': (
#         MrphMatch.match_spaces,
#         MrphMatch.match_noun,
#         MrphMatch.match_left_bracket,
#     ),
#     'idx': 0
# }

kwargs = MRPH_MTCH_PTN['0002']

result = mrph_match.match(**kwargs)

print(f'マッチ判定: {result.matched}')
print(f'マッチ範囲文字列: "{result.matched_str}"')
print(f'マッチ範囲内形態素数: {result.matched_count}')

idx = kwargs['idx']

if idx >= 0:
    idx += result.matched_count
else:
    idx += len(mrphs) - result.matched_count
if len(mrphs) > idx >= 0:
    print(f'次の単語: "{mrphs[idx].midasi}"')
else:
    print('次の単語: なし')
