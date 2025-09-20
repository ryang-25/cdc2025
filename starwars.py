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

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_hero = df['fav_hero']
st.bar_chart(data = fav_hero, x=options, y= numbers, x_label = "Hero Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_villain = df['fav_villain']
st.bar_chart(data = fav_villain, x=options, y= numbers, x_label = "Villain Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_film = df['fav_film']
st.bar_chart(data = fav_film, x=options, y= numbers, x_label = "Film Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_soundtrack = df['fav_soundtrack']
st.bar_chart(data = fav_soundtrack, x=options, y= numbers, x_label = "Soundtrack Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_spaceship = df['fav_spaceship']
st.bar_chart(data = fav_spaceship, x=options, y= numbers, x_label = "Spaceship Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_planet = df['fav_planet']
st.bar_chart(data = fav_planet, x=options, y= numbers, x_label = "Planet Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)

options = sorted(df[col].dropna().unique())
numbers = [1,2,3,4,5,6,7,8,9,10]
fav_robot = df['fav_robot']
st.bar_chart(data = fav_robot, x=options, y= numbers, x_label = "Robot Choices", y_label = "Amount of Inputs (In Thousands)", color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
