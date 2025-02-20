from fastapi import FastAPI, Depends, HTTPException, Request, Header
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
import jwt
from dotenv import load_dotenv
from jwt.exceptions import DecodeError, ExpiredSignatureError
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"  # The algorithm for encoding the JWT

app = FastAPI()

# Create a Pydantic model to handle the login request data
class LoginRequest(BaseModel):
    username: str
    password: str

# Function to generate a JWT token
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=1)  # Set token expiration time
    to_encode = data.copy()
    to_encode.update({"exp": expire})  # Add expiration time to the token data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the JWT token
    print(f"Generated Token: {encoded_jwt}")
    return encoded_jwt

# Function to verify JWT token
def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format. Use 'Bearer <token>'")
    
    token = authorization.replace("Bearer ", "").strip()  # Extract the token correctly
    try:
        print(f"Token received: {token}")  # Print to verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Payload: {payload}")  # Debugging: Check the decoded payload
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dummy function to verify the username and password (replace with your own logic)
def verify_credentials(username: str, password: str):
    if username == "testuser" and password == "password":
        return True
    return False

@app.post("/login")
async def login(request: LoginRequest):
    # Verify the user's credentials
    if not verify_credentials(request.username, request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token
    access_token = create_access_token(data={"sub": request.username})

    # Return the access token to the user
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
    username = token["sub"]
    return {"message": f"Hello, {username}! You are authenticated."}