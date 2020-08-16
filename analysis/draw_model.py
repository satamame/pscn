import os
import pickle

from pydotplus import graph_from_dot_data
from sklearn.tree import export_graphviz

model_file = os.path.join(os.path.dirname(__file__), 'model.pkl')

with open(model_file, 'rb') as f:
    tree = pickle.load(f)

dot_data = export_graphviz(tree, filled=True,
    rounded=True,
    class_names=[
        'TITLE',
        'AUTHOR',
        'CHARSHEADLINE',
        'CHARACTER',
        'H1',
        # 'H2',
        # 'H3',
        'DIRECTION',
        'DIALOGUE',
        'ENDMARK',
        # 'COMMENT',
        'EMPTY',
        # 'CHARACTER_CONTINUED',
        'DIRECTION_CONTINUED',
        'DIALOGUE_CONTINUED',
        # 'COMMENT_CONTINUED',
    ],
    feature_names=[
        'pattern_0001',
        'pattern_0002',
        'pattern_0003',
        'pattern_0004',
        'pattern_0005',
        'pattern_0006',
        'symbol_follows',
        'interj_follows',
        'is_first_line',
        'is_last_line',
        'is_empty',
        'ends_w_bracket',
        'sentence_ends',
        'states_charsheadline',
        'leading_spc',
        'leading_spc_delta',
        'prev_is_empty',
        'prev_ends_w_bracket',
        'prev_sentence_ends',
        'ptn_line_count',
        'str_line_count',
        'spc_line_count',
        'bracket_line_rate',
        'prev_is_CHARACTER',
        'prev_is_CHARACTER_CONTINUED',
        'prev_is_DIRECTION',
        'prev_is_DIRECTION_CONTINUED',
        'prev_is_DIALOGUE',
        'prev_is_DIALOGUE_CONTINUED',
        'prev_is_COMMENT',
        'prev_is_COMMENT_CONTINUED',
        'charsheadline_used',
        'h1_used',
        'direction_used',
        'dialogue_used',
    ],
    out_file=None)

graph = graph_from_dot_data(dot_data)
graph.write_png('tree.png')
