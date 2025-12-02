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
st.caption(f"仕様：{FIXED_TOTAL_FRAMES}フレーム / {FIXED_LOOP_COUNT}ループ / フルカラー")

col1, col2 = st.columns(2)
with col1:
    f1 = st.file_uploader("1枚目", type=["jpg", "png"], key="f1")
with col2:
    f2 = st.file_uploader("2枚目", type=["jpg", "png"], key="f2")

if f1 and f2:
    st.markdown("---")
    # プレビュー
    p1, p2, res = st.columns(3)
    with p1:
        st.image(f1, caption="1枚目", use_column_width=True)
    with p2:
        st.image(f2, caption="2枚目", use_column_width=True)
        
    # 自動生成
    with st.spinner("生成中..."):
        data, size = process_images(f1, f2)
        
    with res:
        st.image(data, caption="生成結果", use_column_width=True)
        
        if size <= MAX_FILE_SIZE_KB:
            st.success(f"容量 OK: {size:.1f}KB")
        else:
            st.error(f"容量超過: {size:.1f}KB")
            
        st.download_button(
            "ダウンロード",
            data=data,
            file_name="alternating_5f_4loop.png",
            mime="image/png",
            type="primary"
        )
elif f1 or f2:
    st.info("2枚の画像をアップロードしてください")
