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
# 2ループ
# フレーム間隔 0.2秒
FIXED_TOTAL_FRAMES = 4
FIXED_LOOP_COUNT = 2
FRAME_DURATION_MS = 200 

def resize_and_center(img_file):
    """画像を読み込んで600x400のキャンバス中央に配置する関数"""
    original = Image.open(img_file).convert("RGBA")
    
    # ベースキャンバス（背景白推奨だが、透過素材も考慮して透明に設定）
    # ※もし背景を白にしたい場合は (255, 255, 255, 255) に変更してください
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
    
    data = output_io.getvalue()
    size_kb = len(data) / 1024
    return data, size_kb

# --- UI ---
st.title("🔄 2枚画像 交互表示 APNG")
st.caption("自動生成：600x400 / 4フレーム / 2ループ / フルカラー")

col_input1, col_input2 = st.columns(2)
with col_input1:
    file1 = st.file_uploader("1枚目の画像", type=["jpg", "png"], key="img1")
with col_input2:
    file2 = st.file_uploader("2枚目の画像", type=["jpg", "png"], key="img2")

# 2枚ともアップロードされたら自動実行
if file1 and file2:
    st.markdown("---")
    col_preview1, col_preview2, col_result = st.columns(3)
    
    with col_preview1:
        st.caption("1枚目")
        st.image(file1, use_column_width=True)
    with col_preview2:
        st.caption("2枚目")
        st.image(file2, use_column_width=True)

    # 自動実行
    with st.spinner("生成中..."):
        apng_bytes, final_size_kb = process_alternating_images(file1, file2)
    
    with col_result:
        st.caption("生成結果 (プレビュー)")
        st.image(apng_bytes, use_column_width=True)
        
        if final_size_kb <= MAX_FILE_SIZE_KB:
            st.success(f"✅ {final_size_kb:.1f}KB (OK)")
        else:
            st.error(f"⚠️ {final_size_kb:.1f}KB (超過)")
            st.caption("※フルカラー維持のため圧縮していません。")
            
        st.download_button(
            label="ダウンロード",
            data=apng_bytes,
            file_name="alternating_anim.png",
            mime="image/png",
            type="primary"
        )
elif file1 or file2:
    st.info("2枚の画像をアップロードしてください。")
