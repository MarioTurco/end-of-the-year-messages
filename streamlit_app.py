import streamlit as st
from st_supabase_connection import SupabaseConnection
from utils import get_or_create_anon_id

MAX_CHARACTERS = 200

st.set_page_config(page_title="New Year's resolution", page_icon="🎫")
st.title("🎫 New Year's resolution")

st.write(
    """
    🎉 Write your New Year’s resolution and join the collective goal-setting fun 🎊
No accounts, no personal data — just anonymous insights and good vibes.
    """
)

st.session_state.anon_id, st.session_state.new_user = get_or_create_anon_id()
st.session_state.sb_conn = st.connection("supabase",type=SupabaseConnection)


st.header("Write a New Year's resolution")

txt = st.text_area(label="New Year's resolution", max_chars=MAX_CHARACTERS, placeholder="Write your New Year's resolution")


