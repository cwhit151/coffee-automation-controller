import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ----------------------------
# CONFIG YOU MUST SET
# ----------------------------
SHEET_ID = "1GVgRB_hgaRMQbOasCKfNugTcyhcdf9o37F9vAcf4ZiI"
WORKSHEET_NAME = "on/off"  # the tab name in your Google Sheet

# Cells for toggles (simple + reliable)
CELL_POSTING_ENABLED = "B2"   # coffee_ig_posting enabled value TRUE/FALSE
CELL_RECYCLE_ENABLED = "B3"   # coffee_recycling enabled value TRUE/FALSE

# Optional: labels shown in the UI
LABEL_POSTING = "Coffee IG Posting"
LABEL_RECYCLE = "Recycle Coffee Photos"


def get_gspread_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    return gspread.authorize(creds)


def read_bool(ws, cell):
    val = ws.acell(cell).value
    return str(val).strip().upper() == "TRUE"


def write_bool(ws, cell, enabled: bool):
    ws.update_acell(cell, "TRUE" if enabled else "FALSE")


st.set_page_config(page_title="Coffee Automation Controller", page_icon="☕", layout="centered")
st.title("☕ Coffee Automation Controller")
st.caption("Flip the switches. Make does the work.")

# Connect
try:
    gc = get_gspread_client()
    ws = gc.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
except Exception as e:
    st.error("Could not connect to Google Sheets. Check your secrets + Sheet ID + access sharing.")
    st.code(str(e))
    st.stop()

# Read current states
posting_enabled_now = read_bool(ws, CELL_POSTING_ENABLED)
recycle_enabled_now = read_bool(ws, CELL_RECYCLE_ENABLED)

# UI toggles
col1, col2 = st.columns(2)

with col1:
    posting_toggle = st.toggle(LABEL_POSTING, value=posting_enabled_now)

with col2:
    recycle_toggle = st.toggle(LABEL_RECYCLE, value=recycle_enabled_now)

# Save changes
changed = False

if posting_toggle != posting_enabled_now:
    write_bool(ws, CELL_POSTING_ENABLED, posting_toggle)
    changed = True

if recycle_toggle != recycle_enabled_now:
    write_bool(ws, CELL_RECYCLE_ENABLED, recycle_toggle)
    changed = True

if changed:
    st.success("✅ Updated!")
    st.rerun()

st.divider()

st.subheader("What Make should do")
st.markdown(
    """
- Your **Posting** scenario should *start by reading* the posting flag cell.
- Your **Recycle** scenario should *start by reading* the recycle flag cell.
- If the flag is FALSE → scenario stops immediately.
"""
)

st.info("Tip: Keep your Make scenarios scheduled. The toggle acts like a valve at the start.")


