import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components  # Import Streamlit components

if "page" not in st.session_state:
    st.session_state.page = "preferences"  # start page
if "prefs" not in st.session_state:
    st.session_state.prefs = None


def load_and_clean_data():
    df = pd.read_csv('Pop_Culture.csv')
    df = df.drop('review_id', axis=1) # Remove review_id
    df = df.rename(columns={
        "fav_heroe": "fav_hero"  # Correct the spelling
    })
    # Correct another spelling
    df["fav_soundtrack"] = df["fav_soundtrack"].replace("Accross the Stars", "Across the Stars")
    categories = df.columns.tolist()
    # Clean + standardize data
    return df, categories

def persist_data(df, categories):
    st.session_state['init'] = True
    st.session_state['df'] = df
    st.session_state['user_df'] = pd.DataFrame(columns=df.columns)
    st.session_state['categories'] = categories
    st.session_state['options'] = [df[column].unique() for column in df.columns]

def get_user_preferences():
    # Custom HTML goes here
    st.html("""
        <style>
        div.stElementContainer {
            width: 100%;
        }
        div[role="radiogroup"] {
            flex-direction: row;
            flex-wrap: wrap;
        }
        div[role="radiogroup"] label {
          flex: 1 1 calc(50% - 12px);
          margin: 0 auto;
        }
        div[role="radiogroup"] {
            gap: 12px;
        }
        input[type="radio"] + div {
            background: rgb(240, 242, 246);
            color: #000;
            border-radius: 8px;
            padding: 8px 18px;
            flex: 1 1 calc(50%);
        }
        input[type="radio"][tabindex="0"] + div {
            background: #4B9CD3;
            color: #FFF;
        }
        div[role="radiogroup"] label > div:first-child {
            display: none;
        }
    </style>
    """)

    st.header("Are you a real Star Wars fan?")
    st.text("Take this quiz to find out! You'll also see how you compare to other users!")

    categories = st.session_state['categories']
    options = st.session_state['options']
    user_prefs = {}
    with st.form('preferences_form'):
        for i, c in enumerate(categories):
            f_name = c.replace('fav_', '').replace('_', ' ')
            user_prefs[c] = st.radio(f'Select your favorite {f_name}', options[i])
        submitted = st.form_submit_button("Submit")

    if submitted:
        user_df = st.session_state['user_df']
        user_df.loc[len(user_df)] = user_prefs
        st.session_state.prefs = user_prefs
        st.session_state.page = "dashboard"
        st.rerun()


def bar_counts_streamlit(df: pd.DataFrame, col: str, title: str, user_choice: str):
        # Count responses in this column
        counts = df[col].value_counts(dropna=False).rename_axis(col).reset_index(name="count")

        # Calculate percentages
        total_count = counts["count"].sum()
        counts["percentage"] = (counts["count"] / total_count * 100).round(2)  # Calculate percentage and round to 2 decimals

        # Scale counts to thousands so the axis reads 1, 2, 3...
        counts["Thousands"] = counts["count"] / 1000.0

        # Highlight user's choice
        counts['highlight'] = counts[col] == user_choice

        x_names = {
            "fav_hero": "Hero",
            "fav_villain": "Villain",
            "fav_film": "Film",
            "fav_soundtrack": "Soundtrack",
            "fav_spaceship": "Spaceship",
            "fav_planet": "Planet",
            "fav_robot": "Robot"
        }

        chart = (alt.Chart(counts).mark_bar().encode(
            x=alt.X(col, sort="y", title=x_names.get(col, col)),
            y=alt.Y("Thousands", title="Responses (Thousands)"),
            color=alt.condition(
                alt.datum.highlight,
                alt.value("#1f77b4"),  # highlighted color
                alt.value("lightgray")  # default bar color
            ),
            tooltip=[col, "count", alt.Tooltip("percentage", title="Percentage (%)")],  # Add percentage to tooltip
        ))
        st.subheader(title)
        st.altair_chart(chart, use_container_width=True)

def dashboard_page(df, prefs):
    st.set_page_config(layout="wide", page_title="Dashboard")

    
    col1, col2, col3 = st.columns([4, 2, 4])

    with col1:
        st.markdown("### Dataset Favorites :)")
        st.text("How you compared to our dataset!")

        # Reusable function for each category
        graph_options = {
            "Favorite Hero": "fav_hero",
            "Favorite Villain": "fav_villain",
            "Favorite Film": "fav_film",
            "Favorite Soundtrack": "fav_soundtrack",
            "Favorite Spaceship": "fav_spaceship",
            "Favorite Planet": "fav_planet",
            "Favorite Robot": "fav_robot"
        }

        # Dropdown to select which graph to display
        selected_graph = st.selectbox("Select a category to view:", list(graph_options.keys()))
        col = graph_options[selected_graph]
        bar_counts_streamlit(df, col, selected_graph, prefs.get(col))

    
    with col3:
        st.markdown("### User Favorites")
        st.text('How you compared to our users!')

        # Reusable function for each category
        graph_options = {
            "Favorite Hero": "fav_hero",
            "Favorite Villain": "fav_villain",
            "Favorite Film": "fav_film",
            "Favorite Soundtrack": "fav_soundtrack",
            "Favorite Spaceship": "fav_spaceship",
            "Favorite Planet": "fav_planet",
            "Favorite Robot": "fav_robot"
        }

        # Dropdown to select which graph to display
        selected_graph = st.selectbox("Select a category to view:", list(graph_options.keys()), key="user_cat")
        col = graph_options[selected_graph]
        bar_counts_streamlit(st.session_state['user_df'], col, selected_graph, prefs.get(col))


    st.text('You can also take a look at our similarity map below!')

    components.html(open('visualize.html', 'r').read(), height=800)

def main():
    if 'init' not in st.session_state:
        df, categories = load_and_clean_data()
        persist_data(df, categories)
    else:
        df = st.session_state['df']
    if st.session_state.page == "preferences":
        get_user_preferences()
    else:
        prefs = st.session_state.get("prefs", None)
        dashboard_page(df, prefs)


if __name__ == "__main__":
    main()