import streamlit as st
import sqlite3
import json
from typing import List

# SQLite setup
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    continent TEXT,
    country_state TEXT,
    cuisine TEXT,
    url TEXT,
    rating REAL,
    total_time INTEGER,
    prep_time INTEGER,
    cook_time INTEGER,
    description TEXT,
    ingredients TEXT,
    instructions TEXT,
    nutrients TEXT,
    serves TEXT
)
''')
conn.commit()

st.title("📘 Recipe Uploader")

# Upload JSON file
uploaded_file = st.file_uploader("Upload a JSON file", type="json")

if uploaded_file is not None:
    try:
        raw_data = json.load(uploaded_file)
        st.success("✅ File loaded successfully!")

        for key, recipe in raw_data.items():
            cursor.execute('''
                INSERT INTO recipes (
                    title, continent, country_state, cuisine, url, rating,
                    total_time, prep_time, cook_time, description,
                    ingredients, instructions, nutrients, serves
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                recipe.get("title"),
                recipe.get("Contient"),
                recipe.get("Country_State"),
                recipe.get("cuisine"),
                recipe.get("URL"),
                recipe.get("rating"),
                recipe.get("total_time"),
                recipe.get("prep_time"),
                recipe.get("cook_time"),
                recipe.get("description"),
                json.dumps(recipe.get("ingredients")),
                json.dumps(recipe.get("instructions")),
                json.dumps(recipe.get("nutrients")),
                recipe.get("serves")
            ))
        conn.commit()
        st.success("🎉 Recipes saved to database!")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")

# Show stored recipes
st.subheader("📋 Stored Recipes")
cursor.execute("SELECT id, title, cuisine, rating FROM recipes ORDER BY id DESC")
rows = cursor.fetchall()

# Show stored recipes in a table
st.subheader("📋 Stored Recipes")

cursor.execute('SELECT id, title, cuisine, rating, total_time, serves FROM recipes ORDER BY id DESC')
rows = cursor.fetchall()

if rows:
    import pandas as pd
    df = pd.DataFrame(rows, columns=["ID", "Title", "Cuisine", "Rating", "Total Time", "Serves"])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No recipes found in the database.")
    
# st.map()

