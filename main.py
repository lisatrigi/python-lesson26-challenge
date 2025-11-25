from fastapi import FastAPI
from typing import List
from models import (
    Category, CategoryOut,
    Recipe, RecipeOut
)
from database import get_connection, init_db

app = FastAPI(title="Recipe Manager API")

init_db()

# -------------------------------------------------------
# CATEGORY ENDPOINTS
# -------------------------------------------------------

@app.get("/categories", response_model=List[CategoryOut])
def get_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/categories", response_model=CategoryOut)
def create_category(category: Category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories (name) VALUES (?)", (category.name,))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return CategoryOut(id=cid, **category.dict())

@app.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category: Category):
    conn = get_connection()
    conn.execute(
        "UPDATE categories SET name=? WHERE id=?", 
        (category.name, category_id)
    )
    conn.commit()
    conn.close()
    return CategoryOut(id=category_id, **category.dict())

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM categories WHERE id=?", (category_id,))
    conn.commit()
    conn.close()
    return {"message": "Category deleted"}

# -------------------------------------------------------
# RECIPE ENDPOINTS
# -------------------------------------------------------

@app.get("/recipes", response_model=List[RecipeOut])
def get_recipes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM recipes").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/recipes", response_model=RecipeOut)
def create_recipe(recipe: Recipe):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO recipes (title, cuisine, difficulty, category_id)
        VALUES (?, ?, ?, ?)
    """, (recipe.title, recipe.cuisine, recipe.difficulty, recipe.category_id))
    conn.commit()
    rid = c.lastrowid
    conn.close()
    return RecipeOut(id=rid, **recipe.dict())

@app.put("/recipes/{recipe_id}", response_model=RecipeOut)
def update_recipe(recipe_id: int, recipe: Recipe):
    conn = get_connection()
    conn.execute("""
        UPDATE recipes 
        SET title=?, cuisine=?, difficulty=?, category_id=?
        WHERE id=?
    """, (recipe.title, recipe.cuisine, recipe.difficulty, recipe.category_id, recipe_id))
    conn.commit()
    conn.close()
    return RecipeOut(id=recipe_id, **recipe.dict())

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM recipes WHERE id=?", (recipe_id,))
    conn.commit()
    conn.close()
    return {"message": "Recipe deleted"}
