import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import uuid
from st_supabase_connection import SupabaseConnection
import math 
import yaml
import streamlit as st

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
        if st.button(
            "⬅ Previous",
            disabled=page == 0,
            key=f"{page_key}_prev"
        ):
            st.session_state[page_key] -= 1

    with col2:
        if st.button(
            "Next ➡",
            disabled=page >= total_pages - 1,
            key=f"{page_key}_next"
        ):
            st.session_state[page_key] += 1

def get_or_create_anon_id():
    """
    Returns a persistent anonymous user ID stored in the browser.

    - Reads anon_id from localStorage
    - If not present, generates a UUID
    - Saves it back to localStorage
    """

    # Try to read anon_id from browser localStorage
    anon_id = streamlit_js_eval(
        js_expressions="localStorage.getItem('anon_id')"
    )
    new_user = False
    if not anon_id:
        new_user = True
        # Generate a new anon_id
        anon_id = str(uuid.uuid4())

        # Save it in localStorage
        streamlit_js_eval(
            js_expressions=f"localStorage.setItem('anon_id', '{anon_id}')"
        )

    return anon_id, new_user

def user_has_message(_conn:SupabaseConnection, anon_id: str) -> bool:
    res = (
        _conn.table("messages")
        .select("anon_id")
        .eq("anon_id", anon_id)
        .limit(1)
        .execute()
    )
    return len(res.data) > 0