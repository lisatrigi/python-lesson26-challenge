from pydantic import BaseModel
from typing import Optional

# ---------------- CATEGORY ----------------
class Category(BaseModel):
    name: str

class CategoryOut(Category):
    id: int

# ---------------- RECIPES ----------------
class Recipe(BaseModel):
    title: str
    cuisine: Optional[str] = None
    difficulty: Optional[str] = None
    category_id: Optional[int] = None

class RecipeOut(Recipe):
    id: int
