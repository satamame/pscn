'''形態素解析を単品で実行して確認するためのスクリプト。
'''

#%%
from pyknp import Juman
from juman_psc import JumanPsc


#%%
# juman = Juman(command='jumanpp_v2',
#     option='--config=C:\ProgramData\jumanpp\model\jumandic.conf')

juman = JumanPsc()

#%%
s = '「'

print(f'{len(s.encode())} bytes.')


#%%
try:
    mrphs = juman.analysis(s).mrph_list()

    for mrph in mrphs:
        print(f'"{mrph.midasi}"')              # 見出し
        print(f'  genkei:   {mrph.genkei}')    # 原形
        print(f'  hinsi:    {mrph.hinsi}')     # 品詞
        print(f'  bunrui:   {mrph.bunrui}')    # 品詞細分類
        print(f'  katuyou2: {mrph.katuyou2}')  # 活用形

except Exception as e:
    print(e)


# %%
