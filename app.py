import streamlit as st
import pandas as pd
import datetime
import math

# ==========================================
# 0. 頁面配置與「沐光與航」海洋明亮風 CSS
# ==========================================
st.set_page_config(
    page_title="沐光與航・馬光家庭日｜院所搶位大挑戰",
    page_icon="⛵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CUSTOM_CSS = """
<style>
    /* 沐光與航主題配色：海洋藍、森林綠、暖陽金 */
    .main { 
        background: linear-gradient(180deg, #e0f2fe 0%, #f0fdf4 100%); 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
    }
    
    /* 頂部主視覺 Banner 卡片 */
    .kv-banner {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        border-radius: 16px;
        padding: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .kv-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }
    .kv-subtitle {
        font-size: 1.05rem;
        background-color: #fef08a;
        color: #854d0e;
        display: inline-block;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 700;
        margin-top: 6px;
    }
    
    /* 競賽進度卡片 */
    .urgent-badge {
        background-color: #fee2e2;
        color: #dc2626;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #fca5a5;
    }
    .success-badge {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid #86efac;
    }
    
    /* 座位圖視覺 */
    .seat-box {
        border-radius: 10px;
        padding: 16px 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .seat-available { 
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); 
        color: white; 
        border: 2px solid #15803d; 
    }
    .seat-taken { 
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
        color: white; 
        border: 2px solid #b91c1c; 
        opacity: 0.95; 
    }
    
    /* 手機按鈕優化 */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.2em;
        font-weight: 700;
        font-size: 1.05rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==========================================
# 1. 資料庫初始化 (Mock Data)
# ==========================================
def init_database():
    if "db_initialized" not in st.session_state:
        # 院所基本資料
        st.session_state.clinics = {
            "C01": {"id": "C01", "name": "高雄旗艦院", "target": 100, "completed_count": 58, "qualified_at": None, "selected_seat": None},
            "C02": {"id": "C02", "name": "左營崇德院", "target": 80, "completed_count": 47, "qualified_at": None, "selected_seat": None},
            "C03": {"id": "C03", "name": "屏東自由院", "target": 120, "completed_count": 68, "qualified_at": None, "selected_seat": None},
            "C04": {"id": "C04", "name": "台南金華院", "target": 60, "completed_count": 35, "qualified_at": None, "selected_seat": None},
            "C05": {"id": "C05", "name": "鳳山五甲院", "target": 90, "completed_count": 40, "qualified_at": None, "selected_seat": None},
        }

        # 融入「沐光與航」主題題庫
        st.session_state.questions = {
            "family_day": [
                {
                    "id": "F01",
                    "q": "今年 2026 馬光家庭日的主題名稱是什麼？",
                    "options": ["A. 光芒萬丈・揚帆出海", "B. 沐光與航", "C. 同心協力・奔向未來", "D. 乘風破浪・共創光芒"],
                    "ans": 1,
                    "exp": "今年主題為『沐光與航』，象徵馬光全員聚心前行、共創繁星！"
                },
                {
                    "id": "F02",
                    "q": "2026/11/01(日) 馬光家庭日的舉辦地點在哪裡？",
                    "options": ["A. 高雄流行音樂中心", "B. 高雄巨蛋體育館", "C. 高雄展覽館南館＋室外草坪", "D. 義大遊樂世界"],
                    "ans": 2,
                    "exp": "本次活動包下高雄展覽館南館（室內特區）及室外海景大草坪！"
                }
            ],
            "ma_kwang": [
                {
                    "id": "M01",
                    "q": "馬光醫療體系始終堅持的核心精神不包含下列何者？",
                    "options": ["A. 專業誠信", "B. 視病猶親", "C. 利潤至上", "D. 團隊協作"],
                    "ans": 2,
                    "exp": "馬光始終以同仁幸福與患者健康為先，堅守醫者仁心。"
                },
                {
                    "id": "M02",
                    "q": "馬光中醫推動的『一人一診室』最主要的初衷是什麼？",
                    "options": ["A. 增加空間租金", "B. 守護患者隱私與頂級問診品質", "C. 方便醫師午休", "D. 配合消防空間劃分"],
                    "ans": 1,
                    "exp": "給予患者最安心放鬆的獨立診斷空間，貫徹高品質醫療標準。"
                }
            ],
            "policy": [
                {
                    "id": "P01",
                    "q": "依據近期院所規範，同仁遇異常事件通報應於多久內登錄系統？",
                    "options": ["A. 24小時內", "B. 3天內", "C. 一週內", "D. 月底前"],
                    "ans": 0,
                    "exp": "及時通報能讓跨部門及時支援，24 小時內通報是保障同仁與院所的關鍵流程！"
                },
                {
                    "id": "P02",
                    "q": "關於同仁外部教育訓練學分補助政策，常規每年度可申請幾次進修補助？",
                    "options": ["A. 1次", "B. 2次", "C. 3次", "D. 依院長專案核定，原則每年2次"],
                    "ans": 3,
                    "exp": "馬光鼓勵同仁不斷精進學習，每年常規提供 2 次補助，特殊專案另行評估。"
                }
            ]
        }

        # 展覽館南館座位區
        st.session_state.seats = {
            "南館A區": {"name": "南館A區 (近主舞台視野特區)", "capacity": 100, "status": "available", "taken_by": None},
            "南館B區": {"name": "南館B區 (中央海景主桌區)", "capacity": 80, "status": "available", "taken_by": None},
            "南館C區": {"name": "南館C區 (草坪出入口動線區)", "capacity": 120, "status": "available", "taken_by": None},
            "南館D區": {"name": "南館D區 (東側家庭歡聚區)", "capacity": 60, "status": "available", "taken_by": None},
            "南館E區": {"name": "南館E區 (西側市集交流特區)", "capacity": 90, "status": "available", "taken_by": None},
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
        "selected_seat": c["selected_seat"]
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
    
    return True, "成功通關！為所屬院所貢獻 1 名關鍵戰力！"

def select_seat_atomic(clinic_id, seat_key):
    seat = st.session_state.seats.get(seat_key)
    clinic = st.session_state.clinics.get(clinic_id)
    
    if not seat or not clinic:
        return False, "無效的選擇"
    if seat["status"] == "taken":
        return False, f"太慢了！{seat_key} 剛剛已被 {seat['taken_by']} 選走！"
    if clinic["selected_seat"] is not None:
        return False, f"貴院所已經選擇過 {clinic['selected_seat']}，無法重複選擇。"
    
    seat["status"] = "taken"
    seat["taken_by"] = clinic["name"]
    clinic["selected_seat"] = seat_key
    return True, f"成功搶下 {seat_key}！"

# ==========================================
# 3. 視覺組件：主 Banner 與排行榜
# ==========================================
def render_header_banner():
    st.markdown("""
    <div class="kv-banner">
        <div style="font-size: 0.95rem; letter-spacing: 1px; opacity: 0.9;">⛵ 2026 馬光醫療網・家庭日專屬活動</div>
        <div class="kv-title">沐光與航・院所搶位大挑戰</div>
        <div class="kv-subtitle">📅 2026/11/01 (日) 高雄展覽館南館＋室外草坪</div>
    </div>
    """, unsafe_allow_html=True)

def render_live_leaderboard():
    st.subheader("🔥 院所啟航即時戰況 (60% 門檻搶室內席位)")
    
    stats_list = [get_clinic_stats(cid) for cid in st.session_state.clinics]
    qualified = sorted([s for s in stats_list if s["is_qualified"]], key=lambda x: x["qualified_at"] or datetime.datetime.max)
    unqualified = sorted([s for s in stats_list if not s["is_qualified"]], key=lambda x: x["rate"], reverse=True)
    sorted_stats = qualified + unqualified

    for idx, s in enumerate(sorted_stats):
        rank = idx + 1
        with st.container():
            col1, col2, col3 = st.columns([1.5, 3, 2])
            with col1:
                if s["is_qualified"]:
                    st.markdown(f"**#{rank} {s['name']}**")
                    st.markdown(f"<span class='success-badge'>🏆 順位 {rank} 達標</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**#{rank} {s['name']}**")
                    st.markdown(f"<span class='urgent-badge'>🔥 衝刺中！還差 {s['diff']} 人</span>", unsafe_allow_html=True)
            with col2:
                progress_val = min(1.0, s["completed"] / s["target"])
                st.progress(progress_val)
                st.caption(f"已上船：{s['completed']}/{s['target']} 人 ({s['rate']:.1f}%) | 達標線：{s['needed_60']} 人")
            with col3:
                if s["selected_seat"]:
                    st.markdown(f"🪑 **已鎖定：{s['selected_seat']}**")
                elif s["is_qualified"]:
                    st.markdown("⏳ **取得優先劃位權**")
                else:
                    st.markdown("⚪ **全員集氣中**")
        st.markdown("---")

def render_seat_map():
    st.subheader("🪑 高雄展覽館南館・室內席位即時配置圖")
    st.markdown("<div style='text-align: center; color: #0284c7; font-weight: bold;'>════ 舞台前方 (STAGE) ════</div><br>", unsafe_allow_html=True)
    
    cols = st.columns(len(st.session_state.seats))
    for idx, (s_key, s_val) in enumerate(st.session_state.seats.items()):
        with cols[idx]:
            if s_val["status"] == "taken":
                st.markdown(f"""
                <div class="seat-box seat-taken">
                    <div>🔴 {s_key}</div>
                    <div style="font-size:0.85rem; margin-top:4px;">{s_val['taken_by']}</div>
                    <div style="font-size:0.75rem;">(已鎖定)</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="seat-box seat-available">
                    <div>🟢 {s_key}</div>
                    <div style="font-size:0.85rem; margin-top:4px;">容量 {s_val['capacity']}人</div>
                    <div style="font-size:0.75rem;">(可選擇)</div>
                </div>
                """, unsafe_allow_html=True)
    st.caption("🟢 綠色：目前可劃位 | 🔴 紅色：已被其他院所鎖定")

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
        st.markdown("### ⛵ 登船身分認證")
        with st.form("login_form"):
            emp_id = st.text_input("請輸入員工編號 (例: MK8801)", value="MK8801")
            clinic_id = st.selectbox("選擇所屬院所", options=list(st.session_state.clinics.keys()), format_func=lambda x: st.session_state.clinics[x]["name"])
            submitted = st.form_submit_button("進入啟航大挑戰")
            if submitted:
                if emp_id.strip():
                    u["logged_in"] = True
                    u["emp_id"] = emp_id.strip()
                    u["clinic_id"] = clinic_id
                    st.rerun()
        return

    c_info = get_clinic_stats(u["clinic_id"])
    st.markdown(f"#### 👋 同仁 `{u['emp_id']}` 一起沐光與航！所屬：**{c_info['name']}**")
    
    all_done = all(u["progress"].values()) or (u["emp_id"] in st.session_state.completed_employees)
    
    if all_done:
        st.success(f"🎉 恭喜完成全部三大關卡！已為 **{c_info['name']}** 增加 1 名戰力！")
        if c_info["is_qualified"]:
            st.info("🏆 貴院所已達標 60% 門檻！敬請鎖定現場即時看板等待劃位！")
        else:
            st.warning(f"🔥 距離 60% 門檻還差 **{c_info['diff']}** 人，快呼叫院內夥伴一起挑戰！")
        return

    p_col1, p_col2, p_col3 = st.columns(3)
    p_col1.metric("① 沐光家庭日", "✅ 通關" if u["progress"]["family_day"] else "⬜ 挑戰中")
    p_col2.metric("② 馬光好文化", "✅ 通關" if u["progress"]["ma_kwang"] else "⬜ 挑戰中")
    p_col3.metric("③ 重點新政策", "✅ 通關" if u["progress"]["policy"] else "⬜ 挑戰中")

    if not u["progress"]["family_day"]:
        active_cat = "family_day"
        cat_title = "關卡一：沐光家庭日知多少"
    elif not u["progress"]["ma_kwang"]:
        active_cat = "ma_kwang"
        cat_title = "關卡二：馬光醫療網文化通"
    else:
        active_cat = "policy"
        cat_title = "關卡三：近期政策與實務規範"

    st.markdown(f"### 📍 當前關卡：{cat_title}")
    
    q_list = st.session_state.questions[active_cat]
    q_data = q_list[u["current_q_idx"] % len(q_list)]

    st.markdown(f"**題目：{q_data['q']}**")
    selected_option = st.radio("請選擇答案：", range(len(q_data["options"])), format_func=lambda i: q_data["options"][i], key=f"q_{active_cat}_{u['current_q_idx']}")

    if u["wrong_feedback"]:
        st.error(f"❌ 答錯囉！{u['wrong_feedback']['msg']}")
        st.info(f"💡 **小知識／解說**：{u['wrong_feedback']['exp']}")

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
# 4. 主畫面佈局
# ==========================================
render_header_banner()

tab_main, tab_quiz, tab_admin = st.tabs(["🔥 搶位即時戰況", "🎯 答題闖關入口", "⚙️ 管理員選位控制"])

with tab_main:
    render_live_leaderboard()
    render_seat_map()
    if st.button("🔄 刷新最新戰況數據"):
        st.rerun()

with tab_quiz:
    render_quiz_engine()

with tab_admin:
    st.subheader("🛠️ 院所選位與活動後台控制")
    qualified_clinics = [c for c in st.session_state.clinics.values() if c["completed_count"] >= math.ceil(c["target"] * 0.6)]
    qualified_clinics = sorted(qualified_clinics, key=lambda x: x["qualified_at"] or datetime.datetime.max)
    
    if not qualified_clinics:
        st.info("目前尚無院所達到 60% 門檻。")
    else:
        admin_c = st.selectbox("選擇操作院所：", options=qualified_clinics, format_func=lambda x: f"{x['name']} (達標時間: {x['qualified_at'].strftime('%H:%M:%S') if x['qualified_at'] else 'N/A'})")
        available_seats = [k for k, v in st.session_state.seats.items() if v["status"] == "available"]
        
        if admin_c["selected_seat"]:
            st.success(f"該院所已劃位：{admin_c['selected_seat']}")
        elif not available_seats:
            st.warning("所有座位已被搶選完畢！")
        else:
            target_seat = st.selectbox("選擇鎖定區域：", options=available_seats)
            if st.button("確認鎖定座位"):
                ok, msg = select_seat_atomic(admin_c["id"], target_seat)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
