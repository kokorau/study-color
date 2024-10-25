import json
from sklearn.model_selection import train_test_split
import numpy as np

# JSONファイルの読み込み
with open('../data/processed/oklchPalette.json', 'r') as file:
    data = json.load(file)

# Numpy配列に変換（データ操作を簡単にするため）
data = np.array(data)

# 訓練データとテストデータに分割 (80%を訓練用, 20%をテスト用)
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# 訓練データの保存
with open('../data/processed/train_oklchPalette.json', 'w') as train_file:
    json.dump(train_data.tolist(), train_file, indent=2)

# テストデータの保存
with open('../data/processed/test_oklchPalette.json', 'w') as test_file:
    json.dump(test_data.tolist(), test_file, indent=2)

print("データを訓練データとテストデータに分割しました。")
