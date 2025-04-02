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
    # Prefer Cloudflare's header for public IP
    client_ip = request.headers.get("cf-connecting-ip")

    # Fallback to x-forwarded-for if behind proxy
    if not client_ip:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host

    current_user = "Anonymous"  # Replace with actual auth logic if needed

    return {
        "message": f"Welcome {current_user}!",
        "ip": client_ip
    }




