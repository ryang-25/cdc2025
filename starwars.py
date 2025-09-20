import streamlit as st
import pandas as pd

def load_and_clean_data():
    df = pd.read_csv('Pop_culture.csv')
    
    df = df.rename(columns={
        "fav_heroe": "fav_hero"  # correct the spelling
    })

    categories = ["fav_hero","fav_villain","fav_film","fav_soundtrack","fav_spaceship","fav_planet","fav_robot"]
    # Clean + standardize data
    return df, categories

def get_user_preferences(df, categories):
    st.header("Compare your Star Wars favorites!")
    user_prefs = {}
    for col in categories:
        if col.endswith('_id'):
            continue # Skip ID columns
        
        # Grab unique options for each category
        options = sorted(df[col].dropna().unique())
        user_prefs[col] = st.selectbox(f"Select your favorite {col.replace('fav_', '').replace('_', ' ')}:", options)
    return user_prefs

def main():
    df, categories = load_and_clean_data()
    prefs = get_user_preferences(df, categories)

    print("\n✅ User preferences:")
    for k, v in prefs.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()

df = pd.read_csv("Pop_Culture.csv") 
    # Reusable function for each category
def bar_counts_streamlit(df: pd.DataFrame, col: str, title: str):
    # Count responses in this column
    counts = df[col].value_counts(dropna=False).rename_axis(col).reset_index(name="count")

    # Scale counts to thousands so the axis reads 1, 2, 3...
    counts["thousands"] = counts["count"] / 1000.0

    # Sort for nicer bars
    counts = counts.sort_values("count", ascending=False)

    # Set index = category so Streamlit uses it as x-axis
    counts = counts.set_index(col)

    # Display
    st.subheader(title)
    st.bar_chart(data=counts, y="thousands", use_container_width=True)
    st.caption("Y-axis is in thousands.")

# Use the function for each column
bar_counts_streamlit(df, "fav_hero", "Hero Choices")
bar_counts_streamlit(df, "fav_villain", "Villain Choices")
bar_counts_streamlit(df, "fav_film", "Film Choices")
bar_counts_streamlit(df, "fav_soundtrack", "Soundtrack Choices")
bar_counts_streamlit(df, "fav_spaceship", "Spaceship Choices")
bar_counts_streamlit(df, "fav_planet", "Planet Choices")
bar_counts_streamlit(df, "fav_robot", "Robot Choices")