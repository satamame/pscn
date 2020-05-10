'''形態素列マッチングを単品で実行して確認するためのスクリプト。
'''

#%%
from juman_psc import JumanPsc
from mrph_match import MrphMatch

juman = JumanPsc()

#%%
line = '  　男「ようこそ皆さん、私の名前はジョニー。今日は私のリサイタルショーにおいで下さってありがとうございます。今宵、しばし皆様の時間を拝借して、私の歌をお聞きください。では、まずはこの歌から」'
# line = '    男  '

mrphs = juman.analysis(line).mrph_list()

mrph_match = MrphMatch(mrphs)

result = mrph_match.match(
    ptn = [
        MrphMatch.match_spaces,
        MrphMatch.match_noun,
        MrphMatch.match_left_corner_bracket,
    ]
)

print(f'マッチ判定: {result.matched}')
print(f'マッチ範囲文字列: {result.matched_str}')
print(f'マッチ範囲内形態素数: {result.matched_count}')
if len(mrphs) >= result.matched_count:
    print(f'後続単語: {mrphs[result.matched_count].midasi}')


# %%
