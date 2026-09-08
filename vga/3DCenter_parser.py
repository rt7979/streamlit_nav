import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

"""

顯卡出貨量

"""



# 1. 模擬/導入從網路爬取下來的原始顯卡歷史季度出貨量數據 (單位：百萬張)
# 這裡選取了包含「2017挖礦潮」、「2021加密貨幣瘋狂期」與「2023-2025 AI浪潮」的核心歷史節點
raw_data = {
    "Quarter": ["2017 Q1", "2017 Q2", "2017 Q3", "2017 Q4", 
                "2018 Q1", "2018 Q2", "2018 Q3", "2018 Q4",
                "2019 Q1", "2019 Q2", "2019 Q3", "2019 Q4",
                "2020 Q1", "2020 Q2", "2020 Q3", "2020 Q4",
                "2021 Q1", "2021 Q2", "2021 Q3", "2021 Q4",
                "2022 Q1", "2022 Q2", "2022 Q3", "2022 Q4",
                "2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4",
                "2024 Q1", "2024 Q2", "2024 Q3", "2024 Q4",
                "2025 Q1", "2025 Q2", "2025 Q3", "2025 Q4"],
    "NVIDIA_Shipments": ["8.1", "8.9", "10.2", "9.5", "8.8", "7.6", "6.2", "5.1", "5.5", "6.2", "7.1", "7.5", "6.8", "7.2", "8.5", "9.1", "9.5", "9.8", "10.1", "10.5", "9.2", "7.8", "5.5", "5.2", "5.4", "5.8", "6.5", "7.2", "7.5", "7.8", "8.2", "8.6", "8.9", "9.2", "9.5", "9.8"],
    "AMD_Shipments": ["3.2", "3.8", "4.1", "3.9", "3.5", "2.9", "2.1", "1.8", "2.0", "2.3", "2.8", "2.7", "2.4", "2.3", "2.9", "3.1", "3.2", "2.9", "2.6", "2.4", "2.1", "1.6", "1.2", "0.9", "0.8", "1.1", "1.3", "1.5", "1.6", "1.5", "1.4", "1.5", "1.6", "1.7", "1.6", "1.7"]
}

df = pd.DataFrame(raw_data)

# =========================================================================
# 【步驟一：數據清洗 Data Cleaning】
# =========================================================================
print("--- 原始數據型態 ---")
print(df.dtypes)

# 1. 將字串型態的「出貨量」轉換為浮點數 (Float)，以便進行數學計算與繪圖
df["NVIDIA_Shipments"] = df["NVIDIA_Shipments"].astype(float)
df["AMD_Shipments"] = df["AMD_Shipments"].astype(float)

# 2. 計算每季總出貨量 (Total Shipments)
df["Total_Shipments"] = df["NVIDIA_Shipments"] + df["AMD_Shipments"]

# 儲存清洗與加總後的資料，方便後續分析使用
csv_path = Path(__file__).with_name("3dcenter_gpu_shipments.csv")
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

# 3. 為了讓 X 軸標籤美觀，創建一個乾淨的時間軸標籤
# 每隔 4 個季度（即每年 Q1）才顯示一次年份，避免 X 軸字體全部擠在一起
x_labels = [q if "Q1" in q else "" for q in df["Quarter"]]

print("\n--- 清洗與加總後的數據預覽 ---")
print(df.head())

# =========================================================================
# 【步驟二：數據視覺化 Data Visualization】
# =========================================================================
# 設定繁體中文和負號顯示（避免 Mac/Windows 轉換時文字變框框）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial'] 
plt.rcParams['axes.unicode_minus'] = False

# 建立圖表畫布大小
plt.figure(figsize=(14, 7), dpi=100)
sns.set_style("whitegrid", {"font.sans-serif": ['Microsoft JhengHei', 'Arial']})

# 1. 繪制出貨量折線圖
plt.plot(df["Quarter"], df["Total_Shipments"], label="全球獨顯總出貨量", color="#2c3e50", linewidth=3, marker='o', markersize=6)
plt.plot(df["Quarter"], df["NVIDIA_Shipments"], label="NVIDIA 出貨量", color="#76B900", linewidth=2, linestyle='--')
plt.plot(df["Quarter"], df["AMD_Shipments"], label="AMD 出貨量", color="#ED1C24", linewidth=2, linestyle='--')

# 2. 【核心精華】利用背景顏色區塊 (axvspan) 標註出影響顯卡售價與金融屬性的歷史重大事件
# 區塊一：2017 - 2018 第一次加密貨幣挖礦潮（比特幣/以太幣暴漲）
plt.axvspan("2017 Q2", "2018 Q1", color='orange', alpha=0.15, label="第一次加密貨幣挖礦潮")
plt.text("2017 Q2", 13.5, " 第一次挖礦潮\n (顯卡供不應求)", color="darkorange", fontsize=10, weight='bold')

# 區塊二：2020 Q4 - 2022 Q2 疫情居家 + 以太坊瘋狂挖礦期（顯卡異變為期貨、溢價最嚴重的時期）
plt.axvspan("2020 Q4", "2022 Q2", color='red', alpha=0.12, label="以太坊挖礦瘋狂期 (顯卡期貨化)")
plt.text("2020 Q4", 14.5, " 🎯 歷史級溢價期\n (年初買、年底加價賣)\n 消費者被迫拉長換機週期", color="crimson", fontsize=10, weight='bold')

# 區塊三：2023 Q3 至今 生成式 AI 浪潮（AI 伺服器搶佔產能、高階顯卡如 4090 價格暴漲）
plt.axvspan("2023 Q3", "2025 Q4", color='green', alpha=0.1, label="生成式 AI 浪潮")
plt.text("2023 Q3", 13.5, " 🤖 AI 浪潮爆發\n (產能移轉/4090禁令溢價)", color="green", fontsize=10, weight='bold')

# 3. 優化圖表細節與標籤
plt.title("全球獨立顯示卡歷史出貨量趨勢與市場重大事件分析 (專題研究)", fontsize=16, pad=20, weight='bold')
plt.xlabel("季度 (Quarter)", fontsize=12, labelpad=10)
plt.ylabel("出貨量 (單位：百萬張 / Millions)", fontsize=12, labelpad=10)

# 設定 X 軸標籤旋轉與過濾（讓圖表更乾淨）
plt.xticks(range(len(df["Quarter"])), x_labels, rotation=45, fontsize=10)
plt.yticks(fontsize=10)

# 設定顯示範圍與圖例
plt.ylim(0, 16)
plt.legend(loc="lower left", fontsize=10, frameon=True, shadow=True)

# 4. 自動調整佈局並儲存圖片
plt.tight_layout()
plt.savefig("gpu_market_analysis_project.png", dpi=300)
plt.show()

print(f"\n[成功] 數據清洗完成，CSV 已儲存為 '{csv_path}'！")
print("圖表已成功繪製並儲存為 'gpu_market_analysis_project.png'！")