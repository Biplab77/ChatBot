from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the JWT secret key from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Ensure SECRET_KEY is not None
if SECRET_KEY is None:
    raise ValueError("JWT_SECRET_KEY is not set. Please check your .env file.")

# Initialize HTTPBearer security scheme to extract Bearer tokens
security = HTTPBearer()

# Function to verify the token provided in the request
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not credentials:
        raise HTTPException(status_code=403, detail="Authorization token required")

    try:
        # Decode the JWT token using the secret key and HS256 algorithm
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        
        # Return the decoded payload
        return payload

    except jwt.ExpiredSignatureError:
        # If the token has expired, raise an HTTP 401 Unauthorized error
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        # If the token is invalid, raise an HTTP 401 Unauthorized error
        raise HTTPException(status_code=401, detail="Invalid token")
