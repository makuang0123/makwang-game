import streamlit as st
import pandas as pd
import datetime
import math
import os

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
        padding: 24px 16px;
        color: white;
        text-align: center;
        box-shadow: 0 12px 25px -5px rgba(2, 132, 199, 0.35);
        border: 2px solid #e0f2fe;
        margin-bottom: 20px;
    }
    .banner-title {
        font-size: 2.1rem;
        font-weight: 900;
        letter-spacing: 2px;
        color: #ffffff;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .banner-badge {
        background: #ffffff;
        color: #0369a1;
        display: inline-block;
        padding: 5px 16px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 0.9rem;
        margin-top: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    /* 空狀態提示卡片 */
    .empty-state-box {
        background: #ffffff;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        border: 2px dashed #93c5fd;
        color: #0369a1;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 15px;
    }

    /* 自家院所專屬高亮卡片 */
    .my-clinic-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border-radius: 16px;
        padding: 18px;
        border: 2.5px solid #22c55e;
        box-shadow: 0 8px 16px rgba(34, 197, 94, 0.15);
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* 標籤徽章 */
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
    .badge-waiting {
        background-color: #f1f5f9;
        color: #64748b;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        border: 1px solid #cbd5e1;
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

    /* 按鈕樣式 */
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
# 1. 員工與院所資料庫 (自動讀取 Excel + 完整防呆備援)
# ==========================================
@st.cache_data
def load_full_employee_data():
    emp_db = {}
    clinic_counts = {
        '屏東院': 56, '管理處': 54, '信義院': 53, '彰化院': 40, '陽明院': 38,
        '崇學院': 35, '明華院': 34, '東港院': 32, '東霖院': 32, '鳳山院': 31,
        '潮州院': 31, '博愛院': 30, '迪化院': 30, '五甲院': 29, '光華院': 28,
        '台東院': 28, '藍田院': 28, '佑昌院': 28, '建功院': 27, '亞灣院': 27,
        '瑞隆院': 24, '意凡院': 23, '民權院': 23, '開元院': 22, '百合院': 22,
        '橋頭院': 18, '崇德院': 18, '成功院': 16, '專案成員': 15, '新加坡': 4
    }

    excel_filename = "Employee-20260901200132.xlsx"
    if os.path.exists(excel_filename):
        try:
            df = pd.read_excel(excel_filename)
            df['員工編號'] = df['員工編號'].astype(str).str.strip().str.upper()
            df['所屬院所'] = df['所屬院所'].astype(str).str.strip()

            def parse_bday(val):
                if pd.isnull(val):
                    return "0101"
                if isinstance(val, pd.Timestamp):
                    return val.strftime('%m%d')
                try:
                    dt = pd.to_datetime(val)
                    return dt.strftime('%m%d')
                except:
                    s = str(val).replace("-", "").replace("/", "").strip()
                    return s[-4:] if len(s) >= 4 else "0101"

            df['bday_mmdd'] = df['生日'].apply(parse_bday)

            for _, row in df.iterrows():
                emp_db[row['員工編號']] = {
                    "clinic": row['所屬院所'],
                    "bday": row['bday_mmdd'],
                    "title": str(row.get('職稱', '同仁'))
                }
            clinic_counts = df['所屬院所'].value_counts().to_dict()
        except Exception:
            pass

    return emp_db, clinic_counts

# 獲取全域唯讀員工資料庫
GLOBAL_EMP_DB, GLOBAL_CLINIC_COUNTS = load_full_employee_data()

def init_database():
    # 確保 employee_db 永遠存在於 session 中
    st.session_state.employee_db = GLOBAL_EMP_DB

    if "clinics" not in st.session_state:
        st.session_state.clinics = {}
        for idx, (c_name, count) in enumerate(GLOBAL_CLINIC_COUNTS.items(), start=1):
            cid = f"C{idx:02d}"
            st.session_state.clinics[c_name] = {
                "id": cid,
                "name": c_name,
                "target": int(count),
                "completed_count": 0,
                "qualified_at": None,
                "selected_island": None
            }

    if "islands" not in st.session_state:
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

    if "questions" not in st.session_state:
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

    if "completed_employees" not in st.session_state:
        st.session_state.completed_employees = set()

init_database()

# ==========================================
# 2. 業務核心邏輯
# ==========================================
def get_clinic_stats(clinic_name):
    c = st.session_state.clinics[clinic_name]
    target = c["target"]
    completed = c["completed_count"]
    rate = (completed / target) * 100 if target > 0 else 0
    needed_for_60 = math.ceil(target * 0.6)
    diff = max(0, needed_for_60 - completed)
    is_qualified = completed >= needed_for_60
    return {
        "id": c["id"],
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

def get_ranked_active_stats():
    all_stats = [get_clinic_stats(c_name) for c_name in st.session_state.clinics]
    active_stats = [s for s in all_stats if s["completed"] > 0]
    qualified = sorted([s for s in active_stats if s["is_qualified"]], key=lambda x: x["qualified_at"] or datetime.datetime.max)
    unqualified = sorted([s for s in active_stats if not s["is_qualified"]], key=lambda x: x["rate"], reverse=True)
    return qualified + unqualified

def record_user_completion(employee_id, clinic_name):
    if employee_id in st.session_state.completed_employees:
        return False, "您先前已經通關，戰力已計入！"
    
    st.session_state.completed_employees.add(employee_id)
    clinic = st.session_state.clinics[clinic_name]
    clinic["completed_count"] += 1
    
    needed_for_60 = math.ceil(clinic["target"] * 0.6)
    if clinic["completed_count"] >= needed_for_60 and clinic["qualified_at"] is None:
        clinic["qualified_at"] = datetime.datetime.now()
    
    return True, "成功通關！為所屬院所增加 1 名航行戰力！"

def select_island_atomic(clinic_name, island_code):
    island = st.session_state.islands.get(island_code)
    clinic = st.session_state.clinics.get(clinic_name)
    
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

def reset_user_session():
    st.session_state.user = {
        "logged_in": False,
        "emp_id": "",
        "clinic_name": "",
        "progress": {"family_day": False, "ma_kwang": False, "policy": False},
        "current_q_idx": 0,
        "wrong_feedback": None
    }

# ==========================================
# 3. 視覺組件
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
    ranked_stats = get_ranked_active_stats()
    
    st.subheader("🔥 領航先鋒榜 (TOP 5)")
    
    if not ranked_stats:
        st.markdown("""
        <div class="empty-state-box">
            ⛵ 全院艦隊整裝待發中！目前尚無同仁通關<br>
            <span style="font-size:0.9rem; font-weight:normal; color:#64748b;">立即前往【🎯 答題闖關入口】，成為第一位幫自家院所奪得排名的先鋒！</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("達標 60% 依時間優先排定選島順位；衝刺中單位依完成率排名。")
        rank_emojis = ["🥇", "🥈", "🥉", "⭐", "⭐"]
        top_5 = ranked_stats[:5]

        for idx, s in enumerate(top_5):
            rank = idx + 1
            icon = rank_emojis[idx] if idx < len(rank_emojis) else "⭐"
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 2])
                with col1:
                    st.markdown(f"**{icon} #{rank} {s['name']}**")
                    if s["is_qualified"]:
                        st.markdown(f"<span class='badge-success'>🏆 第 {rank} 順位達標</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='badge-urgent'>🔥 還差 {s['diff']} 人！</span>", unsafe_allow_html=True)
                with col2:
                    progress_val = min(1.0, s["completed"] / s["target"]) if s["target"] > 0 else 0
                    st.progress(progress_val)
                    st.caption(f"⛵ 登船：{s['completed']}/{s['target']} 人 ({s['rate']:.1f}%) | 60%門檻：{s['needed_60']} 人")
                with col3:
                    if s["selected_island"]:
                        st.markdown(f"🏝️ **已佔領：{s['selected_island']}**")
                    elif s["is_qualified"]:
                        st.markdown("⏳ **待劃位登島**")
                    else:
                        st.markdown("🌊 **全速航行中**")
            st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("🔍 查詢自家院所即時戰況")
    
    clinic_options = list(st.session_state.clinics.keys())
    selected_cname = st.selectbox(
        "請選擇院所／單位以查看獨立進度：",
        options=clinic_options,
        format_func=lambda x: f"{x} (目標: {st.session_state.clinics[x]['target']}人)"
    )
    
    if selected_cname:
        my_rank = next((i + 1 for i, s in enumerate(ranked_stats) if s["name"] == selected_cname), None)
        my_s = get_clinic_stats(selected_cname)
        rank_text = f"第 #{my_rank} 名" if my_rank is not None else "尚無排名 (待首位同仁通關啟航)"
        
        st.markdown(f"""
        <div class="my-clinic-box">
            <div style="font-size: 1.25rem; font-weight: 800; color: #0284c7; margin-bottom: 6px;">
                ⚓ {my_s['name']}（全院即時戰況：<b>{rank_text}</b>）
            </div>
            <div style="font-size: 0.95rem; color: #334155; margin-bottom: 8px;">
                目標應答人數：<b>{my_s['target']} 人</b> ｜ 目前通關人數：<b>{my_s['completed']} 人</b> ｜ 完成率：<b>{my_s['rate']:.1f}%</b>
            </div>
        """, unsafe_allow_html=True)
        
        progress_val = min(1.0, my_s["completed"] / my_s["target"]) if my_s["target"] > 0 else 0
        st.progress(progress_val)
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if my_s["is_qualified"]:
                st.markdown(f"<span class='badge-success' style='font-size:0.9rem;'>🏆 已跨越 60% 門檻（取得順位資格）</span>", unsafe_allow_html=True)
            elif my_s["completed"] > 0:
                st.markdown(f"<span class='badge-urgent' style='font-size:0.9rem;'>🔥 距離 60% 門檻（{my_s['needed_60']}人）還差 <b>{my_s['diff']}</b> 人！</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span class='badge-waiting' style='font-size:0.9rem;'>⏳ 尚未啟航（達標門檻：{my_s['needed_60']}人）</span>", unsafe_allow_html=True)
        with col_b:
            if my_s["selected_island"]:
                st.markdown(f"🏝️ **已佔領席位：{my_s['selected_island']}**")
            elif my_s["is_qualified"]:
                st.markdown("⏳ **資格保留，等待管理員開放劃位**")
            elif my_s["completed"] > 0:
                st.markdown("🌊 **全速航行中，快呼叫更多夥伴！**")
            else:
                st.markdown("⛵ **點擊上方闖關，奪得院所第 1 票！**")
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_island_grid():
    st.subheader("🗺️ 室內渡假群島配置海圖 (一排 5 個・共 5 排)")
    st.markdown("<div style='text-align: center; color: #0284c7; font-weight: 800; margin-bottom: 8px;'>🌊 ═══ 舞台與海景第一排 (STAGE FRONT) ═══ 🌊</div>", unsafe_allow_html=True)
    
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
        reset_user_session()

    u = st.session_state.user

    # 1. 登入表單
    if not u["logged_in"]:
        st.markdown("### ⛵ 登船啟航認證")
        
        emp_id_input = st.text_input("1. 請輸入員工編號 (例: MKM00961 或 CEO00003)", key="login_emp_input").strip().upper()
        
        detected_clinic = ""
        matched_info = None
        emp_dict = getattr(st.session_state, "employee_db", GLOBAL_EMP_DB)
        
        if emp_id_input and emp_id_input in emp_dict:
            matched_info = emp_dict[emp_id_input]
            detected_clinic = matched_info["clinic"]
            st.success(f"識別成功！所屬單位：**{detected_clinic}**（{matched_info['title']}）")
        elif emp_id_input:
            st.warning("⚠️ 查無此員工編號，請確認輸入是否正確。")

        bday_input = st.text_input("2. 請輸入四碼生日密碼 (例: 04月18日請輸入 0418)", type="password", max_chars=4, key="login_bday_input").strip()

        if st.button("驗證身分並啟航", type="primary", key="btn_do_login"):
            if not emp_id_input:
                st.error("請輸入員工編號！")
            elif not matched_info:
                st.error("查無此員工編號，無法登入！")
            elif not bday_input:
                st.error("請輸入四碼生日密碼！")
            elif matched_info["bday"] != bday_input:
                st.error("生日密碼不正確，請重新輸入！(格式範例：0418)")
            else:
                u["logged_in"] = True
                u["emp_id"] = emp_id_input
                u["clinic_name"] = detected_clinic
                st.rerun()
        return

    c_info = get_clinic_stats(u["clinic_name"])
    ranked_stats = get_ranked_active_stats()
    my_rank = next((i + 1 for i, s in enumerate(ranked_stats) if s["name"] == u["clinic_name"]), None)
    rank_str = f"目前排名 #{my_rank}" if my_rank is not None else "尚未啟航"

    col_user, col_logout = st.columns([3, 1])
    with col_user:
        st.markdown(f"#### 👋 同仁 `{u['emp_id']}` 歡迎登船！所屬單位：**{c_info['name']}** ({rank_str})")
    with col_logout:
        if st.button("🚪 切換同仁 / 登出", key="btn_logout_top"):
            reset_user_session()
            st.rerun()
    
    all_done = all(u["progress"].values()) or (u["emp_id"] in st.session_state.completed_employees)
    
    # 通關完成畫面
    if all_done:
        st.success(f"🎉 恭喜通關！您已為 **{c_info['name']}** 貢獻 1 份登島戰力！")
        if c_info["is_qualified"]:
            st.info("🏆 貴院所已跨越 60% 門檻！請密切關注即時海圖與大會廣播！")
        else:
            st.warning(f"🔥 距離 60% 門檻還差 **{c_info['diff']}** 人，快召集院內夥伴登船！")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 交給下一位夥伴作答（更換員工編號）", type="primary", key="btn_next_user"):
            reset_user_session()
            st.rerun()
        return

    # 答題引擎
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

    if st.button("送出答案", type="primary", key="btn_submit_ans"):
        if selected_option == q_data["ans"]:
            u["progress"][active_cat] = True
            u["wrong_feedback"] = None
            u["current_q_idx"] = 0
            
            if all(u["progress"].values()):
                success, msg = record_user_completion(u["emp_id"], u["clinic_name"])
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
    if st.button("🔄 刷新最新戰況海圖", key="btn_refresh_map"):
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
            if st.button("確認鎖定並登島", key="btn_admin_lock"):
                ok, msg = select_island_atomic(admin_c["name"], target_island)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
