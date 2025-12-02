import streamlit as st
# ページ設定（必ずファイルの先頭）
st.set_page_config(page_title="2枚画像 交互表示", layout="centered")

from PIL import Image
import io

# --- 設定値 ---
TARGET_WIDTH = 600
TARGET_HEIGHT = 400
MAX_FILE_SIZE_KB = 300

# 【今回の変更点】
# 5フレーム (1秒)
# 4ループ
# 0.2秒間隔
FIXED_TOTAL_FRAMES = 5
FIXED_LOOP_COUNT = 4
FRAME_DURATION = 200

def resize_and_center(img_file):
    # 画像を読み込んでリサイズ・中央配置
    img = Image.open(img_file).convert("RGBA")
    base = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
    img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
    
    x = (TARGET_WIDTH - img.width) // 2
    y = (TARGET_HEIGHT - img.height) // 2
    base.paste(img, (x, y), img)
    return base

def process_images(file1, file2):
    # 画像準備
    img1 = resize_and_center(file1)
    img2 = resize_and_center(file2)
    
    # 5フレーム作成 (交互に配置: 1->2->1->2->1)
    frames = []
    for i in range(FIXED_TOTAL_FRAMES):
        if i % 2 == 0:
            frames.append(img1)
        else:
            frames.append(img2)
    
    # 保存処理
    output_io = io.BytesIO()
    frames[0].save(
        output_io,
        format="PNG",
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=FIXED_LOOP_COUNT,
        optimize=True
    )
    
    data = output_io.getvalue()
    return data, len(data)/1024

# --- 画面表示 ---
st.title("🔄 2枚画像 交互表示 APNG")
st.caption(f"仕様：{FIXED_TOTAL_FRAMES}フレーム / {FIX
