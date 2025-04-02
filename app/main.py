from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .utils import hash
from .routers import post, user, auth, vote, ai

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
    # Prefer Cloudflare's header, then X-Forwarded-For, then client.host
    client_ip = (
        request.headers.get("cf-connecting-ip")
        or request.headers.get("x-forwarded-for")
        or request.client.host
    )

    # If x-forwarded-for has multiple IPs, get the first
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()

    current_user = "Anonymous"  # Replace with actual authentication logic

    return {
        "message": f"Welcome {current_user}!",
        "ip": client_ip
    }
