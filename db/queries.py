
from st_supabase_connection import SupabaseConnection
import streamlit as st 

CACHE_MINUTES=1

@st.cache_data(ttl=60*CACHE_MINUTES)
def get_resolutions(_conn:SupabaseConnection, limit=10, offset=0):
    res = (
        _conn.table("messages")
        .select("message, created_at")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return res.data

@st.cache_data(ttl=60*CACHE_MINUTES)
def get_total_count(_conn):
    res = _conn.table("messages").select("anon_id", count="exact").execute()
    return res.count