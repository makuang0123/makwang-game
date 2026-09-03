CUSTOM_CSS = """
<style>
    .stApp { 
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%); 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }
    
    /* 頂部海軍深藍 Banner */
    .ocean-banner {
        background: linear-gradient(135deg, #0369a1 0%, #075985 50%, #0c4a6e 100%);
        border-radius: 18px;
        padding: 20px 14px;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 10px 20px -3px rgba(3, 105, 161, 0.4);
        border: 2px solid #38bdf8;
        margin-bottom: 14px;
    }
    .banner-title {
        font-size: 1.85rem;
        font-weight: 900;
        letter-spacing: 1.5px;
        color: #ffffff !important;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
        margin-bottom: 6px;
    }
    .banner-badge {
        background: #fef08a;
        color: #854d0e !important;
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-weight: 900;
        font-size: 0.85rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }
    
    /* 📜 遊戲規則與獎勵說明區塊 */
    .rules-card {
        background: #ffffff;
        border: 2.5px solid #0284c7;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.15);
    }
    .rules-title {
        font-size: 1.15rem;
        font-weight: 900;
        color: #0369a1;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .rules-content {
        font-size: 0.92rem;
        color: #1e293b;
        line-height: 1.6;
        font-weight: 600;
    }

    /* 🎯 頂部導覽選單放大、整體框線與字體加大 */
    div[data-testid="stHorizontalBlock"] div[data-baseweb="radio"] {
        background: #ffffff !important;
        border: 2.5px solid #0284c7 !important;
        border-radius: 14px !important;
        padding: 10px 18px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.2) !important;
    }
    div[data-baseweb="radio"] label {
        font-size: 1.35rem !important;
        font-weight: 900 !important;
        color: #0369a1 !important;
    }
    
    /* 🌟 特別將第二個選項（答題闖關入口）加上鮮艷的橘紅色底色塊與白字突顯 */
    div[data-baseweb="radio"] div:nth-child(2) {
        background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%) !important;
        padding: 4px 12px !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 10px rgba(234, 88, 12, 0.35) !important;
        margin-left: 6px;
        margin-right: 6px;
    }
    div[data-baseweb="radio"] div:nth-child(2) label {
        color: #ffffff !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }

    /* 🚢 巨型豪華郵輪浮標 (純視覺動畫) */
    .floating-cruise-container {
        position: fixed !important;
        right: 6px !important;
        bottom: 155px !important;
        width: 190px !important;
        height: 135px !important;
        z-index: 999990 !important;
        pointer-events: none !important;
        animation: floatCruise 3s ease-in-out infinite alternate !important;
        filter: drop-shadow(0 14px 28px rgba(0, 0, 0, 0.45));
    }
    @keyframes floatCruise {
        0% { transform: translateY(0px) rotate(-1.5deg); }
        50% { transform: translateY(-8px) rotate(1.5deg); }
        100% { transform: translateY(0px) rotate(-1.5deg); }
    }

    .st-key-floating_cruise_btn {
        position: fixed !important;
        right: 6px !important;
        bottom: 155px !important;
        width: 190px !important;
        height: 135px !important;
        z-index: 999999 !important;
    }
    .st-key-floating_cruise_btn button {
        width: 190px !important;
        height: 135px !important;
        border-radius: 24px !important;
        background: transparent !important;
        border: none !important;
        cursor: pointer !important;
    }

    label[data-testid="stWidgetLabel"] p {
        font-size: 1.18rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        margin-bottom: 8px !important;
    }
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 2.5px solid #0284c7 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.18) !important;
    }

    .island-5x6-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 5px;
        width: 100%;
        margin-top: 8px;
        margin-bottom: 12px;
    }
    .island-grid-item {
        border-radius: 8px;
        padding: 6px 2px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 66px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
    }
    .island-available {
        background: #ffffff;
        border: 1.5px dashed #0284c7;
        color: #0369a1;
    }
    .island-taken {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        border: 2px solid #082f49;
        color: #ffffff;
    }
    .island-title {
        font-size: 0.72rem;
        font-weight: 800;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
    }
    .island-taken-who {
        background: #fef08a;
        color: #713f12 !important;
        font-size: 0.76rem;
        font-weight: 900;
        border-radius: 4px;
        padding: 1px 3px;
        margin: 2px 0;
        width: 92%;
    }
    .island-status-open {
        color: #0284c7;
        font-size: 0.68rem;
        font-weight: 800;
        margin: 1px 0;
    }
    .island-code {
        font-size: 0.6rem;
        color: #64748b;
    }
    .island-code-taken {
        font-size: 0.6rem;
        color: #e0f2fe;
    }

    .live-broadcast-ticker {
        background: #ffffff;
        border: 2px solid #0284c7;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 14px;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.12);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ticker-tag {
        background: #0284c7;
        color: #ffffff !important;
        padding: 3px 8px;
        border-radius: 14px;
        font-weight: 900;
        font-size: 0.75rem;
        white-space: nowrap;
    }
    .ticker-content {
        font-weight: 800;
        color: #0f172a;
        font-size: 0.88rem;
    }
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
    .my-clinic-box {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px;
        border: 2.5px solid #16a34a;
        box-shadow: 0 6px 14px rgba(22, 163, 74, 0.15);
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .badge-urgent {
        background-color: #ffedd5;
        color: #9a3412 !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        border: 1px solid #fdba74;
    }
    .badge-success {
        background-color: #dcfce7;
        color: #15803d !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        border: 1px solid #86efac;
    }
    .badge-waiting {
        background-color: #f1f5f9;
        color: #334155 !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        border: 1px solid #cbd5e1;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.2em;
        font-weight: 800;
        font-size: 1.05rem;
        background: #0284c7;
        color: white !important;
        border: none;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.28);
    }
</style>
"""
