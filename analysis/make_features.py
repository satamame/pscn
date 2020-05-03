'''台本ファイルから各行の特徴量を作る

現在のコードは、動作確認のため単品のマッチングだけしている。
'''

#%%
from juman_psc import JumanPsc
from mrph_match import MrphMatch, MrphMatchResult

# 入力ディレクトリ (ディレクトリごと処理する場合)
# input_dir = 'line_start_samples'

# 入力ファイル (ファイル単位で処理する場合)
input_file = 'line_start_samples/000001.txt'

# 出力ディレクトリ
output_dir = 'line_start_features'

#%%
juman = JumanPsc(command='jumanpp_v2',
    option='--config=C:\ProgramData\jumanpp\model\jumandic.conf')

#%%
line = '  　男「ようこそ皆さん、私の名前はジョニー。今日は私のリサイタルショーにおいで下さってありがとうございます。今宵、しばし皆様の時間を拝借して、私の歌をお聞きください。では、まずはこの歌から」'
line = '  a    '

mrphs = juman.analysis(line).mrph_list()

mrph_match = MrphMatch(mrphs)

result = mrph_match.match(
    conds = [
        MrphMatch.match_spaces,
    ]
)

print(result.matched)
print(result.matched_str)
print(result.matched_count)


# %%
