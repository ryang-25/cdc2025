import pandas as pd

def load_and_clean_data():
    df = pd.read_csv('Pop_culture.csv')
    
    categories = ["review_id","fav_heroe","fav_villain","fav_film","fav_soundtrack","fav_spaceship","fav_planet","fav_robot"]
    # Clean data
    for col in categories:
        df[col] = df[col].str.strip().str.lower().str.replace(' ', '_', regex=False)


