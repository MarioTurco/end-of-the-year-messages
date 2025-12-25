import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import uuid

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
