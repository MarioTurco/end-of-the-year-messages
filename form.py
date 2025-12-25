import streamlit as st
from utils import load_config

config = load_config()

def resolution_form(max_chars:int, disabled: bool = False):
    st.subheader("✨ Your New Year’s Resolution")

    message = st.text_area(
        "What is your New Year’s resolution?",
        max_chars=max_chars,
        disabled=disabled,
        placeholder="e.g. Exercise consistently, learn a new skill..."
    )

    # Fo
    with st.form("resolution_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age (optional)",
                min_value=13,
                max_value=100,
                disabled=disabled
            )

            country = st.selectbox(
                "Country (optional)",
                options=config.get('countries', []),
                disabled=disabled
            )

        with col2:
            resolution_category = st.multiselect(
                "Resolution category",
                options=config.get('resolution_categories', []),
                disabled=disabled
            )

            motivation = st.multiselect(
                "Main motivation",
                options=config.get('motivations', []),
                disabled=disabled
            )

        st.markdown("### 📊 How do you feel?")
        col3, col4 = st.columns(2)
        with col3:
            past_year_score = st.slider(
                "How was your past year?",
                0, 5, 3,
                disabled=disabled
            )

        with col4:
            new_year_score = st.slider(
                "How do you expect the new year to be?",
                0, 5, 4,
                disabled=disabled
            )

        completion_confidence = st.slider(
            "How confident are you that you’ll complete this resolution?",
            0, 5, 3,
            disabled=disabled
        )

        submitted = st.form_submit_button(
            "🚀 Submit resolution",
            disabled=disabled
        )
    if disabled:
        return None
    
    
    if not submitted:
        return None
    
    if not resolution_category:
        st.error("Please select at least one resolution category.")
        return None
    
    if not motivation:
        st.error("Please select at least one motivation.")
        return None

    if not message.strip():
        st.error("Please write your resolution.")
        return None
    
    if submitted: 
        st.session_state.has_submitted = True
        st.success("Thanks for your submission!")

    return {
        "message": message.strip(),
        "age": age if age > 0 else None,
        "country": country or None,
        "resolution_category": resolution_category,
        "motivation": motivation,
        "past_year_score": past_year_score,
        "new_year_score": new_year_score,
        "completion_confidence": completion_confidence,
    }
