import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="108 Japa Counter", layout="centered")

# ---------------- HELPERS ----------------
DEVANAGARI_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")
def to_devanagari(n: int) -> str:
    return str(n).translate(DEVANAGARI_DIGITS)

# ---------------- STATE ----------------
if "done" not in st.session_state:
    st.session_state.done = [False] * 108

completed = sum(st.session_state.done)

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style="text-align:center; margin-top:32px;">
      <div style="font-size:48px; line-height:1.2;">ॐ</div>
      <div style="font-size:28px; font-weight:700;">108 Japa Counter</div>
      <div style="opacity:.75; font-size:15px;">Tap a bead to mark your japa</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- PROGRESS ----------------
st.markdown(
    f"""
    <div style="text-align:center; margin-top:14px; font-size:18px;">
      <span style="
        padding:8px 16px;
        border-radius:999px;
        background:rgba(156,39,176,.10);
        border:1px solid rgba(156,39,176,.30);
      ">
        <b>{completed}</b> / <b>108</b> completed
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.progress(completed / 108)

# ---------------- STYLES ----------------
st.markdown(
    """
    <style>
      .block-container { max-width: 920px; padding-top: 12px; }

      /* Mala beads */
      div.stButton > button {
        width: 54px !important;
        height: 54px !important;
        border-radius: 999px !important;
        border: 1.6px solid rgba(106,27,154,.45) !important;
        background: radial-gradient(circle at 30% 30%, #ffffff, #f3e5f5) !important;
        box-shadow: 0 6px 14px rgba(0,0,0,.08) !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #3a0f4b !important;
        margin: 6px 4px !important;
        font-family: "Noto Serif Devanagari", "Mangal", "Georgia", serif !important;
      }

      /* Completed beads */
      div.stButton > button.japa-done {
        background: radial-gradient(circle at 30% 30%, #ba68c8, #4a148c) !important;
        color: white !important;
        border: 1.6px solid #4a148c !important;
        text-decoration: line-through !important;
      }

      /* Guru bead style (applies to centered column button) */
      .guru div.stButton > button {
        width: 64px !important;
        height: 64px !important;
        border-radius: 50% !important;
        border: 2px solid rgba(106,27,154,.8) !important;
        background: radial-gradient(circle at 30% 30%, #ffffff, #e1bee7) !important;
        box-shadow: 0 10px 24px rgba(0,0,0,.25) !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #4A148C !important;
        padding: 0 !important;
        line-height: 1 !important;
      }

      .guru div.stButton > button:hover {
        background: radial-gradient(circle at 30% 30%, #d1a6e0, #8e24aa) !important;
        color: white !important;
      }

      @media (max-width: 520px) {
        div.stButton > button { width: 48px !important; height: 48px !important; font-size: 16px !important; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- MALA GRID ----------------
cols_per_row = 12
for row in range(0, 108, cols_per_row):
    cols = st.columns(cols_per_row, gap="small")
    for j, col in enumerate(cols):
        idx = row + j
        if idx >= 108:
            break
        with col:
            if st.button(to_devanagari(idx + 1), key=f"bead_{idx}"):
                st.session_state.done[idx] = not st.session_state.done[idx]
                st.rerun()

# ---------------- APPLY DONE STYLING ----------------
done_labels = [to_devanagari(i + 1) for i, v in enumerate(st.session_state.done) if v]
st.markdown(
    f"""
    <script>
      const done = new Set({done_labels});
      document.querySelectorAll('div.stButton > button').forEach(b => {{
        if (done.has(b.innerText.trim())) b.classList.add('japa-done');
        else b.classList.remove('japa-done');
      }});
    </script>
    """,
    unsafe_allow_html=True,
)

# ---------------- GURU BEAD RESET (TRULY CENTERED) ----------------
left, center, right = st.columns([4, 1, 4])
with center:
    st.markdown("<div class='guru'>", unsafe_allow_html=True)
    if st.button("ॐ", key="guru_reset"):
        st.session_state.done = [False] * 108
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
