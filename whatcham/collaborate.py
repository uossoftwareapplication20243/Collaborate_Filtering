import numpy as np
import pandas as pd
import math

from pro_CF import champion_names, champion_winrate

champion_winrate_dict = dict(zip(champion_names, champion_winrate))

# 아이템 유사도 가져오기
item_similarity = pd.read_csv('./whatcham/output_item.csv')

# 새로운 유저의 가중치를 받아오면 아이템 유사도를 바탕으로 챔피언 추천하기