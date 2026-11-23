import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="손서연 STOP",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GREEN = "#0f4d3a"
GREEN_DARK = "#0a3326"
YELLOW = "#ffc144"
CREAM = "#fff6ec"
PINK = "#ff9fb5"
BLUE = "#9db8ff"

# ------------------------------------------------------------------ CSS
st.markdown(
    f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
html, body, [class*="css"], .stApp {{ font-family: 'Pretendard', sans-serif; }}
.stApp {{ background: {CREAM}; }}
header[data-testid="stHeader"], footer, #MainMenu {{ display: none; }}
.block-container {{ padding-top: 0 !important; max-width: 1100px; }}

/* 상단 네비 */
.topbar {{
  background: {GREEN_DARK}; margin: 0 -9999px; padding: 12px 9999px;
  display: flex; align-items: center; gap: 12px;
  border-bottom: 3px solid; border-image: linear-gradient(90deg,{BLUE},{PINK},{YELLOW}) 1;
}}
.logo {{ width: 44px; height: 44px; border-radius: 50%; background: {YELLOW};
  display:flex; align-items:center; justify-content:center; font-weight:900; color:{GREEN_DARK}; font-size:20px; }}
.brand b {{ color:#fff; font-size:18px; display:block; line-height:1.1; }}
.brand span {{ color:#9fd5bf; font-size:10px; letter-spacing:2px; }}

/* 히어로 */
.hero {{
  position: relative; margin: 0 -9999px; padding: 70px 9999px 110px;
  background:
    radial-gradient(circle at 85% 20%, rgba(255,193,68,.25), transparent 40%),
    radial-gradient(circle at 10% 90%, rgba(255,159,181,.18), transparent 40%),
    linear-gradient(135deg, {GREEN_DARK}, {GREEN} 60%, #1b6b52);
  color: #fff; overflow: hidden;
}}
.lights {{ height: 14px; margin: 0 -9999px; background:
  radial-gradient(circle, {YELLOW} 2px, transparent 3px) 0 0/28px 14px repeat-x; opacity:.9; }}
.pill {{ display:inline-block; background:rgba(0,0,0,.45); border:1px solid rgba(255,255,255,.15);
  padding:7px 16px; border-radius:12px; font-size:12px; color:{YELLOW}; letter-spacing:1px; margin-bottom:22px; }}
.hero h1 {{ font-size: 64px; line-height: 1.15; font-weight: 900; margin: 0 0 22px; color:#fff; }}
.grad {{ background: linear-gradient(90deg,{BLUE},{PINK}); -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; }}
.hero p {{ font-size:16px; line-height:1.9; color:#e8f3ee; margin-bottom:28px; }}
.btn {{ display:inline-block; padding:16px 44px; border-radius:14px; font-weight:800; margin-right:12px; }}
.btn-y {{ background:{YELLOW}; color:{GREEN_DARK}; box-shadow:0 5px 0 #d99a1f; }}
.btn-g {{ background:rgba(255,255,255,.12); color:#fff; border:1px solid rgba(255,255,255,.35); }}
.floating {{ position:absolute; right: 12%; top: 50px; font-size:120px; opacity:.9; }}

/* 정보 바 */
.infobar {{
  margin-top: -52px; position: relative; background:#fff; border:1.5px solid {GREEN_DARK};
  border-radius: 22px; display:grid; grid-template-columns: repeat(3,1fr);
  box-shadow: 0 10px 0 rgba(255,193,68,.35); overflow:hidden;
}}
.infobar div {{ padding: 20px 26px; border-right:1px dashed #ddd; display:flex; gap:14px; align-items:center; }}
.infobar div:last-child {{ border-right:none; }}
.ico {{ width:44px; height:44px; border-radius:50%; background:linear-gradient(135deg,{BLUE},{PINK});
  display:flex; align-items:center; justify-content:center; font-size:20px; }}
.infobar small {{ color:#888; font-size:11px; display:block; }}
.infobar b {{ color:{GREEN_DARK}; font-size:15px; }}

.stop {{ margin: 46px 0 14px; display:flex; align-items:center; gap:10px; }}
.stop .tag {{ background:#111; color:{YELLOW}; padding:6px 16px; border-radius:10px; font-size:12px; font-weight:800; letter-spacing:1px; }}
.stop .dash {{ flex:1; border-top:2px dashed #9fd5bf; }}

/* 카드 */
.card {{ background:#fff; border-radius:22px; padding:24px 26px; border:1.5px solid #f0e2d0;
  box-shadow:0 6px 0 rgba(15,77,58,.08); }}
.card h3 {{ color:{GREEN_DARK}; margin:0 0 6px; }}
.winner {{ background:linear-gradient(135deg,{GREEN_DARK},{GREEN}); color:#fff; border-radius:22px;
  padding:30px; text-align:center; box-shadow:0 8px 0 {YELLOW}; }}
.winner h2 {{ color:{YELLOW}; font-size:40px; margin:6px 0; }}

/* 탭 = 네비 알약 */
.stTabs [data-baseweb="tab-list"] {{ gap:8px; background:{GREEN_DARK}; padding:8px; border-radius:40px;
  width:fit-content; margin:18px auto 0; }}
.stTabs [data-baseweb="tab"] {{ color:#cfe9de; border-radius:30px; padding:8px 22px; height:auto; background:transparent; }}
.stTabs [aria-selected="true"] {{ background:{YELLOW} !important; color:{GREEN_DARK} !important; font-weight:800; }}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display:none; }}

div.stButton > button {{ background:{YELLOW}; color:{GREEN_DARK}; font-weight:800; border:none;
  border-radius:14px; padding:12px 28px; box-shadow:0 5px 0 #d99a1f; }}
div.stButton > button:hover {{ background:#ffcf6b; color:{GREEN_DARK}; }}
.stSlider [data-baseweb="slider"] div[role="slider"] {{ background:{GREEN}; }}
@media (max-width:768px) {{ .hero h1 {{ font-size:38px; }} .floating {{ display:none; }}
  .infobar {{ grid-template-columns:1fr; }} }}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ 상태
CATEGORIES = ["센스", "유머", "배려", "분위기", "취향 일치", "연락 빈도", "추억 점수", "설렘 지수"]

if "friend_name" not in st.session_state:
    st.session_state.friend_name = "친구"
if "scores" not in st.session_state:
    st.session_state.scores = {c: {"jy": 5, "fr": 5} for c in CATEGORIES}
if "memo" not in st.session_state:
    st.session_state.memo = ""

JY = "이종윤"


def totals():
    jy = sum(v["jy"] for v in st.session_state.scores.values())
    fr = sum(v["fr"] for v in st.session_state.scores.values())
    return jy, fr


# ------------------------------------------------------------------ 상단
st.markdown(
    """
<div class="topbar">
  <div class="logo">서</div>
  <div class="brand"><b>서연 스탑</b><span>SEOYEON STOP</span></div>
</div>
""",
    unsafe_allow_html=True,
)

tab_home, tab_cmp, tab_res = st.tabs(["🏠 홈", "⚖️ 비교하기", "📊 결과 조회"])

# ------------------------------------------------------------------ 홈
with tab_home:
    st.markdown(
        f"""
<div class="hero">
  <div class="floating">💚</div>
  <div class="pill">● SEOYEON · 손서연 비교 라운지 &amp; 카페</div>
  <h1>고민도<br><span class="grad">설렘</span>이 될 수 있도록</h1>
  <p>손서연을 주제로, {JY}과 친구를 한 번에 비교해 보세요.<br>
  항목별로 점수를 매기면 레이더 차트와 최종 결과가 바로 나와요.</p>
  <span class="btn btn-y">비교하러 가기</span><span class="btn btn-g">결과 보기</span>
</div>
<div class="infobar">
  <div><span class="ico">👤</span><span><small>주제</small><b>손서연</b></span></div>
  <div><span class="ico">⚖️</span><span><small>비교 대상</small><b>{JY} vs {st.session_state.friend_name}</b></span></div>
  <div><span class="ico">📋</span><span><small>비교 항목</small><b>{len(CATEGORIES)}가지 항목</b></span></div>
</div>
<div class="stop"><span class="tag">NEXT STOP 01</span><b style="color:{GREEN_DARK}">이용 방법</b><span class="dash"></span></div>
""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    steps = [
        ("1️⃣ 이름 정하기", "‘비교하기’ 탭에서 친구 이름을 입력해요."),
        ("2️⃣ 점수 매기기", "각 항목을 0~10점 슬라이더로 채워요."),
        ("3️⃣ 결과 확인", "‘결과 조회’에서 차트와 승자를 확인해요."),
    ]
    for col, (t, d) in zip((c1, c2, c3), steps):
        col.markdown(f'<div class="card"><h3>{t}</h3><p style="color:#666;margin:0">{d}</p></div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ 비교하기
with tab_cmp:
    st.markdown(
        f'<div class="stop"><span class="tag">NEXT STOP 02</span><b style="color:{GREEN_DARK}">점수 입력</b><span class="dash"></span></div>',
        unsafe_allow_html=True,
    )
    st.session_state.friend_name = st.text_input("친구 이름", value=st.session_state.friend_name, max_chars=10)
    fr_name = st.session_state.friend_name or "친구"

    h1, h2, h3 = st.columns([1.2, 2, 2])
    h1.markdown("**항목**")
    h2.markdown(f"**🟢 {JY}**")
    h3.markdown(f"**🟡 {fr_name}**")

    for cat in CATEGORIES:
        c1, c2, c3 = st.columns([1.2, 2, 2])
        c1.markdown(f"<div style='padding-top:32px;font-weight:700;color:{GREEN_DARK}'>{cat}</div>", unsafe_allow_html=True)
        st.session_state.scores[cat]["jy"] = c2.slider(f"{cat}-jy", 0, 10, st.session_state.scores[cat]["jy"], key=f"jy_{cat}", label_visibility="collapsed")
        st.session_state.scores[cat]["fr"] = c3.slider(f"{cat}-fr", 0, 10, st.session_state.scores[cat]["fr"], key=f"fr_{cat}", label_visibility="collapsed")

    st.session_state.memo = st.text_area("한 줄 메모 (선택)", value=st.session_state.memo, placeholder="비교하면서 느낀 점을 적어보세요")

    b1, b2 = st.columns([1, 5])
    if b1.button("초기화"):
        for cat in CATEGORIES:
            st.session_state.scores[cat] = {"jy": 5, "fr": 5}
            st.session_state[f"jy_{cat}"] = 5
            st.session_state[f"fr_{cat}"] = 5
        st.rerun()
    b2.caption("점수를 입력하면 ‘결과 조회’ 탭에 바로 반영돼요.")

# ------------------------------------------------------------------ 결과
with tab_res:
    st.markdown(
        f'<div class="stop"><span class="tag">NEXT STOP 03</span><b style="color:{GREEN_DARK}">비교 결과</b><span class="dash"></span></div>',
        unsafe_allow_html=True,
    )
    fr_name = st.session_state.friend_name or "친구"
    jy_total, fr_total = totals()
    max_total = len(CATEGORIES) * 10

    if jy_total > fr_total:
        title, sub = JY, f"{jy_total - fr_total}점 차이로 앞서요"
    elif fr_total > jy_total:
        title, sub = fr_name, f"{fr_total - jy_total}점 차이로 앞서요"
    else:
        title, sub = "무승부", "두 사람이 똑같아요"

    w1, w2 = st.columns([1.2, 2])
    with w1:
        st.markdown(
            f"""<div class="winner"><div>🏆 손서연 기준 종합 결과</div>
            <h2>{title}</h2><div>{sub}</div>
            <div style="margin-top:14px;opacity:.85">{JY} {jy_total} / {max_total} &nbsp;·&nbsp; {fr_name} {fr_total} / {max_total}</div></div>""",
            unsafe_allow_html=True,
        )
        if st.session_state.memo:
            st.markdown(f'<div class="card" style="margin-top:16px"><b>📝 메모</b><p style="margin:6px 0 0;color:#555">{st.session_state.memo}</p></div>', unsafe_allow_html=True)

    with w2:
        jy_vals = [st.session_state.scores[c]["jy"] for c in CATEGORIES]
        fr_vals = [st.session_state.scores[c]["fr"] for c in CATEGORIES]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=jy_vals + jy_vals[:1], theta=CATEGORIES + CATEGORIES[:1], fill="toself", name=JY, line_color=GREEN, fillcolor="rgba(15,77,58,.25)"))
        fig.add_trace(go.Scatterpolar(r=fr_vals + fr_vals[:1], theta=CATEGORIES + CATEGORIES[:1], fill="toself", name=fr_name, line_color="#f0a500", fillcolor="rgba(255,193,68,.35)"))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            margin=dict(l=40, r=40, t=20, b=20), height=380,
            paper_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=-0.1),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 항목별 비교")
    df = pd.DataFrame(
        {"항목": CATEGORIES, JY: jy_vals, fr_name: fr_vals}
    )
    df["우세"] = [JY if a > b else (fr_name if b > a else "동점") for a, b in zip(jy_vals, fr_vals)]
    st.bar_chart(df.set_index("항목")[[JY, fr_name]], color=[GREEN, YELLOW], height=300)
    st.dataframe(df, use_container_width=True, hide_index=True)

    wins_jy = (df["우세"] == JY).sum()
    wins_fr = (df["우세"] == fr_name).sum()
    m1, m2, m3 = st.columns(3)
    m1.metric(f"{JY} 우세 항목", f"{wins_jy}개")
    m2.metric(f"{fr_name} 우세 항목", f"{wins_fr}개")
    m3.metric("동점 항목", f"{(df['우세'] == '동점').sum()}개")

st.markdown("<div style='text-align:center;color:#aaa;margin:50px 0 20px;font-size:12px'>© 서연 스탑 · 재미로 보는 비교 사이트</div>", unsafe_allow_html=True)
