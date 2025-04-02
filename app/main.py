from fastapi import FastAPI, Request
#from .database import lifespan
from .utils import hash
from .routers import post, user, auth, vote, ai
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(ai.router)

@app.get("/")
async def root(request: Request):
    # Grab original client IP from headers
    forwarded_for = request.headers.get("x-forwarded-for")
    client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host

    # This assumes you have some auth system, stub here:
    current_user = "Anonymous"

    return {
        "message": f"Welcome {current_user}!",
        "ip": client_ip
    }






