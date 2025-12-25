import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import uuid
from st_supabase_connection import SupabaseConnection
import math 
import yaml
import streamlit as st
from datetime import datetime
from streamlit_cookies_manager import EncryptedCookieManager

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def paginated_fetch(
    fetch_fn: callable,
    count_fn: callable,
    _conn:SupabaseConnection,
    page_size:int=10,
    page_key:str="page"
):
    """
    Paginate data fetching and display with Previous/Next buttons in Streamlit.

    Parameters:
    -----------
    fetch_fn : callable
        Function to fetch a page of data. Must accept parameters:
        (_conn, limit, offset) and return a list (or iterable) of items.
    count_fn : callable
        Function to get the total count of items. Must accept parameter (_conn)
        and return an integer count.
    _conn : SupabaseConnection
        Database or connection object passed to fetch_fn and count_fn.
    page_size : int, optional
        Number of items per page (default is 10).
    page_key : str, optional
        Key used in `st.session_state` to keep track of the current page.
        Allows multiple independent paginators (default is "page").

    Yields:
    -------
    item : any
        Each item fetched from fetch_fn for the current page.

    Side effects:
    -------------
    Displays pagination buttons ("Previous" and "Next") and page indicator
    in Streamlit. Updates `st.session_state[page_key]` to track current page.

    Usage example:
    --------------
    for record in paginated_fetch(fetch_fn=get_data, count_fn=get_count, _conn=conn):
        st.write(record)
    """
    if page_key not in st.session_state:
        st.session_state[page_key] = 0

    total_items = count_fn(_conn)
    total_pages = max(1, math.ceil(total_items / page_size))

    if st.session_state[page_key] >= total_pages:
        st.session_state[page_key] = total_pages - 1
    if st.session_state[page_key] < 0:
        st.session_state[page_key] = 0

    page = st.session_state[page_key]
    offset = page * page_size

    data = fetch_fn(
        _conn=_conn,
        limit=page_size,
        offset=offset,
    )
    # Render data
    for item in data:
        yield item

    # Page indicator
    st.caption(f"Page {page + 1} of {total_pages}")

    col1, col2 = st.columns(2)

    with col1:
        prev_disabled = page == 0
        if st.button("⬅ Previous", disabled=prev_disabled, key=f"{page_key}_prev"):
            if not prev_disabled:
                st.session_state[page_key] = page - 1
                st.rerun()

    with col2:
        next_disabled = page >= total_pages - 1
        if st.button("Next ➡", disabled=next_disabled, key=f"{page_key}_next"):
            if not next_disabled:
                st.session_state[page_key] = page + 1
                st.rerun()

def get_or_create_anon_id(cookie_password):
    """
    Returns a persistent anonymous user ID stored in the browser.

    - Reads anon_id from localStorage
    - If not present, generates a UUID
    - Saves it back to localStorage
    """
    cookies = EncryptedCookieManager(prefix="new-year-resolution-mt", password=cookie_password)

    if not cookies.ready():
        st.stop()

    anon_id = cookies.get("anon_id")

    if anon_id is None:
        # Genera anon_id e salvalo nei cookie
        anon_id = str(uuid.uuid4())
        cookies["anon_id"] = anon_id
        cookies.save()

    st.session_state.anon_id = anon_id
    # Try to read anon_id from browser localStorage

    return anon_id


def render_resolution_card(resolution):
    """
    Render a New Year resolution with all related info in a clean, readable format.
    """
    created_at = resolution.get("created_at", "")
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at)
        except Exception:
            created_at = None

    date_str = created_at.strftime("%b %d, %Y") if created_at else "Unknown date"
    resolution_no = resolution.get("resolution_no", "x")
    with st.container():
        st.markdown(f"### 📝 Resolution {resolution_no}")
        st.write(resolution.get("message", "No message provided"))

        # Metadata row 1: Date, Age, Country
        cols1 = st.columns([1, 1, 1])
        with cols1[0]:
            st.caption(f"📅 Date: {date_str}")
        with cols1[1]:
            age = resolution.get("age", "Not disclosed")
            st.caption(f"🎂 Age: {age if age is not None else 'N/A'}")
        with cols1[2]:
            country = resolution.get("country", "Not disclosed")
            st.caption(f"🌍 Country: {country if country else 'N/A'}")

        # Metadata row 2: Category, Motivation
        resolution_categories = resolution.get("resolution_category", [])
        motivations = resolution.get("motivation", [])
        cols2 = st.columns([1, 1])
        with cols2[0]:
            st.caption(f"🏷️ Categories: {', '.join(resolution_categories) if resolution_categories else 'N/A'}")
        with cols2[1]:
            st.caption(f"🎯 Motivations: {', '.join(motivations) if motivations else 'N/A'}")


        # Metadata row 3: Old Year Flag, New Year Flag, Completion Confidence
        cols3 = st.columns([1, 1, 1])
        with cols3[0]:
            old_flag = resolution.get("past_year_score", "Not disclosed")
            st.caption(f"⬅️ Past Year: {old_flag if old_flag is not None else 'N/A'} / 5")
        with cols3[1]:
            new_flag = resolution.get("new_year_score", "Not disclosed")
            st.caption(f"➡️ New Year: {new_flag if new_flag is not None else 'N/A'} / 5")
        with cols3[2]:
            confidence = resolution.get("completion_confidence", "Not disclosed")
            st.caption(f"✅ Confidence: {confidence if confidence is not None else 'N/A'} / 5")

        st.divider()