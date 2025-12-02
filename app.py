import streamlit as st
from PIL import Image
import io

# --- ページ設定 ---
st.set_page_config(page_title="2枚画像 交互表示APNG", layout="centered")

# --- 設定 (固定値) ---
TARGET_WIDTH = 600
TARGET_HEIGHT = 400
MAX_FILE_SIZE_KB = 300

# 【固定設定】
# 4フレーム (A -> B -> A -> B)
# 3ループ
# フレーム間隔 0.2秒
FIXED_TOTAL_FRAMES = 4
FIXED_LOOP_COUNT = 3  # ループ数を3に変更
FRAME_DURATION_MS = 200 

def resize_and_center(img_file):
    """画像を読み込んで600x400のキャンバス中央に配置する関数"""
    original = Image.open(img_file).convert("RGBA")
    
    # ベースキャンバス（背景透明）
    base = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    
    # アスペクト比を維持してリサイズ
    original.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
    
    # 中央配置
    x = (TARGET_WIDTH - original.width) // 2
    y = (TARGET_HEIGHT - original.height) // 2
    base.paste(original, (x, y), original)
    
    return base

def process_alternating_images(file1, file2):
    # 1. 画像の準備
    img1 = resize_and_center(file1)
    img2 = resize_and_center(file2)

    # 2. シーケンス作成 (4フレーム: 1 -> 2 -> 1 -> 2)
    frames = [img1, img2, img1, img2]
            
    # 3. 保存処理 (フルカラー維持)
    output_io = io.BytesIO()
    frames[0].save(
        output_io,
        format="PNG",
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=FIXED_LOOP_COUNT,
        optimize=True
    )
