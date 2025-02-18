import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import necessary modules
from fastapi import FastAPI, Depends, HTTPException  # FastAPI for creating API and Depends for dependency injection (e.g., token verification)
from pydantic import BaseModel  # BaseModel for data validation (Pydantic)
from chatbot import ChatBot  # Import the ChatBot class to handle chatbot interactions
from app.authentication import verify_token, create_access_token, verify_credentials  # Import authentication-related functions
from database import SessionLocal  # Import the database session for interacting with the database
from models.chat_history import ChatHistory  # Import the ChatHistory model to store chat records in the database
# Initialize the FastAPI app
app = FastAPI()


# Initialize the chatbot instance
chatbot = ChatBot()

# Define the structure of the incoming message using Pydantic
class Message(BaseModel):
    user_id: int  # User ID that sent the message
    text: str  # The text of the message sent by the user

# Define a Pydantic model for login requests
class LoginRequest(BaseModel):
    username: str
    password: str

# POST endpoint for login to authenticate user and return JWT token
@app.post("/login")
async def login(request: LoginRequest):
    # Verify the user's credentials
    if not verify_credentials(request.username, request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token for the user
    access_token = create_access_token(data={"sub": request.username})

    # Return the access token to the user
    return {"access_token": access_token, "token_type": "bearer"}

# Define a POST endpoint to handle chat interactions
@app.post("/chat")
async def chat(message: Message, token: str = Depends(verify_token)):
    """
    Handles the chat request. It validates the incoming message, gets the bot's response,
    and stores the conversation in the database.
    
    - `message`: The user input message validated by the `Message` model.
    - `token`: The user's authentication token, verified using the `verify_token` function.
    """
    # Get the chatbot's response for the user's message
    response = chatbot.get_response(message.text)

    # Create a new database session to store the chat
    db = SessionLocal()

    # Create a new record for the chat (both user message and bot response)
    new_chat = ChatHistory(
        user_id=message.user_id,  # Store the user ID
        user_message=message.text,  # Store the user's message
        bot_response=response  # Store the bot's response
    )

    # Add the new chat record to the database
    db.add(new_chat)
    db.commit()  # Commit the transaction to save the chat record
    db.refresh(new_chat)  # Refresh the session to get the latest data from the database
    db.close()  # Close the database session after use

    # Return the bot's response as the API response
    return {"response": response}

# Define a simple GET endpoint for the home page
@app.get("/")
def home():
    """
    A simple test endpoint to check if the server is running.
    It returns a welcome message.
    """
    return {"message": "LangChain Chatbot API"}

@app.get("/protected")
async def protected_route(token: str = Depends(verify_token)):
    # If the token is valid, this endpoint will execute
    return {"message": "This is a protected route"}