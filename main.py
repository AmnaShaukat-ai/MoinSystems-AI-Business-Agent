import json 
from fastapi import FastAPI
from agent.controller import agent_controller

app = FastAPI()

# Global dictionary to store chat history for each user/session.
# In a real app, you would use a database (like Redis or PostgreSQL) for this.
chat_memory = {}

@app.post("/business-agent")
def business_agent(req: dict):
    # Get the user's message and session_id (default to 'default_user' if not provided)
    user_message = req.get("message", "")
    session_id = req.get("session_id", "default_user")
    
    # Retrieve past conversation history for this session, or start a new one
    history = chat_memory.get(session_id, [])
    
    # Call the agent controller and pass the current message along with history
    # Note: You will need to update your controller.py to accept this 'history' parameter
    response = agent_controller(user_message, history)
    
    # Save the new user message and the agent's response to the memory
    history.append({"role": "user", "content": user_message})
      # Save the new user message and the agent's response to the memory
    history.append({"role": "user", "content": user_message})
    
    # Convert the response dictionary into a JSON string before saving to memory
    if isinstance(response, dict):
        history.append({"role": "assistant", "content": json.dumps(response)})
    else:
        history.append({"role": "assistant", "content": str(response)})
    
    # Keep only the last 10 messages to prevent memory overload
    if len(history) > 10:
        history = history[-10:]
        
    chat_memory[session_id] = history
    
    return response