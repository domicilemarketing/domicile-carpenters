import streamlit as st
import pandas as pd
import time
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DOMICILE Pro-Link",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand CSS (RTL + DOMICILE palette) ───────────────────────────────────────
st.markdown("""
<style>
/* Google Fonts – Heebo (Hebrew-friendly) */
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;900&display=swap');

/* ── Root variables ── */
:root {
    --brand-navy:   #0D1B2A;
    --brand-red:    #C0392B;
    --brand-gold:   #D4AC0D;
    --brand-light:  #F4F6F9;
    --brand-card:   #FFFFFF;
    --brand-border: #E2E8F0;
    --brand-text:   #1A202C;
    --brand-muted:  #718096;
    --brand-active: #27AE60;
    --brand-warn:   #E67E22;
    --radius:       12px;
    --shadow:       0 4px 24px rgba(13,27,42,.10);
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Heebo', sans-serif !important;
    direction: rtl;
    text-align: right;
    background: var(--brand-light);
    color: var(--brand-text);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--brand-navy) !important;
    border-left: 4px solid var(--brand-red);
}
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 1.05rem; }

/* ── Main content padding ── */
.main .block-container { padding: 2rem 2.5rem 3rem; max-width: 1100px; }

/* ── Page header ── */
.page-header {
    background: linear-gradient(135deg, var(--brand-navy) 0%, #1a3550 100%);
    color: #fff !important;
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow);
}
.page-header h1 { font-size: 1.9rem; font-weight: 900; margin: 0; color: #fff; }
.page-header p  { margin: .25rem 0 0; color: #94A3B8; font-size: .95rem; }
.badge-pro {
    background: var(--brand-red);
    color: #fff;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .1em;
    padding: .2em .7em;
    border-radius: 20px;
    text-transform: uppercase;
    margin-right: .6rem;
}

/* ── Cards ── */
.card {
    background: var(--brand-card);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    margin-bottom: 1.4rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--brand-border);
}
.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--brand-navy);
    border-bottom: 2px solid var(--brand-red);
    padding-bottom: .55rem;
    margin-bottom: 1.1rem;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1.2rem; margin-bottom: 1.4rem; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 180px;
    background: var(--brand-card);
    border-radius: var(--radius);
    padding: 1.3rem 1.6rem;
    box-shadow: var(--shadow);
    border-top: 4px solid var(--brand-red);
    text-align: center;
}
.metric-card .metric-value {
    font-size: 2.1rem; font-weight: 900; color: var(--brand-navy); line-height: 1;
}
.metric-card .metric-label { font-size: .85rem; color: var(--brand-muted); margin-top: .35rem; }

/* ── Mobile frame ── */
.mobile-frame {
    max-width: 420px;
    margin: 0 auto;
    background: #fff;
    border-radius: 28px;
    box-shadow: 0 8px 48px rgba(13,27,42,.18);
    overflow: hidden;
    border: 3px solid var(--brand-navy);
}
.mobile-topbar {
    background: var(--brand-navy);
    color: #fff;
    padding: .9rem 1.4rem;
    display: flex;
    align-items: center;
    gap: .75rem;
}
.mobile-topbar .dot { width:10px; height:10px; border-radius:50%; }
.mobile-topbar .app-name { font-weight: 700; font-size: 1rem; color: #fff; flex: 1; text-align: center; }
.mobile-body { padding: 1.6rem 1.4rem; }

/* ── Status badges ── */
.status-active  { background:#D4EDDA; color:#155724; padding:.2em .7em; border-radius:20px; font-size:.82rem; font-weight:600; }
.status-warning { background:#FFF3CD; color:#856404; padding:.2em .7em; border-radius:20px; font-size:.82rem; font-weight:600; }

/* ── Points badge ── */
.points-pill {
    display: inline-block;
    background: var(--brand-navy);
    color: var(--brand-gold);
    font-weight: 700;
    font-size: .92rem;
    padding: .3em 1em;
    border-radius: 20px;
    margin-top: .5rem;
}

/* ── JSON result box ── */
.json-box {
    background: #0D1B2A;
    color: #A8FF78;
    font-family: 'Courier New', monospace;
    font-size: .88rem;
    padding: 1.1rem 1.3rem;
    border-radius: 10px;
    direction: ltr;
    text-align: left;
    margin-top: .8rem;
}

/* ── Streamlit form tweaks for RTL ── */
label { direction: rtl; text-align: right; }
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stSelectbox>div>div { direction: rtl; text-align: right; }

/* ── Dividers ── */
hr { border-color: var(--brand-border); margin: 1.2rem 0; }

/* ── Success / info boxes ── */
.stAlert { direction: rtl; text-align: right; }

/* ── Scrollbar (subtle) ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.5rem 0 1rem;">
        <div style="font-size:2.2rem;">🔩</div>
        <div style="font-size:1.3rem; font-weight:900; color:#fff; letter-spacing:.04em;">DOMICILE</div>
        <div style="font-size:.78rem; color:#94A3B8; letter-spacing:.15em; text-transform:uppercase;">Pro-Link Platform</div>
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
    <div style="font-size:.78rem; color:#4A5568; text-align:center;">
        גרסה 1.0 · סביבת הדגמה<br>
        <span style="color:#C0392B;">● </span>מחובר לענן
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — CARPENTER EXPERIENCE (mobile mock)
# ══════════════════════════════════════════════════════════════════════════════
if view == "👷 חוויית הנגר":

    st.markdown("""
    <div class="page-header">
        <div>
            <h1>👷 חוויית הנגר</h1>
            <p>סימולציה של ממשק האפליקציה הנגרית – מבט מנייד</p>
        </div>
        <span class="badge-pro">MOBILE VIEW</span>
    </div>
    """, unsafe_allow_html=True)

    col_phone, col_info = st.columns([1, 1], gap="large")

    with col_phone:
        # ── Mobile frame ──
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

        # ── STEP 1: Onboarding ──
        st.markdown('<div class="card-title">📋 הצטרפות לתוכנית</div>', unsafe_allow_html=True)

        with st.form("onboarding_form"):
            name = st.text_input("שם מלא", placeholder="ישראל ישראלי")
            shop = st.text_input("שם הנגרייה", placeholder="נגרות ישראלי בע״מ")
            city = st.selectbox("עיר", ["תל אביב", "ירושלים", "חיפה", "ראשון לציון", "נתניה", "באר שבע", "פתח תקווה", "אחר"])
            submitted = st.form_submit_button("✅ הצטרף לתוכנית", use_container_width=True)
            if submitted and name and shop:
                st.success(f"ברוך הבא, {name}! חשבונך נוצר בהצלחה.")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── STEP 2: Photo upload ──
        st.markdown('<div class="card-title">📸 העלאת חשבונית / תמונת התקנה</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("בחר קובץ", type=["jpg", "jpeg", "png", "pdf"], label_visibility="collapsed")

        if uploaded:
            with st.spinner("מנתח עם AI..."):
                time.sleep(2.2)

            result = {
                "Product": "מסילות מגירה soft-close",
                "Quantity": 50,
                "Points_Earned": 500
            }
            st.markdown(f"""
            <div style="margin-top:.5rem;">
                <div style="color:#27AE60; font-weight:700; font-size:.95rem;">✅ ניתוח הושלם!</div>
                <div class="json-box">{json.dumps(result, ensure_ascii=False, indent=2)}</div>
                <div class="points-pill">🏅 +500 נקודות נצברו!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#94A3B8; font-size:.88rem;">העלה תמונה או PDF של חשבונית / התקנה לקבלת נקודות אוטומטית.</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── STEP 3: Tech support ──
        st.markdown('<div class="card-title">💬 תמיכה טכנית</div>', unsafe_allow_html=True)
        question = st.text_area("שאל שאלה טכנית", placeholder="למשל: איך מכוונים מסילות soft-close לדלת שמינה 19מ\"מ?", height=100)
        if st.button("📨 שלח למנהל הקהילה", use_container_width=True):
            if question:
                st.success("שאלתך נשלחה! מנהל הקהילה יחזור אליך תוך 24 שעות.")
            else:
                st.warning("אנא כתוב שאלה לפני השליחה.")

        st.markdown('</div></div>', unsafe_allow_html=True)  # close mobile-body + mobile-frame

    with col_info:
        st.markdown("""
        <div class="card">
            <div class="card-title">🚀 יתרון תחרותי</div>
            <p style="color:#4A5568; font-size:.94rem; line-height:1.75;">
                בעוד <strong>תדיראן</strong> ו<strong>תמבור</strong> מוכרות מוצרים <em>ללא זיהוי הלקוח הסופי</em>,
                Pro-Link מאפשרת ל-DOMICILE לדעת בדיוק:
            </p>
            <ul style="color:#4A5568; font-size:.92rem; line-height:2; padding-right:1.2rem;">
                <li>🔍 <strong>מי</strong> הנגר שמתקין את המוצרים</li>
                <li>📍 <strong>איפה</strong> הוא פועל</li>
                <li>📦 <strong>מה</strong> הוא קונה ובאיזו תדירות</li>
                <li>🛠️ <strong>אילו בעיות</strong> הוא נתקל בהן</li>
            </ul>
        </div>

        <div class="card">
            <div class="card-title">📈 מסע הנגר</div>
            <div style="display:flex; flex-direction:column; gap:.7rem;">
                <div style="display:flex; align-items:center; gap:.8rem;">
                    <div style="width:32px; height:32px; border-radius:50%; background:#0D1B2A; color:#D4AC0D; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">1</div>
                    <div style="font-size:.92rem; color:#4A5568;">הצטרפות מהירה דרך האפליקציה</div>
                </div>
                <div style="display:flex; align-items:center; gap:.8rem;">
                    <div style="width:32px; height:32px; border-radius:50%; background:#0D1B2A; color:#D4AC0D; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">2</div>
                    <div style="font-size:.92rem; color:#4A5568;">צילום חשבונית → AI מזהה מוצרים</div>
                </div>
                <div style="display:flex; align-items:center; gap:.8rem;">
                    <div style="width:32px; height:32px; border-radius:50%; background:#0D1B2A; color:#D4AC0D; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">3</div>
                    <div style="font-size:.92rem; color:#4A5568;">צבירת נקודות ✦ הטבות בלעדיות</div>
                </div>
                <div style="display:flex; align-items:center; gap:.8rem;">
                    <div style="width:32px; height:32px; border-radius:50%; background:#C0392B; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">4</div>
                    <div style="font-size:.92rem; color:#4A5568;">DOMICILE רואה הכל בדאשבורד</div>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-title">💡 AI זיהוי מוצרים</div>
            <p style="color:#4A5568; font-size:.92rem; line-height:1.7;">
                מנוע ה-AI מזהה אוטומטית מוצרי DOMICILE מתוך חשבוניות ותמונות,
                ומייצר מיידית: שם מוצר, כמות, ונקודות לצבירה – <strong>ללא הקלדה ידנית</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)


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

    # ── Metric cards ──
    st.markdown("""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-value">847</div>
            <div class="metric-label">🔩 נגרים פעילים</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="font-size:1.2rem; padding-top:.4rem;">מסילות Soft-Close</div>
            <div class="metric-label">🏆 המוצר הפופולרי ביותר</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:#C0392B;">23</div>
            <div class="metric-label">🛠️ פניות תמיכה ממתינות</div>
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color:#D4AC0D;">₪2.4M</div>
            <div class="metric-label">📦 הכנסות מזוהות (Q1)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CRM Table ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">👥 ניהול קשרי נגרים (CRM)</div>', unsafe_allow_html=True)

    crm_data = {
        "שם": ["יוסי כהן", "אמיר לוי", "דוד בן-דוד", "מוחמד עלי", "ניר שפירא", "אלי מזרחי", "תמי גולן", "ראם קדוש"],
        "עיר": ["תל אביב", "חיפה", "ירושלים", "נצרת", "ראשון לציון", "באר שבע", "פתח תקווה", "נתניה"],
        "רכישה אחרונה": ["15/04/2025", "10/04/2025", "02/04/2025", "28/03/2025", "25/03/2025", "20/03/2025", "01/03/2025", "14/02/2025"],
        "סה״כ נקודות": [4500, 3200, 2800, 2100, 1950, 1700, 800, 420],
        "סטטוס": ["פעיל", "פעיל", "פעיל", "פעיל", "פעיל", "פעיל", "דורש תשומת לב", "דורש תשומת לב"],
    }
    df = pd.DataFrame(crm_data)

    def style_status(val):
        if val == "פעיל":
            return "background-color:#D4EDDA; color:#155724; font-weight:600; border-radius:20px; text-align:center;"
        return "background-color:#FFF3CD; color:#856404; font-weight:600; border-radius:20px; text-align:center;"

    styled_df = df.style.applymap(style_status, subset=["סטטוס"]) \
        .set_properties(**{"text-align": "right", "font-family": "Heebo, sans-serif"}) \
        .format({"סה״כ נקודות": "{:,}"}) \
        .set_table_styles([
            {"selector": "th", "props": [("background-color", "#0D1B2A"), ("color", "white"), ("font-family", "Heebo, sans-serif"), ("text-align", "right"), ("padding", "10px 16px")]},
            {"selector": "td", "props": [("padding", "10px 16px"), ("border-bottom", "1px solid #E2E8F0")]},
            {"selector": "tr:hover td", "props": [("background-color", "#F7FAFC")]},
        ])

    st.dataframe(df, use_container_width=True, height=310, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Bottom row: Charts + Actions ──
    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📦 מוצרים מובילים</div>', unsafe_allow_html=True)
        products_df = pd.DataFrame({
            "מוצר": ["מסילות Soft-Close", "ציר הידראולי", "ידיות אלומיניום", "מנגנון Push-to-Open", "מסילות Full-Extension"],
            "יחידות": [1240, 980, 760, 540, 390]
        })
        st.bar_chart(products_df.set_index("מוצר"), color="#C0392B", height=220)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🗺️ פיזור גיאוגרפי</div>', unsafe_allow_html=True)
        geo_df = pd.DataFrame({
            "עיר": ["ת״א", "חיפה", "ירושלים", "ר״ל", "ב״ש", "נתניה"],
            "נגרים": [210, 180, 150, 120, 105, 82]
        })
        st.bar_chart(geo_df.set_index("עיר"), color="#0D1B2A", height=220)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Support queue ──
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🛠️ תור פניות תמיכה טכנית</div>', unsafe_allow_html=True)
    support_data = {
        "נגר": ["יוסי כהן", "תמי גולן", "ראם קדוש"],
        "שאלה": [
            "איך מכוונים מסילות soft-close לחזית כבדה במיוחד?",
            "ציר הידראולי נסגר מהר מדי – יש אפשרות כוונון?",
            "Push-to-open לא מגיב אחרי לחיצה ראשונה",
        ],
        "זמן המתנה": ["2 שעות", "5 שעות", "1 יום"],
        "עדיפות": ["🔴 גבוהה", "🟡 בינונית", "🟡 בינונית"],
    }
    support_df = pd.DataFrame(support_data)
    st.dataframe(support_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
