import numpy as np
import pandas as pd
import math
from sklearn.metrics.pairwise import cosine_similarity

champion_names = [
    "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe",
    "AurelionSol", "Aurora", "Azir", "Bard", "Belveth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn", "Camille",
    "Cassiopeia", "Chogath", "Corki", "Darius", "Diana", "DrMundo", "Draven", "Ekko", "Elise",
    "Evelynn", "Ezreal", "Fiddlesticks", "Fiora", "Fizz", "Galio", "Gangplank", "Garen", "Gnar",
    "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei", "Illaoi", "Irelia", "Ivern", "Janna",
    "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "KSante", "Kaisa", "Kalista", "Karma", "Karthus",
    "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Khazix", "Kindred", "Kled", "KogMaw", "Leblanc",
    "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Malzahar", "Maokai",
    "MasterYi", "Milio", "MissFortune", "Mordekaiser", "Morgana", "Naafiri", "Nami", "Nasus", "Nautilus", "Neeko",
    "Nidalee", "Nilah", "Nocturne", "Nunu", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy",
    "Pyke", "Qiyana", "Quinn", "Rakan", "Rammus", "RekSai", "Rell", "Renata", "Renekton", "Rengar",
    "Riven", "Rumble", "Ryze", "Samira", "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen",
    "Shyvana", "Singed", "Sion", "Sivir", "Skarner","Smolder", "Sona", "Soraka", "Swain", "Sylas", "Syndra",
    "TahmKench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh", "Tristana", "Trundle", "Tryndamere",
    "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar", "Velkoz", "Vex", "Vi",
    "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "MonkeyKing", "Xayah", "Xerath", "XinZhao",
    "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
]

champion_winrate = [
    0.4953, 0.5016, 0.492, 0.4904, 0.4885, 0.5326, 0.5196, 0.5081, 0.4751, 0.4909, 
    0.5187, 0.4817, 0.4621, 0.491, 0.4957, 0.4906, 0.5077, 0.4987, 0.5201, 0.4914, 
    0.503, 0.5125, 0.5091, 0.4268, 0.4933, 0.5074, 0.4938, 0.5105, 0.5023, 0.4991, 
    0.4899, 0.4774, 0.5097, 0.4982, 0.5054, 0.5221, 0.4768, 0.5194, 0.4865, 0.4863, 
    0.4859, 0.4997, 0.4883, 0.5104, 0.5018, 0.5212, 0.4921, 0.4881, 0.516, 0.5079, 
    0.4924, 0.4801, 0.5232, 0.5047, 0.5007, 0.4754, 0.4979, 0.4919, 0.497, 0.4884, 
    0.5028, 0.5034, 0.4971, 0.502, 0.4774, 0.5161, 0.522, 0.4545, 0.5008, 0.4834, 
    0.5014, 0.5144, 0.5077, 0.4851, 0.5043, 0.5062, 0.4938, 0.5116, 0.4864, 0.4987, 
    0.5123, 0.5052, 0.5023, 0.5203, 0.5046, 0.5215, 0.5205, 0.5116, 0.482, 0.4941, 
    0.4726, 0.5152, 0.5223, 0.4917, 0.4875, 0.4932, 0.5091, 0.494, 0.5146, 0.4943, 
    0.4722, 0.5031, 0.4894, 0.5037, 0.5, 0.4986, 0.4879, 0.4974, 0.4606, 0.4882, 
    0.4729, 0.5072, 0.4874, 0.482, 0.5134, 0.4999, 0.5177, 0.4977, 0.5079, 0.5171, 
    0.5123, 0.5023, 0.4994, 0.486, 0.4647, 0.5133, 0.5054, 0.5064, 0.5004, 0.5078, 
    0.5163, 0.4963, 0.4887, 0.5236, 0.5026, 0.4933, 0.447, 0.5024, 0.5003, 0.4975, 
    0.4929, 0.5103, 0.5163, 0.4794, 0.4918, 0.5168, 0.5109, 0.5153, 0.4896, 0.5015, 
    0.5103, 0.4859, 0.5127, 0.518, 0.4834, 0.5162, 0.5058, 0.486, 0.4872, 0.5268, 
    0.4772, 0.503, 0.4891, 0.4822, 0.5053, 0.5051, 0.4955, 0.5112
]

champion_winrate_dict = dict(zip(champion_names, champion_winrate))

# 데이터 파일 로드
data = pd.read_csv('./whatcham/id_champion_stats.csv')

# 열 이름 지정 (데이터에 따라 조정 필요)
data.columns = ['UserID', 'Champion', 'Games', 'Wins', 'WinRate', 'TotalGame', 'PickRate']

# 유저ID로 그룹화
grouped = data.groupby('UserID')

# 결과를 저장할 빈 데이터프레임 생성
rows = []

scale = 1
margin = 0
# 각 유저에 대해 반복
for name, group in grouped:
    # 각 챔피언의 게임 가중치를 저장할 임시 딕셔너리
    champion_dict = {champion: 0 for champion in champion_names}
    
    # 그룹 내의 데이터를 이용해 챔피언 데이터 업데이트
    for index, row in group.iterrows():
        champion = row['Champion']
        if champion in champion_dict:
            # 가중치 행렬 작성
            avg_winrate = champion_winrate_dict.get(champion, 0)
            winning_weight = 1 + 0.5 * math.tanh(scale * (row['WinRate']/100 - avg_winrate + margin))
            champion_dict[champion] = winning_weight * row['PickRate']/100
        else:
            #챔피언 오타 처리
            print(champion)

    # 결과 리스트에 추가
    rows.append({'UserID': name, **champion_dict})
    
user_item_DataFrame = pd.DataFrame(rows, columns = champion_names)
# 결과 저장
user_item_DataFrame.to_csv('./whatcham/output_user.csv', index=False)
user_item_matrix = user_item_DataFrame.to_numpy()

# 아이템 간의 코사인 유사도 계산 (100 x 100 크기의 아이템 유사도 행렬)
item_similarity = cosine_similarity(user_item_matrix.T)

pd.DataFrame(item_similarity, columns=champion_names).to_csv('./whatcham/output_item.csv', index=False)

# def recommend_items(user_ratings, item_similarity, top_n=5):
#     # 사용자가 평가한 아이템들 중 평가한 아이템의 유사한 아이템 점수 계산
#     # item_similarity.dot(user_ratings) 계산
#     numerators = item_similarity.dot(user_ratings)
#     # 분모 계산: 각 아이템에 대한 유사도의 절대값 합
#     denominators = np.abs(item_similarity).sum(axis=1)
#     # 분모가 0인 경우에는 매우 작은 수(epsilon)로 대체
#     safe_denominators = np.where(denominators > 0, denominators, 1)
#     # 안전한 나눗셈 수행
#     scores = numerators / safe_denominators

#     # 이미 평가한 아이템은 제외 (0으로 설정)
#     # already_rated = user_ratings > 0
#     # scores[already_rated] = 0

#     # 추천할 아이템 top_n 선정
#     recommended_items = np.argsort(-scores)
    
#     return recommended_items

# def add_new_user(user_item_matrix, new_user_ratings):
#     # 새로운 유저의 평가를 행렬에 추가
#     updated_matrix = np.vstack([user_item_matrix, new_user_ratings])
#     return updated_matrix

# # 예시로 0번 유저에게 추천할 아이템
# user_index = 0
# print(f"User {user_index}번이 평가한 아이템: {user_item_matrix[user_index]}")
# # 해당 유저가 평가한 아이템들 가져오기
# user_ratings = user_item_matrix[user_index]
# recommended_items = recommend_items(user_ratings, item_similarity)

# # User에게 추천할 아이템의 이름을 출력
# recommended_champions = [champion_names[idx] for idx in recommended_items[:20]]  # 상위 20개 추천 결과
# print(f"User {user_index}에게 추천할 아이템: {recommended_champions}")