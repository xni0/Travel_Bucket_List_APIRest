from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional


# APP CONFIGURATION
app = FastAPI(
    title="User Management API",
    description="Simplified API for user management only (in-memory)",
    version="1.0.0"
)


# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows connection from any origin (e.g., localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DATA MODELS
class User(BaseModel):
    # ID is optional so it's not required when creating from React
    id: Optional[int] = None 
    name: str
    surname: str
    email: str
    age: Optional[int] = None


# FAKE DATABASE (IN MEMORY)
users_fake_db = [
    User(id=1, name="Vicent", surname="Foo", email="vicent@example.com", age=30),
    User(id=2, name="Lucilene", surname="Bar", email="lucilene@example.com", age=25),
    User(id=3, name="Pepe", surname="Gotera", email="pepe@example.com", age=40),
]


# ENDPOINTS (ROUTES)
# Get all users
@app.get("/users", response_model=List[User], tags=["Users"])
def get_users():
    return users_fake_db

# Get a user by ID (UserDetail)
@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int):
    for user in users_fake_db:
        if user.id == user_id:
            return user
    # If not found, raise a real 404 error
    raise HTTPException(status_code=404, detail="User not found")

# Create a new user
@app.post("/users", response_model=User, tags=["Users"], status_code=201)
def create_user(user: User):
    # Automatically generate a new ID (highest + 1)
    if users_fake_db:
        new_id = max(u.id for u in users_fake_db) + 1
    else:
        new_id = 1
        
    user.id = new_id
    users_fake_db.append(user)
    return user

# Delete user 
@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int):
    for index, user in enumerate(users_fake_db):
        if user.id == user_id:
            users_fake_db.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

# Update user (PUT) 
@app.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users_fake_db):
        if user.id == user_id:
            # Keep the original ID, but update the rest
            updated_user.id = user_id
            users_fake_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Welcome endpoint
@app.get("/")
def root():
    return {
        "message": "User API is running",
        "docs": "Go to /docs to test the endpoints"
    }