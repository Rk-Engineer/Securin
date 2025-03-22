from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import sqlite3
import json
import os
from typing import Optional

app = FastAPI()

# DB setup
DB_FILE = "recipes.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

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

# 1st api used for upload :
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON files are accepted.")

    try:
        contents = await file.read()
        data = json.loads(contents)

        for key, recipe in data.items():
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

        return {"message": "Recipes uploaded and stored successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/recipes")
def get_all_recipes():
    cursor.execute('SELECT * FROM recipes ORDER BY id DESC')
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    recipes = [dict(zip(columns, row)) for row in rows]
    for recipe in recipes:
        recipe["ingredients"] = json.loads(recipe["ingredients"])
        recipe["instructions"] = json.loads(recipe["instructions"])
        recipe["nutrients"] = json.loads(recipe["nutrients"])
    return recipes


@app.get("/recipes/filter")
def filter_recipes(
    cuisine: Optional[str] = Query(None),
    country_state: Optional[str] = Query(None),
    continent: Optional[str] = Query(None)
):
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if cuisine:
        query += " AND cuisine = ?"
        params.append(cuisine)
    if country_state:
        query += " AND country_state = ?"
        params.append(country_state)
    if continent:
        query += " AND continent = ?"
        params.append(continent)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    recipes = [dict(zip(columns, row)) for row in rows]

    for recipe in recipes:
        recipe["ingredients"] = json.loads(recipe["ingredients"])
        recipe["instructions"] = json.loads(recipe["instructions"])
        recipe["nutrients"] = json.loads(recipe["nutrients"])

    return recipes
