import streamlit as st
import pandas as pd
import datetime
import math
import random

# ==========================================
# 0. 頁面配置與藍白渡假風 CSS
# ==========================================
st.set_page_config(
    page_title="沐光與航｜群島搶位大挑戰",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CUSTOM_CSS = """
<style>
    /* 藍白海洋渡假主色系 */
    .stApp { 
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%); 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }
    
    /* 渡假風主視覺 Banner */
    .ocean-banner {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #075985 100%);
        border-radius: 20px;
        padding: 26px 16px;
        color: white;
        text-align: center;
        box-shadow: 0 12px 25px -5px rgba(2, 132, 199, 0.35);
        border: 2px solid #e0f2fe;
        margin-bottom: 20px;
    }
    .banner-title {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .banner-badge {
        background: #ffffff;
        color: #0369a1;
        display: inline-block;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.95rem;
        margin-top: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    /* 賽事排行榜卡片 */
    .clinic-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border: 1.5px solid #e0f2fe;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .badge-urgent {
        background-color: #ffedd5;
        color: #c2410c;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        border: 1px solid #fdba74;
    }
    .badge-success {
        background-color: #ecfdf5;
        color: #047857;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        border: 1px solid #a7f3d0;
    }

    /* 5x5 群島樣式座位卡 */
    .island-card {
        border-radius: 12px;
        padding: 10px 4px;
        text-align: center;
        margin: 4px 0;
        font-size: 0.85rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
    }
    .island-available {
        background: #ffffff;
        border: 2px dashed #0284c7;
        color: #0369a1;
    }
    .island-taken {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border: 2px solid #075985;
        color: #ffffff;
    }

    /* 手機按鈕 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        font-weight: 800;
        font-size: 1.05rem;
        background: #0284c7;
        color: white;
        border: none;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.3);
    }
    .stButton>button:hover {
        background: #0369a1;
        color: white;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 1. 資料庫初始化 (Mock Data)
# ==========================================
def init_database():
    if "db_initialized" not in st.session_state:
        # 院所清單
        st.session_state.clinics = {
            "C01": {"id": "C01", "name": "高雄旗艦院", "target": 100, "completed_count": 58, "qualified_at": None, "selected_island": None},
            "C02": {"id": "C02", "name": "左營崇德院", "target": 80, "completed_count": 47, "qualified_at": None, "selected_island": None},
            "C03": {"id": "C03", "name": "屏東自由院", "target": 120, "completed_count": 68, "qualified_at": None, "selected_island": None},
            "C04": {"id": "C04", "name": "台南金華院", "target": 60, "completed_count": 35, "qualified_at": None, "selected_island": None},
            "C05": {"id": "C05", "name": "鳳山五甲院", "target": 90, "completed_count": 40, "qualified_at": None, "selected_island": None},
        }

        # 5 排 × 每排 5 個 = 25 個渡假群島席位
        st.session_state.islands = {}
        island_themes = [
            "蔚藍島", "晨曦島", "椰影島", "珊瑚島", "微風島",
            "晴空島", "海鷗島", "海星島", "珍珠島", "沐光島",
            "碧波島", "逐浪島", "金沙島", "揚帆島", "晨光島",
            "星月島", "海螺島", "向陽島", "海嵐島", "琉璃島",
            "天際島", "悠遊島", "綠洲島", "航向島", "榮耀島"
        ]
        
        idx = 0
        for r in range(1, 6):
            for c in range(1, 6):
                code = f"R{r}-{c}"
                name = island_themes[idx]
                st.session_state.islands[code] = {
                    "code": code,
                    "name": name,
                    "row": r,
                    "col": c,
                    "status": "available",
                    "taken_by": None
                }
                idx += 1

        # 題庫
        st.session_state.questions = {
            "family_day": [
                {
                    "id": "F01",
                    "q": "⛵ 2026 馬光家庭日的主軸名稱為何？",
                    "options": ["A. 光芒萬丈", "B. 沐光與航", "C. 同心協力", "D. 乘風破浪"],
                    "ans": 1,
                    "exp": "今年主題為『沐光與航』，象徵大家如艦隊般齊心出航！"
                },
                {
                    "id": "F02",
                    "q": "🏝️ 2026/11/01(日) 馬光家庭日的舉辦地點在哪裡？",
                    "options": ["A. 高雄流行音樂中心", "B. 高雄巨蛋", "C. 高雄展覽館南館＋室外草坪", "D. 駁二特區"],
                    "ans": 2,
                    "exp": "活動包下高雄展覽館南館渡假室內區與海景草坪！"
                }
            ],
            "ma_kwang": [
                {
                    "id": "M01",
                    "q": "⚓ 馬光醫療體系的核心理念不包含下列何者？",
                    "options": ["A. 專業誠信", "B. 視病猶親", "C. 利潤至上", "D. 團隊協作"],
                    "ans": 2,
                    "exp": "馬光始終以同仁與患者的幸福健康為最高準則。"
                },
                {
                    "id": "M02",
                    "q": "🏥 馬光中醫首創推動的『一人一診室』主要目的是？",
                    "options": ["A. 增加裝潢費用", "B. 守護隱私與維持極致問診品質", "C. 醫師休息室", "D. 放置更多儀器"],
                    "ans": 1,
                    "exp": "提供患者安心放鬆且完全獨立的問診環境！"
                }
            ],
            "policy": [
                {
                    "id": "P01",
                    "q": "📑 依最新通報指引，同仁若遇異常事件應於多久內登錄系統？",
                    "options": ["A. 24小時內", "B. 3天內", "C. 一週內", "D. 月底結算"],
                    "ans": 0,
                    "exp": "24小時內通報能讓跨部門及時提供後援支援！"
                },
                {
                    "id": "P02",
                    "q": "🎓 關於同仁外部進修補助政策，常規每年度可申請幾次補助？",
                    "options": ["A. 1次", "B. 2次", "C. 3次", "D. 原則每年2次，專案另計"],
                    "ans": 3,
                    "exp": "鼓勵同仁自主進修，每年常規提供 2 次額度支援。"
                }
            ]
        }

        st.session_state.completed_employees = set()
        st.session_state.db_initialized = True

init_database()

# ==========================================
# 2. 業務核心邏輯
# ==========================================
def get_clinic_stats(clinic_id):
    c = st.session_state.clinics[clinic_id]
    target = c["target"]
    completed = c["completed_count"]
    rate = (completed / target) * 100
    needed_for_60 = math.ceil(target * 0.6)
    diff = max(0, needed_for_60 - completed)
    is_qualified = completed >= needed_for_60
    return {
        "id": clinic_id,
        "name": c["name"],
        "target": target,
        "completed": completed,
        "rate": rate,
        "needed_60": needed_for_60,
        "diff": diff,
        "is_qualified": is_qualified,
        "qualified_at": c["qualified_at"],
        "selected_island": c["selected_island"]
    }

def record_user_completion(employee_id, clinic_id):
    if employee_id in st.session_state.completed_employees:
        return False, "您先前已經通關，戰力已計入！"
    
    st.session_state.completed_employees.add(employee_id)
    clinic = st.session_state.clinics[clinic_id]
    clinic["completed_count"] += 1
    
    needed_for_60 = math.ceil(clinic["target"] * 0.6)
    if clinic["completed_count"] >= needed_for_60 and clinic["qualified_at"] is None:
        clinic["qualified_at"] = datetime.datetime.now()
    
    return True, "成功通關！為所屬院所增加 1 名航行戰力！"

def select_island_atomic(clinic_id, island_code):
    island = st.session_state.islands.get(island_code)
    clinic = st.session_state.clinics.get(clinic_id)
    
    if not island or not clinic:
        return False, "無效的選擇"
    if island["status"] == "taken":
        return False, f"太慢了！【{island['name']}】剛被 {island['taken_by']} 搶先登島！"
    if clinic["selected_island"] is not None:
        return False, f"貴院所已經選擇過【{clinic['selected_island']}】，無法重複選擇。"
    
    island["status"] = "taken"
    island["taken_by"] = clinic["name"]
    clinic["selected_island"] = f"{island['name']} ({island_code})"
    return True, f"成功登陸並佔領【{island['name']} ({island_code})】！"

# ==========================================
# 3. 視覺元件：渡假風主視覺與 5x5 群島海圖
# ==========================================
def render_header_banner():
    st.markdown("""
    <div class="ocean-banner">
        <div style="font-size: 1rem; letter-spacing: 2px; opacity: 0.95;">🌊 2026 馬光醫療網・家庭日啟航競賽</div>
        <div class="banner-title">⛵ 沐光與航・群島搶位戰</div>
        <div class="banner-badge">📍 2026/11/01 (日) 高雄展覽館南館 ✕ 海景草坪</div>
    </div>
    """, unsafe_allow_html=True)

def render_live_leaderboard():
    st.subheader("🏆 院所艦隊戰況 (滿 60% 即刻搶登島嶼席位)")
    
    stats_list = [get_clinic_stats(cid) for cid in st.session_state.clinics]
    qualified = sorted([s for s in stats_list if s["is_qualified"]], key=lambda x: x["qualified_at"] or datetime.datetime.max)
    unqualified = sorted([s for s in stats_list if not s["is_qualified"]], key=lambda x: x["rate"], reverse=True)
    sorted_stats = qualified + unqualified

    for idx, s in enumerate(sorted_stats):
        rank = idx + 1
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 2])
            with col1:
                if s["is_qualified"]:
                    st.markdown(f"**#{rank} {s['name']}**")
                    st.markdown(f"<span class='badge-success'>🏆 第 {rank} 順位達標</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**#{rank} {s['name']}**")
                    st.markdown(f"<span class='badge-urgent'>🔥 還差 {s['diff']} 人達標！</span>", unsafe_allow_html=True)
            with col2:
                progress_val = min(1.0, s["completed"] / s["target"])
                st.progress(progress_val)
                st.caption(f"⛵ 登船進度：{s['completed']}/{s['target']} 人 ({s['rate']:.1f}%) | 門檻：{s['needed_60']} 人")
            with col3:
                if s["selected_island"]:
                    st.markdown(f"🏝️ **已佔領：{s['selected_island']}**")
                elif s["is_qualified"]:
                    st.markdown("⏳ **待選島中**")
                else:
                    st.markdown("🌊 **全院航行中**")
        st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

def render_island_grid():
    st.subheader("🗺️ 室內渡假群島配置海圖 (一排 5 個・共 5 排)")
    st.markdown("<div style='text-align: center; color: #0284c7; font-weight: 800; margin-bottom: 8px;'>🌊 ═══ 舞台與海景第一排 (STAGE FRONT) ═══ 🌊</div>", unsafe_allow_html=True)
    
    # 5排 x 5欄
    for r in range(1, 6):
        cols = st.columns(5)
        for c in range(1, 6):
            code = f"R{r}-{c}"
            island = st.session_state.islands[code]
            with cols[c - 1]:
                if island["status"] == "taken":
                    st.markdown(f"""
                    <div class="island-card island-taken">
                        <div>🚩 <b>{island['name']}</b></div>
                        <div style="font-size:0.75rem; margin-top:2px;">{island['taken_by']}</div>
                        <div style="font-size:0.7rem; opacity:0.85;">({code} 已鎖定)</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="island-card island-available">
                        <div>🏝️ <b>{island['name']}</b></div>
                        <div style="font-size:0.75rem; margin-top:2px; color:#0284c7;">可搶登</div>
                        <div style="font-size:0.7rem; color:#64748b;">({code})</div>
                    </div>
                    """, unsafe_allow_html=True)
    st.caption("⚪ 白底虛線：開放登陸的島嶼 | 🔵 藍底色塊：已被其他院所插旗鎖定")

def render_quiz_engine():
    if "user" not in st.session_state:
        st.session_state.user = {
            "logged_in": False,
            "emp_id": "",
            "clinic_id": "C01",
            "progress": {"family_day": False, "ma_kwang": False, "policy": False},
            "current_q_idx": 0,
            "wrong_feedback": None
        }

    u = st.session_state.user

    if not u["logged_in"]:
        st.markdown("### ⛵ 登船啟航認證")
        with st.form("login_form"):
            emp_id = st.text_input("請輸入員工編號 (例: MK8801)", value="MK8801")
            clinic_id = st.selectbox("選擇所屬院所", options=list(st.session_state.clinics.keys()), format_func=lambda x: st.session_state.clinics[x]["name"])
            submitted = st.form_submit_button("進入航海搶位戰")
            if submitted:
                if emp_id.strip():
                    u["logged_in"] = True
                    u["emp_id"] = emp_id.strip()
                    u["clinic_id"] = clinic_id
                    st.rerun()
        return

    c_info = get_clinic_stats(u["clinic_id"])
    st.markdown(f"#### 👋 同仁 `{u['emp_id']}` 歡迎登船！所屬艦隊：**{c_info['name']}**")
    
    all_done = all(u["progress"].values()) or (u["emp_id"] in st.session_state.completed_employees)
    
    if all_done:
        st.success(f"🎉 恭喜通關！您已為 **{c_info['name']}** 貢獻 1 份登島戰力！")
        if c_info["is_qualified"]:
            st.info("🏆 貴院所已跨越 60% 門檻！請密切關注大會廣播與即時海圖！")
        else:
            st.warning(f"🔥 距離 60% 門檻還差 **{c_info['diff']}** 人，快召集同院夥伴登船！")
        return

    p_col1, p_col2, p_col3 = st.columns(3)
    p_col1.metric("① 沐光家庭日", "✅ 通關" if u["progress"]["family_day"] else "⬜ 挑戰中")
    p_col2.metric("② 馬光好精神", "✅ 通關" if u["progress"]["ma_kwang"] else "⬜ 挑戰中")
    p_col3.metric("③ 重點新政策", "✅ 通關" if u["progress"]["policy"] else "⬜ 挑戰中")

    if not u["progress"]["family_day"]:
        active_cat = "family_day"
        cat_title = "關卡一：沐光家庭日知多少 🌴"
    elif not u["progress"]["ma_kwang"]:
        active_cat = "ma_kwang"
        cat_title = "關卡二：馬光醫療網文化通 ⚓"
    else:
        active_cat = "policy"
        cat_title = "關卡三：近期政策與實務規範 📑"

    st.markdown(f"### 📍 當前航線：{cat_title}")
    
    q_list = st.session_state.questions[active_cat]
    q_data = q_list[u["current_q_idx"] % len(q_list)]

    st.markdown(f"**題目：{q_data['q']}**")
    selected_option = st.radio("請選擇正確答案：", range(len(q_data["options"])), format_func=lambda i: q_data["options"][i], key=f"q_{active_cat}_{u['current_q_idx']}")

    if u["wrong_feedback"]:
        st.error(f"❌ 答錯囉！{u['wrong_feedback']['msg']}")
        st.info(f"💡 **解析叮嚀**：{u['wrong_feedback']['exp']}")

    if st.button("送出答案", type="primary"):
        if selected_option == q_data["ans"]:
            u["progress"][active_cat] = True
            u["wrong_feedback"] = None
            u["current_q_idx"] = 0
            
            if all(u["progress"].values()):
                success, msg = record_user_completion(u["emp_id"], u["clinic_id"])
                st.balloons()
            st.rerun()
        else:
            u["wrong_feedback"] = {
                "msg": f"正確答案是：{q_data['options'][q_data['ans']]}",
                "exp": q_data["exp"]
            }
            u["current_q_idx"] += 1
            st.rerun()

# ==========================================
# 4. 主畫面排版
# ==========================================
render_header_banner()

tab_main, tab_quiz, tab_admin = st.tabs(["🔥 群島搶位戰況", "🎯 答題闖關入口", "⚙️ 管理員劃島控制"])

with tab_main:
    render_live_leaderboard()
    st.markdown("---")
    render_island_grid()
    if st.button("🔄 刷新最新戰況海圖"):
        st.rerun()

with tab_quiz:
    render_quiz_engine()

with tab_admin:
    st.subheader("🛠️ 院所搶島與活動後台控制")
    qualified_clinics = [c for c in st.session_state.clinics.values() if c["completed_count"] >= math.ceil(c["target"] * 0.6)]
    qualified_clinics = sorted(qualified_clinics, key=lambda x: x["qualified_at"] or datetime.datetime.max)
    
    if not qualified_clinics:
        st.info("目前尚無院所達到 60% 門檻。")
    else:
        admin_c = st.selectbox("選擇操作院所：", options=qualified_clinics, format_func=lambda x: f"{x['name']} (順位達標時間: {x['qualified_at'].strftime('%H:%M:%S') if x['qualified_at'] else 'N/A'})")
        available_islands = [k for k, v in st.session_state.islands.items() if v["status"] == "available"]
        
        if admin_c["selected_island"]:
            st.success(f"該院所已成功佔領：{admin_c['selected_island']}")
        elif not available_islands:
            st.warning("所有群島已被佔領完畢！")
        else:
            target_island = st.selectbox("選擇要登陸的島嶼：", options=available_islands, format_func=lambda k: f"{st.session_state.islands[k]['name']} ({k})")
            if st.button("確認鎖定並登島"):
                ok, msg = select_island_atomic(admin_c["id"], target_island)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
