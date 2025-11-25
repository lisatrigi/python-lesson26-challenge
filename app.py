import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_BASE_URL")

st.title("Recipe Manager")

# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def get_recipes():
    r = requests.get(f"{API_URL}/recipes")
    return r.json() if r.status_code == 200 else []

def get_categories():
    r = requests.get(f"{API_URL}/categories")
    return r.json() if r.status_code == 200 else []

def create_recipe(payload):
    return requests.post(f"{API_URL}/recipes", json=payload)

def update_recipe(recipe_id, payload):
    return requests.put(f"{API_URL}/recipes/{recipe_id}", json=payload)

def delete_recipe(recipe_id):
    return requests.delete(f"{API_URL}/recipes/{recipe_id}")

def create_category(payload):
    return requests.post(f"{API_URL}/categories", json=payload)

def update_category(category_id, payload):
    return requests.put(f"{API_URL}/categories/{category_id}", json=payload)

def delete_category(category_id):
    return requests.delete(f"{API_URL}/categories/{category_id}")

# -------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Manage Recipes", "Manage Categories"]
)

# -------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------

if menu == "Dashboard":
    st.header("Dashboard Overview")

    st.subheader("Recipes")
    recipes = get_recipes()
    st.dataframe(pd.DataFrame(recipes) if recipes else pd.DataFrame())

    st.subheader("Categories")
    categories = get_categories()
    st.dataframe(pd.DataFrame(categories) if categories else pd.DataFrame())

# -------------------------------------------------------
# MANAGE RECIPES
# -------------------------------------------------------

elif menu == "Manage Recipes":
    st.header("Manage Recipes")

    categories = get_categories()
    category_map = {c["name"]: c["id"] for c in categories}

    # ------------ Add Recipe ------------
    st.subheader("Add New Recipe")

    title = st.text_input("Title")
    cuisine = st.text_input("Cuisine")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    category_name = st.selectbox("Category", list(category_map.keys()) if category_map else ["No categories"])

    if st.button("Create Recipe"):
        payload = {
            "title": title,
            "cuisine": cuisine,
            "difficulty": difficulty,
            "category_id": category_map.get(category_name)
        }
        r = create_recipe(payload)
        st.success("Recipe created!") if r.status_code == 200 else st.error(r.text)

    st.write("---")

    # ------------ Edit/Delete Recipes ------------
    st.subheader("Edit or Delete Recipes")
    recipes = get_recipes()

    if recipes:
        recipe_map = {r["title"]: r for r in recipes}
        selected_title = st.selectbox("Select Recipe", list(recipe_map.keys()))

        rec = recipe_map[selected_title]

        new_title = st.text_input("New Title", rec["title"])
        new_cuisine = st.text_input("New Cuisine", rec["cuisine"])
        new_difficulty = st.selectbox(
            "New Difficulty",
            ["Easy", "Medium", "Hard"],
            index=["Easy", "Medium", "Hard"].index(rec["difficulty"]) if rec["difficulty"] else 0
        )
        new_category_name = st.selectbox(
            "New Category",
            list(category_map.keys()) if category_map else []
        )

        if st.button("Update Recipe"):
            payload = {
                "title": new_title,
                "cuisine": new_cuisine,
                "difficulty": new_difficulty,
                "category_id": category_map[new_category_name]
            }
            update_recipe(rec["id"], payload)
            st.success("Recipe updated!")

        if st.button("Delete Recipe"):
            delete_recipe(rec["id"])
            st.error("Recipe deleted.")

    else:
        st.info("No recipes found.")

# -------------------------------------------------------
# MANAGE CATEGORIES
# -------------------------------------------------------

elif menu == "Manage Categories":
    st.header("Manage Categories")

    # ------------ Add Category ------------
    st.subheader("Add Category")
    new_cat = st.text_input("New Category Name")

    if st.button("Create Category"):
        r = create_category({"name": new_cat})
        st.success("Category created!") if r.status_code == 200 else st.error(r.text)

    st.write("---")

    # ------------ Edit/Delete Category ------------
    st.subheader("Edit or Delete Category")
    categories = get_categories()

    if categories:
        category_map = {c["name"]: c for c in categories}
        selected_cat = st.selectbox("Select Category", list(category_map.keys()))

        cat = category_map[selected_cat]
        updated_name = st.text_input("New Name", cat["name"])

        if st.button("Update Category"):
            update_category(cat["id"], {"name": updated_name})
            st.success("Category updated!")

        if st.button("Delete Category"):
            delete_category(cat["id"])
            st.error("Category deleted.")
    else:
        st.info("No categories available.")

