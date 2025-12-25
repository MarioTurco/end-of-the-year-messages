import streamlit as st
from st_supabase_connection import SupabaseConnection
from utils import get_or_create_anon_id

MAX_CHARACTERS = 200

st.set_page_config(page_title="End of the year messages", page_icon="🎫")
st.title("🎫 End of the year messages")

st.write(
    """
    🎉 One New Year’s resolution. Totally anonymous.
    Let’s see what everyone is aiming for this year!
    """
)

st.session_state.anon_id, st.session_state.new_user = get_or_create_anon_id()
st.session_state.sb_conn = st.connection("supabase",type=SupabaseConnection)


st.header("Write a new message")

txt = st.text_area(label="Message", max_chars=200)

st.write(f"{len(txt)}/{MAX_CHARACTERS} characters.")
