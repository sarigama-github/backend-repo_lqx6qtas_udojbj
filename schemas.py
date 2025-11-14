"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Lobster harvest & investing app schemas

class Harvest(BaseModel):
    """
    Lobster harvest logs
    Collection: "harvest"
    """
    harvest_date: dt.date = Field(..., description="Catch date")
    boat: str = Field(..., description="Vessel name/ID")
    location: str = Field(..., description="Fishing area / port")
    weight_kg: float = Field(..., gt=0, description="Total catch weight (kg)")
    price_per_kg: float = Field(..., ge=0, description="Dock price per kg ($)")
    notes: Optional[str] = Field(None, description="Optional notes")

class Investment(BaseModel):
    """
    Investment records for lobster operations
    Collection: "investment"
    """
    investor_name: str = Field(..., description="Investor full name")
    amount_usd: float = Field(..., gt=0, description="Amount invested (USD)")
    investment_date: dt.date = Field(..., description="Investment date")
    instrument: str = Field(..., description="Type (equipment, working-capital, revenue-share, etc.)")
    notes: Optional[str] = Field(None, description="Optional notes")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
