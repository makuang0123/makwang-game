# ==========================================
# 4. 主畫面排版 (戰況看板置頂・答題闖關第二順位凸顯)
# ==========================================
render_header_banner()

if "nav_tab" not in st.session_state:
    st.session_state.nav_tab = "🔥 戰況看板 & 群島海圖"

if st.session_state.nav_tab != "🎯 答題闖關入口":
    st.markdown(
        '<div class="floating-cruise-container">'
        '<svg width="190" height="135" viewBox="0 0 220 160" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<path d="M22 108L42 136C42 136 100 142 174 136L202 108H22Z" fill="#0f172a" stroke="#0369a1" stroke-width="2.5"/>'
        '<path d="M24 108H200L194 114H31L24 108Z" fill="#ef4444"/>'
        '<path d="M28 84H192L198 108H24L28 84Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="2.5"/>'
        '<rect x="46" y="62" width="130" height="22" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>'
        '<path d="M34 6 C80 1 120 14 170 8 C195 5 210 10 214 12 C206 24 214 36 210 48 C160 42 120 54 80 48 C55 52 40 48 34 50 Z" fill="#dc2626" stroke="#fef08a" stroke-width="3"/>'
        '<text x="120" y="34" font-size="21" font-weight="900" fill="#ffffff" text-anchor="middle" font-family="-apple-system, sans-serif" letter-spacing="3">點我闖關</text>'
        '</svg>'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button(" ", key="floating_cruise_btn"):
        st.session_state.nav_tab = "🎯 答題闖關入口"
        st.rerun()

# 調整順序：戰況看板放第一位，答題闖關放第二位，管理員放第三位
nav_options = ["🔥 戰況看板 & 群島海圖", "🎯 答題闖關入口", "⚙️ 管理員劃島控制"]
selected_nav = st.radio(
    "導覽選單",
    options=nav_options,
    index=nav_options.index(st.session_state.nav_tab) if st.session_state.nav_tab in nav_options else 0,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.nav_tab = selected_nav

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

if selected_nav == "🔥 戰況看板 & 群島海圖":
    render_live_leaderboard_auto()
elif selected_nav == "🎯 答題闖關入口":
    render_quiz_engine()
elif selected_nav == "⚙️ 管理員劃島控制":
    st.subheader("🛠️ 院所搶島與活動後台控制")
    qualified_clinics = [c for c in GLOBAL_STATE["clinics"].values() if c["completed_count"] >= math.ceil(c["target"] * 0.6)]
    qualified_clinics = sorted(qualified_clinics, key=lambda x: x["qualified_at"] or datetime.datetime.max)
    
    if not qualified_clinics:
        st.info("目前尚無院所達到 60% 門檻。")
    else:
        admin_c = st.selectbox("選擇操作院所：", options=qualified_clinics, format_func=lambda x: f"{x['name']} (順位達標時間: {x['qualified_at'].strftime('%H:%M:%S') if x['qualified_at'] else 'N/A'})")
        available_islands = [k for k, v in GLOBAL_STATE["islands"].items() if v["status"] == "available"]
        
        if admin_c["selected_island"]:
            st.success(f"該院所已成功佔領：{admin_c['selected_island']}")
        elif not available_islands:
            st.warning("所有群島已被佔領完畢！")
        else:
            target_island = st.selectbox("選擇要登陸的島嶼：", options=available_islands, format_func=lambda k: f"{GLOBAL_STATE['islands'][k]['name']} ({k})")
            if st.button("確認鎖定並登島", key="btn_admin_lock"):
                ok, msg = select_island_atomic(admin_c["name"], target_island)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    st.markdown("---")
    st.subheader("📋 闖關完成名單查詢與下載")
    records = GLOBAL_STATE["completion_records"]
    if not records:
        st.info("目前尚無同仁完成通關。")
    else:
        df_records = pd.DataFrame(records)
        st.dataframe(df_records, use_container_width=True)
        
        csv_data = df_records.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載通關名單 CSV",
            data=csv_data,
            file_name=f"ma_kwang_completion_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            key="btn_download_csv"
        )
