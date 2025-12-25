import streamlit as st
from st_supabase_connection import SupabaseConnection
from db.queries import get_resolutions, get_total_count, user_has_message, insert_resolution
from utils import get_or_create_anon_id, paginated_fetch, load_config, render_resolution_card
from form import resolution_form

config = load_config()

MAX_CHARACTERS = config.get('max_len', 400)
PAGE_SIZE = config.get('element_per_paginator_page', 400)
cookie_pwd = st.secrets["COOKIE_PASSWORD"]

st.set_page_config(page_title="New Year's resolution", page_icon="🎫")
st.title("🎫 New Year's resolution")

st.write(
    """
    🎉 Write your New Year’s resolution and join the collective goal-setting fun 🎊

    No accounts, no personal data — just anonymous insights and good vibes.
"""
)
with st.spinner('Loading user data'):
    st.session_state.anon_id = get_or_create_anon_id(cookie_password=cookie_pwd)
st.session_state.sb_conn = st.connection("supabase",type=SupabaseConnection)

st.write(st.session_state.anon_id)

if "has_submitted" not in st.session_state:
    st.session_state.has_submitted = user_has_message(
        anon_id=st.session_state.anon_id,
        _conn=st.session_state.sb_conn
    )

if st.session_state.has_submitted:
    st.success("🎉 You’ve already submitted your New Year’s resolution!")
    # resolution_form(max_chars=MAX_CHARACTERS, disabled=True)
    
else:
    data = resolution_form(max_chars=MAX_CHARACTERS)
    if data:
        insert_resolution(conn=st.session_state.sb_conn, anon_id=st.session_state.anon_id, **data)
        st.session_state.has_submitted = True

with st.spinner('Loading community resolutions'):
    st.subheader("Community resolutions 🎯")
    for resolution in paginated_fetch(
        fetch_fn=get_resolutions,
        count_fn=get_total_count,
        _conn=st.session_state.sb_conn,
        page_size=PAGE_SIZE,
        page_key="resolutions_page"
    ):
        render_resolution_card(resolution)