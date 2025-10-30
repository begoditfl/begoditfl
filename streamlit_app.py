import streamlit as st
import yt_dlp

st.set_page_config(page_title="整合歌單播放器", layout="wide")
st.title("🎶 YouTube + Bilibili 整合歌單（公開）")

# ---- 固定歌單 ----
YOUTUBE_PLAYLIST = "https://www.youtube.com/playlist?list=PLejd3ch_3Lm3-FpvZZwHkvLivbq0fFXlc"
BILIBILI_PLAYLIST = "https://space.bilibili.com/354630275/favlist?fid=3667255975&ftype=create"

ydl_opts = {"quiet": True, "extract_flat": True, "skip_download": True}

def fetch_entries(url):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        st.error(f"無法載入歌單：{e}")
        return []
    entries = info.get("entries") or []
    result = []
    for e in entries:
        url = e.get("webpage_url") or e.get("url") or e.get("id")
        title = e.get("title") or url
        result.append({"title": title, "url": url})
    return result

st.header("YouTube 歌單")
for s in fetch_entries(YOUTUBE_PLAYLIST):
    st.markdown(f"**{s['title']}**")
    st.video(s["url"])

st.header("Bilibili 歌單")
for s in fetch_entries(BILIBILI_PLAYLIST):
    st.markdown(f"**{s['title']}**")
    st.components.v1.iframe(s["url"], height=360)

