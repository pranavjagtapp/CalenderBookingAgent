from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langraph_agent import BookingAgent

app = FastAPI()
agent = BookingAgent()

@app.post("/chat/")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")
        print("User said:", user_message)

        reply = agent.run(user_message)
        print("Agent replied:", reply)

        if not isinstance(reply, str):
            reply = str(reply)

        return JSONResponse(content={"response": reply})

    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)

