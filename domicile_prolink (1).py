import streamlit as st
import pandas as pd
import time
import json

st.set_page_config(
    page_title="DOMICILE Pro-Link",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');

:root {
    --brand-navy:   #0D1B2A;
    --brand-red:    #C0392B;
    --brand-gold:   #D4AC0D;
    --brand-light:  #F4F6F9;
    --brand-card:   #FFFFFF;
    --brand-border: #E2E8F0;
    --brand-text:   #1A202C;
    --brand-muted:  #718096;
    --radius:       12px;
    --shadow:       0 4px 24px rgba(13,27,42,.10);
}

html, body, [class*="css"] {
    font-family: 'Heebo', sans-serif !important;
    direction: rtl;
    text-align: right;
    background: var(--brand-light);
    color: var(--brand-text);
}

#MainMenu, footer, header { visibility: hidden; }

section[data-testid="stSidebar"] {
    background: var(--brand-navy) !important;
    border-left: 4px solid var(--brand-red);
}
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }

.main .block-container { padding: 2rem 2.5rem 3rem; max-width: 960px; }

.page-header {
    background: linear-gradient(135deg, var(--brand-navy) 0%, #1a3550 100%);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow);
}
.page-header h1 { font-size: 1.6rem; font-weight: 900; margin: 0; color: #fff; }
.page-header p  { margin: .2rem 0 0; color: #94A3B8; font-size: .88rem; }
.badge-pro {
    background: var(--brand-red);
    color: #fff;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .1em;
    padding: .25em .8em;
    border-radius: 20px;
    text-transform: uppercase;
    white-space: nowrap;
}

.card {
    background: var(--brand-card);
    border-radius: var(--radius);
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--brand-border);
}
.card-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--brand-navy);
    border-bottom: 2px solid var(--brand-red);
    padding-bottom: .45rem;
    margin-bottom: 1rem;
}

.metric-row { display: flex; gap: 1rem; margin-bottom: 1.4rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 160px;
    background: var(--brand-card);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    box-shadow: var(--shadow);
    border-top: 4px solid var(--brand-red);
    text-align: center;
}
.metric-card .metric-value { font-size: 2rem; font-weight: 900; color: var(--brand-navy); line-height: 1; }
.metric-card .metric-label { font-size: .82rem; color: var(--brand-muted); margin-top: .3rem; }

.mobile-frame {
    max-width: 400px;
    margin: 0 auto;
    background: #fff;
    border-radius: 28px;
    box-shadow: 0 8px 48px rgba(13,27,42,.18);
    overflow: hidden;
    border: 3px solid var(--brand-navy);
}
.mobile-topbar {
    background: var(--brand-navy);
    padding: .85rem 1.4rem;
    display: flex;
    align-items: center;
    gap: .6rem;
}
.mobile-topbar .dot { width:9px; height:9px; border-radius:50%; }
.mobile-topbar .app-name { font-weight: 700; font-size: .95rem; color: #fff; flex: 1; text-align: center; }
.mobile-body { padding: 1.4rem 1.3rem 1.8rem; }

.points-pill {
    display: inline-block;
    background: var(--brand-navy);
    color: var(--brand-gold);
    font-weight: 700;
    font-size: .9rem;
    padding: .35em 1.1em;
    border-radius: 20px;
    margin-top: .6rem;
}

.json-box {
    background: #0D1B2A;
    color: #A8FF78;
    font-family: 'Courier New', monospace;
    font-size: .85rem;
    padding: 1rem 1.2rem;
    border-radius: 10px;
    direction: ltr;
    text-align: left;
    margin-top: .7rem;
}

label { direction: rtl; text-align: right; }
.stTextInput>div>div>input,
.stSelectbox>div>div { direction: rtl; text-align: right; }
hr { border-color: var(--brand-border); margin: 1rem 0; }
.stAlert { direction: rtl; text-align: right; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size:2rem;">🔩</div>
        <div style="font-size:1.25rem; font-weight:900; color:#fff; letter-spacing:.04em;">DOMICILE</div>
        <div style="font-size:.72rem; color:#94A3B8; letter-spacing:.15em; text-transform:uppercase;">Pro-Link</div>
    </div>
    <hr style="border-color:#2D3748; margin:.5rem 0 1.2rem;">
    """, unsafe_allow_html=True)

    view = st.radio(
        "ניווט",
        ["👷 חוויית הנגר", "📊 לוח ניהול"],
        label_visibility="collapsed",
    )

    st.markdown("""
    <hr style="border-color:#2D3748; margin:1.5rem 0 1rem;">
    <div style="font-size:.75rem; color:#4A5568; text-align:center;">
        גרסה 1.0 · סביבת הדגמה<br>
        <span style="color:#C0392B;">● </span>מחובר לענן
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — CARPENTER (mobile)
# ══════════════════════════════════════════════════════════════════════════════
if view == "👷 חוויית הנגר":

    st.markdown("""
    <div class="page-header">
        <div>
            <h1>👷 חוויית הנגר</h1>
            <p>ממשק האפליקציה הנגרית – מבט מנייד</p>
        </div>
        <span class="badge-pro">MOBILE VIEW</span>
    </div>
    """, unsafe_allow_html=True)

    _, col_c, _ = st.columns([0.5, 2, 0.5])
    with col_c:
        st.markdown('<div class="mobile-frame">', unsafe_allow_html=True)
        st.markdown("""
        <div class="mobile-topbar">
            <div class="dot" style="background:#EF4444;"></div>
            <div class="dot" style="background:#FBBF24;"></div>
            <div class="dot" style="background:#34D399;"></div>
            <div class="app-name">🔩 Pro-Link</div>
        </div>
        <div class="mobile-body">
        """, unsafe_allow_html=True)

        # ── Registration ──
        st.markdown('<div class="card-title">📋 הצטרפות לתוכנית</div>', unsafe_allow_html=True)
        with st.form("onboarding_form"):
            name     = st.text_input("שם מלא", placeholder="ישראל ישראלי")
            shop     = st.text_input("שם הנגרייה", placeholder="נגרות ישראלי בע״מ")
            city     = st.selectbox("עיר", ["תל אביב", "ירושלים", "חיפה", "ראשון לציון", "נתניה", "באר שבע", "פתח תקווה", "אחר"])
            supplier = st.selectbox("בית מסחר רכישה", ["ACE", "יינות ביתן כלים", "כפר הנגרות", "לידור סיטונאות", "אחר"])
            submitted = st.form_submit_button("✅ הצטרף לתוכנית", use_container_width=True)
            if submitted and name and shop:
                st.success(f"ברוך הבא, {name}! חשבונך נוצר.")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Invoice upload ──
        st.markdown('<div class="card-title">📸 העלאת חשבונית</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("בחר קובץ", type=["jpg", "jpeg", "png", "pdf"], label_visibility="collapsed")

        if uploaded:
            with st.spinner("מנתח עם AI..."):
                time.sleep(2.2)
            result = {
                "מוצר": "מסילות מגירה Soft-Close",
                "כמות": 50,
                "נקודות_שנצברו": 500,
                "בית_מסחר": "ACE"
            }
            st.markdown(f"""
            <div style="margin-top:.5rem;">
                <div style="color:#27AE60; font-weight:700; font-size:.92rem;">✅ ניתוח הושלם!</div>
                <div class="json-box">{json.dumps(result, ensure_ascii=False, indent=2)}</div>
                <div class="points-pill">🏅 +500 נקודות נצברו!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94A3B8; font-size:.85rem;">העלה חשבונית לקבלת נקודות אוטומטית.</div>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — MANAGEMENT DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
else:

    st.markdown("""
    <div class="page-header">
        <div>
            <h1>📊 לוח ניהול</h1>
            <p>מבט כולל על קהילת הנגרים · בזמן אמת</p>
        </div>
        <span class="badge-pro">ADMIN VIEW</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Metrics ──
    st.markdown("""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">847</div>
            <div class="metric-label">🔩 נגרים פעילים</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.1rem; padding-top:.5rem;">מסילות Soft-Close</div>
            <div class="metric-label">🏆 מוצר מוביל</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:#D4AC0D;">₪2.4M</div>
            <div class="metric-label">📦 הכנסות מזוהות (Q1)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.1rem; padding-top:.5rem;">ACE</div>
            <div class="metric-label">🏪 בית מסחר מוביל</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CRM Table with supplier filter ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">👥 נגרים רשומים – פילוח לפי בית מסחר</div>', unsafe_allow_html=True)

    crm_data = {
        "שם":           ["יוסי כהן",  "אמיר לוי",   "דוד בן-דוד", "מוחמד עלי", "ניר שפירא",   "אלי מזרחי",  "תמי גולן",       "ראם קדוש"],
        "עיר":          ["תל אביב",   "חיפה",        "ירושלים",    "נצרת",       "ראשון לציון", "באר שבע",    "פתח תקווה",      "נתניה"],
        "בית מסחר":     ["ACE",       "כפר הנגרות", "לידור",      "ACE",        "יינות ביתן",  "כפר הנגרות", "לידור",          "אחר"],
        "רכישה אחרונה": ["15/04/25",  "10/04/25",    "02/04/25",   "28/03/25",   "25/03/25",    "20/03/25",   "01/03/25",       "14/02/25"],
        "סה״כ נקודות":  [4500,        3200,          2800,         2100,         1950,          1700,         800,              420],
        "סטטוס":        ["פעיל",      "פעיל",        "פעיל",       "פעיל",       "פעיל",        "פעיל",       "דורש תשומת לב", "דורש תשומת לב"],
    }
    df = pd.DataFrame(crm_data)

    suppliers = ["הכל"] + sorted(df["בית מסחר"].unique().tolist())
    selected_sup = st.selectbox("סנן לפי בית מסחר", suppliers, label_visibility="collapsed")
    df_show = df if selected_sup == "הכל" else df[df["בית מסחר"] == selected_sup]

    st.dataframe(df_show, use_container_width=True, height=300, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Charts ──
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🏪 נגרים לפי בית מסחר</div>', unsafe_allow_html=True)
        sup_df = pd.DataFrame({
            "בית מסחר": ["ACE", "כפר הנגרות", "לידור", "יינות ביתן", "אחר"],
            "נגרים":    [280,   210,           175,     130,           52]
        })
        st.bar_chart(sup_df.set_index("בית מסחר"), color="#C0392B", height=210)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📦 מוצרים מובילים</div>', unsafe_allow_html=True)
        prod_df = pd.DataFrame({
            "מוצר":    ["Soft-Close", "ציר הידראולי", "ידיות Al", "Push-to-Open", "Full-Ext"],
            "יחידות":  [1240,         980,            760,        540,            390]
        })
        st.bar_chart(prod_df.set_index("מוצר"), color="#0D1B2A", height=210)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Supplier × Product breakdown ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔍 מוצר מוביל לפי בית מסחר</div>', unsafe_allow_html=True)
    breakdown_data = {
        "בית מסחר":   ["ACE",              "ACE",           "כפר הנגרות",    "כפר הנגרות",     "לידור",           "לידור",         "יינות ביתן",   "יינות ביתן"],
        "מוצר":       ["Soft-Close",        "ציר הידראולי", "Soft-Close",     "Full-Extension", "ידיות אלומיניום", "Push-to-Open", "Soft-Close",   "ציר הידראולי"],
        "יחידות":     [520,                 310,            280,              195,              210,               175,            180,            130],
        "נגרים":      [280,                 280,            210,              210,              175,               175,            130,            130],
    }
    bd_df = pd.DataFrame(breakdown_data)
    st.dataframe(bd_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
