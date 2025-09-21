import streamlit as st
import pandas as pd
import altair as alt

if "page" not in st.session_state:
    st.session_state.page = "preferences"  # start page
if "prefs" not in st.session_state:
    st.session_state.prefs = None

def load_and_clean_data():
    df = pd.read_csv('Pop_culture.csv')
    
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    df = df.rename(columns={
        "fav_heroe": "fav_hero"  # correct the spelling
    })

    if "fav_soundtrack" in df.columns:
        df["fav_soundtrack"] = df["fav_soundtrack"].str.strip()
        df["fav_soundtrack"] = df["fav_soundtrack"].str.replace("Accross the Stars", "Across the Stars")

    categories = ["fav_hero","fav_villain","fav_film","fav_soundtrack","fav_spaceship","fav_planet","fav_robot"]
    # Clean + standardize data
    return df, categories

def get_user_preferences(df, categories):
    st.header("Compare your Star Wars favorites!")
    user_prefs = {}
    with st.form('preferences_form'):
        for col in categories:
            if col.endswith('_id'):
                continue # Skip ID columns
        
        # Grab unique options for each category
            options = sorted(df[col].dropna().unique())
            user_prefs[col] = st.selectbox(f"Select your favorite {col.replace('fav_', '').replace('_', ' ')}:", options)
        
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.session_state.prefs = user_prefs
        st.session_state.page = "dashboard"
    else:
        return None

def bar_counts_streamlit(df: pd.DataFrame, col: str, title: str, user_choice: str):
        # Count responses in this column
        counts = df[col].value_counts(dropna=False).rename_axis(col).reset_index(name="count")

        # Scale counts to thousands so the axis reads 1, 2, 3...
        counts["Thousands"] = counts["count"] / 1000.0

        # Highlight user's choice
        counts['highlight'] = counts[col] == user_choice

        chart = (alt.Chart(counts).mark_bar().encode(
            x=alt.X(col, sort="-y"),
            y=alt.Y("Thousands", title="Responses (Thousands)"),
            color=alt.condition(
                alt.datum.highlight,
                alt.value("#1f77b4"),  # highlighted color
                alt.value("lightgray"),  # default bar color
            ),
            tooltip=[col, "count"]
        )
    )
        st.subheader(title)
        st.altair_chart(chart, use_container_width=True)

def dashboard_page(df, prefs):
    st.markdown("<h1 style='text-align: left; color: #FF5733;'>Star Wars Favorites Dashboard</h1>", unsafe_allow_html=True)
    
    # Reusable function for each category

    # Use the function for each column
    bar_counts_streamlit(df, "fav_hero", "Hero Choices", prefs.get("fav_hero"))
    bar_counts_streamlit(df, "fav_villain", "Villain Choices", prefs.get("fav_villain"))
    bar_counts_streamlit(df, "fav_film", "Film Choices", prefs.get("fav_film"))
    bar_counts_streamlit(df, "fav_soundtrack", "Soundtrack Choices", prefs.get("fav_soundtrack"))
    bar_counts_streamlit(df, "fav_spaceship", "Spaceship Choices", prefs.get("fav_spaceship"))
    bar_counts_streamlit(df, "fav_planet", "Planet Choices", prefs.get("fav_planet"))
    bar_counts_streamlit(df, "fav_robot", "Robot Choices", prefs.get("fav_robot"))

def main():
    df, categories = load_and_clean_data()
    if st.session_state.page == "preferences":
        prefs = get_user_preferences(df, categories)
    else:
        prefs = st.session_state.get("prefs", None)
        dashboard_page(df, prefs)


if __name__ == "__main__":
    main()