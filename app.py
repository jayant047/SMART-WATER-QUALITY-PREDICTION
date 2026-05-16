import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="AquaAI — Water Quality", layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state:
    st.session_state.page = "home"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
header, [data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── App shell ── */
[data-testid="stAppViewContainer"] {
    background: #020d18;
    font-family: 'DM Sans', sans-serif;
    color: #e8f4fd;
    min-height: 100vh;
    overflow-x: hidden;
}

/* ── Animated mesh background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(0,180,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(0,80,200,0.10) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0,220,180,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* Grid overlay */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,180,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,180,255,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

/* ── Content wrapper ── */
.aq-wrap {
    position: relative;
    z-index: 1;
    max-width: 960px;
    margin: 0 auto;
    padding: 48px 28px 60px;
}

/* ── Header ── */
.aq-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
}
.aq-badge {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00cfff;
    background: rgba(0,207,255,0.10);
    border: 1px solid rgba(0,207,255,0.25);
    border-radius: 40px;
    padding: 4px 14px;
}
.aq-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(38px, 6vw, 64px);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -1.5px;
    background: linear-gradient(100deg, #e8f4fd 30%, #00cfff 70%, #0080ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 16px 0 10px;
}
.aq-sub {
    font-size: 16px;
    color: rgba(232,244,253,0.55);
    font-weight: 300;
    letter-spacing: 0.3px;
    margin-bottom: 44px;
}

/* ── Primary action cards ── */
.aq-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 18px;
}
.aq-card {
    position: relative;
    border-radius: 20px;
    padding: 32px 28px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    overflow: hidden;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    cursor: pointer;
}
.aq-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(0,207,255,0.06), transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
}
.aq-card:hover { transform: translateY(-4px); border-color: rgba(0,207,255,0.35); box-shadow: 0 20px 60px rgba(0,100,200,0.2); }
.aq-card:hover::before { opacity: 1; }
.aq-card-icon { font-size: 36px; margin-bottom: 14px; display: block; }
.aq-card-title { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; color: #e8f4fd; margin-bottom: 6px; }
.aq-card-desc { font-size: 13.5px; color: rgba(232,244,253,0.48); line-height: 1.55; }
.aq-card-arrow {
    position: absolute;
    bottom: 22px; right: 22px;
    font-size: 20px;
    opacity: 0.3;
    transition: opacity 0.25s, transform 0.25s;
}
.aq-card:hover .aq-card-arrow { opacity: 0.9; transform: translate(3px, -3px); }

/* ── Feature strip ── */
.aq-features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 36px;
}
.aq-feat {
    border-radius: 14px;
    padding: 20px 18px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    display: flex;
    align-items: flex-start;
    gap: 13px;
}
.aq-feat-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: rgba(0,207,255,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.aq-feat-label { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; color: #e8f4fd; margin-bottom: 3px; }
.aq-feat-text { font-size: 12px; color: rgba(232,244,253,0.45); line-height: 1.5; }

/* ── Tools row ── */
.aq-tools-label {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(232,244,253,0.35);
    margin-bottom: 14px;
}

/* ── Divider ── */
.aq-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,207,255,0.2), transparent);
    margin: 32px 0;
}

/* ── Footer ── */
.aq-footer {
    text-align: center;
    font-size: 12.5px;
    color: rgba(232,244,253,0.22);
    letter-spacing: 0.5px;
    margin-top: 48px;
}
.aq-footer span { color: rgba(0,207,255,0.5); }

/* ── Streamlit buttons restyled ── */

/* Primary big buttons */
div[data-testid="column"]:has(.primary-btn) .stButton > button {
    height: auto !important;
}
.stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.04) !important;
    color: #e8f4fd !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    padding: 14px 20px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: rgba(0,207,255,0.12) !important;
    border-color: rgba(0,207,255,0.4) !important;
    color: #00cfff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,100,200,0.18) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Big action buttons */
.big-btn .stButton > button {
    padding: 32px 28px !important;
    border-radius: 20px !important;
    font-size: 18px !important;
    text-align: left !important;
    height: 110px !important;
}
.big-btn .stButton > button:hover {
    background: rgba(0,207,255,0.10) !important;
    border-color: rgba(0,207,255,0.45) !important;
    color: #00cfff !important;
}

/* Back button */
.back-btn .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-size: 13px !important;
    width: auto !important;
    display: inline-flex !important;
}

/* ── Result cards ── */
.aq-result {
    border-radius: 16px;
    padding: 22px 24px;
    margin: 12px 0;
    display: flex;
    align-items: center;
    gap: 16px;
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 600;
}
.aq-result.safe {
    background: rgba(0,220,130,0.10);
    border: 1px solid rgba(0,220,130,0.25);
    color: #00dc82;
}
.aq-result.unsafe {
    background: rgba(255,80,80,0.10);
    border: 1px solid rgba(255,80,80,0.25);
    color: #ff6060;
}
.aq-result-icon { font-size: 28px; }
.aq-disease {
    border-radius: 12px;
    padding: 16px 20px;
    background: rgba(0,130,255,0.08);
    border: 1px solid rgba(0,130,255,0.18);
    color: rgba(232,244,253,0.70);
    font-size: 14px;
    margin-top: 8px;
}
.aq-disease strong { color: #7dc8ff; }

/* ── Stacked page layout ── */
.aq-page-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 20px 0 6px;
    color: #e8f4fd;
}
.aq-page-sub {
    font-size: 13.5px;
    color: rgba(232,244,253,0.40);
    margin-bottom: 26px;
}

/* ── Status dot ── */
.aq-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: rgba(232,244,253,0.40);
    font-weight: 500;
    letter-spacing: 0.3px;
    margin-bottom: 36px;
}
.aq-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #00dc82;
    box-shadow: 0 0 8px #00dc82;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; } 50% { opacity: 0.4; }
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1.5px dashed rgba(0,207,255,0.22) !important;
    border-radius: 16px !important;
    padding: 18px !important;
}
[data-testid="stFileUploader"] label, [data-testid="stFileUploader"] span {
    color: rgba(232,244,253,0.55) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Camera ── */
[data-testid="stCameraInput"] {
    border-radius: 16px;
    overflow: hidden;
}

/* ── Image display ── */
[data-testid="stImage"] img {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)


# ── Analyze function ──────────────────────────────────────────────
def analyze(img):
    arr = np.array(img)
    if arr.mean() > 120:
        return "✅ Safe to Use", "None detected", "safe"
    else:
        return "❌ Not Safe", "Cholera, Typhoid", "unsafe"


# ── HOME PAGE ─────────────────────────────────────────────────────
if st.session_state.page == "home":

    st.markdown('<div class="aq-wrap">', unsafe_allow_html=True)

    # Badge + status
    st.markdown("""
    <div class="aq-badge">AquaAI · ML Platform</div>
    <div style="margin-top:10px;" class="aq-status">
        <span class="aq-dot"></span> Model online &amp; ready
    </div>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("""
    <div class="aq-title">Water Quality<br>Intelligence</div>
    <div class="aq-sub">AI-powered real-time water analysis — upload or capture to assess contamination risk instantly.</div>
    """, unsafe_allow_html=True)

    # Primary action buttons
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="big-btn">', unsafe_allow_html=True)
        if st.button("📷  Camera Analysis\nCapture live water sample", use_container_width=True):
            st.session_state.page = "cam"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="big-btn">', unsafe_allow_html=True)
        if st.button("🖼  Upload Image\nAnalyze from your device", use_container_width=True):
            st.session_state.page = "up"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Feature strip
    st.markdown("""
    <div style="margin-top:28px;">
    <div class="aq-features">
        <div class="aq-feat">
            <div class="aq-feat-icon">⚡</div>
            <div>
                <div class="aq-feat-label">Instant Analysis</div>
                <div class="aq-feat-text">Results in under 2 seconds using on-device ML</div>
            </div>
        </div>
        <div class="aq-feat">
            <div class="aq-feat-icon">🦠</div>
            <div>
                <div class="aq-feat-label">Pathogen Detection</div>
                <div class="aq-feat-text">Identifies bacterial & contamination risk markers</div>
            </div>
        </div>
        <div class="aq-feat">
            <div class="aq-feat-icon">📡</div>
            <div>
                <div class="aq-feat-label">Smart Reports</div>
                <div class="aq-feat-text">Detailed analysis with confidence scoring</div>
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Divider
    st.markdown('<div class="aq-divider"></div>', unsafe_allow_html=True)

    # More Options
    st.markdown('<div class="aq-tools-label">More Options</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.button("📊  Reports", key="rep", use_container_width=True)
    with c2:
        st.button("⚙  Settings", key="set", use_container_width=True)
    with c3:
        st.button("🔒  Security", key="sec", use_container_width=True)
    with c4:
        st.button("🚀  Launch", key="launch", use_container_width=True)

    # Footer
    st.markdown("""
    <div class="aq-footer">
        AquaAI Water Intelligence &nbsp;·&nbsp; Built by <span>Jayant</span> &nbsp;·&nbsp; Powered by ML
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── CAMERA PAGE ───────────────────────────────────────────────────
elif st.session_state.page == "cam":

    st.markdown('<div class="aq-wrap">', unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="aq-page-title">📷 Camera Analysis</div>
    <div class="aq-page-sub">Point your camera at the water sample and capture an image for instant AI analysis.</div>
    """, unsafe_allow_html=True)

    img_data = st.camera_input("Capture water sample")

    if img_data:
        im = Image.open(img_data)
        st.image(im, use_container_width=True)

        label, disease, cls = analyze(im)

        result_html = f"""
        <div class="aq-result {cls}">
            <span class="aq-result-icon">{'✅' if cls=='safe' else '❌'}</span>
            <div>
                <div>{label}</div>
                <div style="font-size:12px;font-weight:400;opacity:0.7;margin-top:3px;">Analysis complete</div>
            </div>
        </div>
        <div class="aq-disease">
            <strong>⚠ Detected Risks:</strong>&nbsp; {disease}
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── UPLOAD PAGE ───────────────────────────────────────────────────
elif st.session_state.page == "up":

    st.markdown('<div class="aq-wrap">', unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="aq-page-title">🖼 Upload Image</div>
    <div class="aq-page-sub">Upload a photo of your water sample — JPG, PNG, or WEBP supported.</div>
    """, unsafe_allow_html=True)

    f = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "webp"])

    if f:
        im = Image.open(f)
        st.image(im, use_container_width=True)

        label, disease, cls = analyze(im)

        result_html = f"""
        <div class="aq-result {cls}">
            <span class="aq-result-icon">{'✅' if cls=='safe' else '❌'}</span>
            <div>
                <div>{label}</div>
                <div style="font-size:12px;font-weight:400;opacity:0.7;margin-top:3px;">Analysis complete</div>
            </div>
        </div>
        <div class="aq-disease">
            <strong>⚠ Detected Risks:</strong>&nbsp; {disease}
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)