
from st_supabase_connection import SupabaseConnection
import streamlit as st 
from datetime import datetime 

CACHE_MINUTES=1


def get_resolutions(_conn:SupabaseConnection, limit=50, offset=0):
    res = (
        _conn.table("messages")
        .select("*")
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return res.data

@st.cache_data(ttl=60*CACHE_MINUTES)
def get_total_count(_conn):
    res = _conn.table("messages").select("anon_id", count="exact").execute()
    return res.count

def user_has_message(_conn:SupabaseConnection, anon_id: str) -> bool:
    res = (
        _conn.table("messages")
        .select("anon_id")
        .eq("anon_id", anon_id)
        .limit(1)
        .execute()
    )
    return len(res.data) > 0

def insert_resolution(conn, anon_id, message, age=None, country=None,
                      past_year_score=None, new_year_score=None,
                      resolution_category=None, completion_confidence=None,
                      motivation=None):
    """
    Insert a new New Year resolution into the 'messages' table.

    Parameters:
    -----------
    conn : Supabase client or DB connection object
        The connection used to interact with the database.
    anon_id : str
        Anonymous user identifier.
    message : str
        The resolution text.
    age : int, optional
    country : str, optional
    past_year_score : int, optional
    new_year_score : int, optional
    resolution_category : str, optional
    completion_confidence : int, optional
    motivation : str, optional

    Returns:
    --------
    dict
        The inserted row data returned from the DB.
    """
    data = {
        "anon_id": anon_id,
        "created_at": datetime.utcnow().isoformat(),
        "message": message,
        "age": age,
        "country": country,
        "past_year_score": past_year_score,
        "new_year_score": new_year_score,
        "resolution_category": resolution_category,
        "completion_confidence": completion_confidence,
        "motivation": motivation,
    }

    # Clean out None values to avoid inserting null if DB doesn't allow
    clean_data = {k: v for k, v in data.items() if v is not None}
    try:
        result = conn.table("messages").insert(clean_data).execute()

        # Ora puoi accedere a result.data tranquillamente
        return result.data
    except Exception as ex:
        print(f"Exception: {ex}")
        return None